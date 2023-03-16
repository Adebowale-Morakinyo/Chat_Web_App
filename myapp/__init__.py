from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from myapp.config import Config
from myapp.database import db

socket = SocketIO()
cors = CORS()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    socket.init_app(app, cors_allowed_origins="*")
    cors.init_app(app)

    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()

        # Register blueprints
        from .views import views
        app.register_blueprint(views)

        return app, socket
