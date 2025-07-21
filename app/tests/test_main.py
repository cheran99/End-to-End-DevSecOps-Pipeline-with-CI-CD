from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from google.cloud import secretmanager
from google.cloud.sql.connector import Connector, IPTypes
import pymysql
import sqlalchemy
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

def get_db_connection() -> sqlalchemy.engine.base.Engine:
    user = access_secret_version("db-user")
    password = access_secret_version("db-pass")
    database = access_secret_version("db-name")
    instance_connection_name = access_secret_version("instance-connection-name")
    port = 3306

    ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC 
    connector = Connector(ip_type=ip_type, refresh_strategy="LAZY")

    def getconn() -> pymysql.connections.Connection:
        conn: pymysql.connections.Connection = connector.connect(
            user=user,
            password=password,
            host=instance_connection_name,
            port=port,
            db=database
        )
        return conn

    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL.create(
            "mysql+pymysql://",
            creator=getconn,
            pool_size=5,
            max_overflow=2,
            pool_timeout=30,
            pool_recycle=1800,
        )
    )
    return pool

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)

    def __repr__(self):
        return self.text

@app.route('/')
def index():
    incomplete = Todo.query.filter_by(complete=False).all()
    complete = Todo.query.filter_by(complete=True).all()

    return render_template('index.html', incomplete=incomplete, complete=complete)

@app.route('/add', methods=['POST'])
def add():
    todo = Todo(text=request.form['todoitem'], complete=False)
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/complete/<id>')
def complete(id):

    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()

    return redirect(url_for('index'))
