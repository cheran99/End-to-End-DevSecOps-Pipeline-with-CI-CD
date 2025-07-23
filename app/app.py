from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from google.cloud import secretmanager
from google.cloud.sql.connector import Connector, IPTypes
import pymysql
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Boolean, select, insert, update, engine, URL
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
            user=user,
            password=password,
            host=instance_connection_name,
            port=port,
            db=database
        )
        return conn

    engine = create_engine(
        engine.url.URL.create(
            "mysql+pymysql://",
            creator=getconn,
            pool_size=5,
            max_overflow=2,
            pool_timeout=30,
            pool_recycle=1800,
        )
    )
    return engine

engine = get_db_connection () 
metadata = MetaData()
    
todos = Table(
    "todos", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("text", String(200)),
    Column("complete", Boolean),
)

metadata.create_all(engine)

@app.route('/')
def index():
    with engine.connect() as conn:
        incomplete = conn.execute(select(todos).where(todos.c.complete == False)).fetchall()   #todos.query.filter_by(complete=False).all()
        complete = conn.execute(select(todos).where(todos.c.complete == True)).fetchall() #todos.query.filter_by(complete=True).all()

        return render_template('index.html', incomplete=incomplete, complete=complete)

@app.route('/add', methods=['POST'])
def add():
    with engine.begin() as conn:
        if request.method == 'POST':
            task = request.form["to-do item"]
            query = insert(todos).values(text=task, complete = False) 
            #todo = todos(text=request.form['todoitem'], complete=False)
            conn.execute(query)
            conn.commit()

        return redirect(url_for('index'))

@app.route('/complete/<id>')
def complete(id):
    with engine.begin() as conn:
        conn.execute(update(todos).where(todos.c.id == int(id)).values(complete = True)) #todos.query.filter_by(id=int(id)).first()
        conn.commit()

        return redirect(url_for('index'))
