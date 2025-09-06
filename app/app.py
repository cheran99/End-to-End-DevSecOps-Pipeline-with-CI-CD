from flask import Flask, render_template, request, redirect, url_for
from flask_talisman import Talisman
from google.cloud.sql.connector import Connector, IPTypes
import pymysql
from sqlalchemy import (create_engine, MetaData, Table, Column, Integer, String, Boolean, select, insert, update, engine)
from flask_wtf import FlaskForm, CSRFProtect
from sqlalchemy.orm import declarative_base, Session
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
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


class ToDoForm(FlaskForm):
    name = StringField('to-do item', validators=[DataRequired()])
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


@app.route('/')
def index():
    form = ToDoForm()
    with Session(engine) as session:
        incomplete = session.execute(select(todos).where(todos.c.complete.is_(False))).fetchall()
        complete = session.execute(select(todos).where(todos.c.complete.is_(True))).fetchall()

        return render_template('index.html', incomplete=incomplete, complete=complete, form=form)


@app.route('/add', methods=['POST'])
def add():
    form = ToDoForm()
    if form.validate_on_submit():
        task = form.name.data
        with Session(engine) as session:
            task = request.form["to-do item"]
            query = insert(todos).values(text=task, complete=False)
            session.execute(query)

            return redirect(url_for('index'))
    return redirect(url_for('index'))


@app.route('/complete/<id>')
def complete(id):
    with Session(engine) as session:
        session.execute(update(todos).where(todos.c.id == int(id)).values(complete=True))

        return redirect(url_for('index'))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)   # nosec B104