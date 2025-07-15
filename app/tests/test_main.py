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
        )
    )
    return pool




