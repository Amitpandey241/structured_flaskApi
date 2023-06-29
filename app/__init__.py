import os

from flask import Flask, request,jsonify,make_response,Blueprint
from flask_restful import Resource,Api
from flask_pymongo import PyMongo
from flask_jwt_extended import create_access_token, JWTManager, get_jwt_identity, jwt_required
from dotenv import load_dotenv
import secrets


load_dotenv()
app =Flask(__name__)
api= Api(app)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["JWT_SECRET_KEY"] = secrets.token_hex(16)

jwt = JWTManager(app)
mongo = PyMongo(app)
