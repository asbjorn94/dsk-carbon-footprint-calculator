from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from local_config import sqllite_dir

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = sqllite_dir
# app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///mydatabase.db'
# app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:////home/asbjorn/mysite/mydatabase.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
#30.34