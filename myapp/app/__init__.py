from flask import Flask
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config_class)

    # Register blueprints
    from .main.routes import main_bp
    from .auth.routes import auth_bp
    from .api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(api_bp)

    return app