from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_cors import CORS

mongo = PyMongo()
mongo_quantaxis = PyMongo()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    if app.config["ENV"] == "production":
        app.config.from_object("config.ProdConfig")
    else:
        app.config.from_object("config.DevConfig")

    mongo.init_app(app)
    mongo_quantaxis.init_app(app, "mongodb://localhost:27017/quantaxis")
    jwt.init_app(app)

    from app.v1 import v1_blueprint
    app.register_blueprint(v1_blueprint)

    CORS(app)
    return app
