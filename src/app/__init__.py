from flask import Flask
from flask_login import LoginManager
from config import Config

login_manager = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config_class)
    
    # Init Flask-Login
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "warning"
    login_manager.init_app(app)
    
    # Register blueprints
    from .main.routes import main_bp
    from .auth.routes import auth_bp
    from .api import api_bp
    from .db import teardown_db

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(api_bp)

    app.teardown_appcontext(teardown_db)

    # User loader
    from .models import User
    from .db import get_db

    @login_manager.user_loader
    def load_user(user_id):
        engine = get_db()
        return User.get_by_id(engine, user_id)

    return app
