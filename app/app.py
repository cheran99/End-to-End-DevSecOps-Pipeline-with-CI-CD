from flask import Flask, render_template, redirect, url_for, jsonify, Response
from flask_talisman import Talisman
from google.cloud.sql.connector import Connector, IPTypes
from sqlalchemy import (create_engine, MetaData, Table, Column, Integer, String, Boolean, select, insert, update, engine)
from flask_wtf import FlaskForm, CSRFProtect
from sqlalchemy.orm import declarative_base, Session
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFError
import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import pymysql
import logging
import os

app = Flask(__name__)

project_id = "devsecops-pipeline-463112"


def access_secret_version(secret_id: str):
    from google.cloud import secretmanager
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("UTF-8")
    return payload


app.config['SECRET_KEY'] = access_secret_version("flask-secret-key")

csrf = CSRFProtect(app)

csp = {
    'default-src': "'self'",
    'style-src': ["'self'", 'https://fonts.googleapis.com'],
    'font-src': ["'self'", 'https://fonts.gstatic.com']
}
Talisman(app, content_security_policy=csp, force_https=True)


client = google.cloud.logging.Client()
client.setup_logging()

handler = CloudLoggingHandler(client)

logger = logging.getLogger("todo_app")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

logger.info("App started successfully")


ADD_COUNTER = Counter('todo_app_requests_total', 'Total number of add requests')
ADD_LATENCY = Histogram('todo_add_request_latency_seconds', 'Latency of add requests in seconds')
CSRF_FAILURES = Counter('csrf_failures_total', 'Total number of failed CSRF attempts')


class ToDoForm(FlaskForm):
    name = StringField('To-Do Item', validators=[DataRequired()])
    submit = SubmitField('Add Item')


def get_db_connection() -> engine.base.Engine:
    user = access_secret_version("db-user")
    password = access_secret_version("db-pass")
    database = access_secret_version("db-name")
    instance_connection_name = access_secret_version("instance-connection-name")
    port = 3306

    ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC
    connector = Connector(ip_type=ip_type, refresh_strategy="LAZY")

    def getconn() -> pymysql.connections.Connection:
        conn: pymysql.connections.Connection = connector.connect(
            instance_connection_string=instance_connection_name,
            driver="pymysql",
            user=user,
            password=password,
            port=port,
            db=database
        )
        return conn

    engine = create_engine(
        "mysql+pymysql://",
        creator=getconn,
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=1800,
    )
    return engine


engine = get_db_connection()
metadata = MetaData()
Base = declarative_base()


todos = Table(
    "todos", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("text", String(200)),
    Column("complete", Boolean),
)

Base.metadata.create_all(engine)


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    CSRF_FAILURES.inc()
    logger.warning(f"CSRF failure: {e.description}")
    return "Bad Request: CSRF token missing or invalid", 400


@app.route('/')
def index():
    form = ToDoForm()
    with Session(engine) as session:
        incomplete = session.execute(select(todos).where(todos.c.complete.is_(False))).fetchall()
        complete = session.execute(select(todos).where(todos.c.complete.is_(True))).fetchall()
    return render_template('index.html', incomplete=incomplete, complete=complete, form=form)


@app.route('/add', methods=['POST'])
def add():
    with ADD_LATENCY.time():
        ADD_COUNTER.inc()
        form = ToDoForm()
        if form.validate_on_submit():
            task = form.name.data
            with Session(engine) as session:
                query = insert(todos).values(text=task, complete=False)
                session.execute(query)
                session.commit()
            logger.info(f"Task added: {task}")
            return redirect(url_for('index'))
        logger.warning("CSRF validation failed")
        return "Bad Request: CSRF token missing or invalid", 400


@app.route('/complete/<id>')
def complete(id):
    with Session(engine) as session:
        session.execute(update(todos).where(todos.c.id == int(id)).values(complete=True))
        session.commit()
    logger.info(f"Task completed: {id}")
    return redirect(url_for('index'))


@app.route('/metrics')
def metrics():
    return Response(generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST})


@app.route('/health')
def health():
    return jsonify(status="ok"), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)   # nosec B104
