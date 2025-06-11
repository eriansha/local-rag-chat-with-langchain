from flask import Flask
from flask_cors import CORS
from app.routes import routes

def create_app():
    app = Flask(__name__)

    # Allow all origins (for development)
    CORS(app)

    # OR restrict to specific origin:
    # CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

    app.register_blueprint(routes)
    return app
