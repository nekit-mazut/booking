from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .models import db

def create_app():
    app = Flask(__name__)

    try:
        app.config.from_object('app.config.Config')
        db.init_app(app)
        migrate = Migrate(app, db)
        jwt = JWTManager(app)


        CORS(app)

        from .routes import bp as user_bp
        app.register_blueprint(user_bp)
    except Exception as e:
        app.logger.error(f'Error while creating the app: {e}')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=app.config['PORT'])