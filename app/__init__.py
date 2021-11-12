from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


db = SQLAlchemy()

def createApp():
    app = Flask(__name__, static_url_path = '')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/blog'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'static/'
    app.config['SECRET_KEY'] = 'blog-secret'

    CORS(app)

    db.init_app(app)

    return app
