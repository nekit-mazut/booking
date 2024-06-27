from flask import Flask
from .routes import bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    app.register_blueprint(bp, url_prefix='/email')
    return app