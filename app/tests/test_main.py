from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from google.cloud import secretmanager
import os

app = Flask(__name__)

project_id = "devsecops-pipeline-463112"

def get_secret(secret_id: str):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("UTF-8")
    return payload

user = get_secret("db-user")
password = get_secret("db-pass")
database = get_secret("db-name")
host = get_secret("instance-connection-name")
port = 3306

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{user}:{password}@{host}:{port}/{database}'

