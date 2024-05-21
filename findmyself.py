from flask import Flask
import os
from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', "postgresql://postgres:findmyself123@34.101.69.150:5432")
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', "postgresql://postgres:ta@host.docker.internal:5431")
db.init_app(app)