from flask import Flask, request, render_template
from flask_migrate import Migrate

from .models.db import db
# DevelopmentConfig kept importable as `dc` for the test suite, which overrides
# its database_uri before calling create_app().
from config import DevelopmentConfig as dc
from config import get_config
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

migrate = Migrate()

def create_app(config_class=None):
    app = Flask(__name__)

    if config_class is None:
        config_class = get_config()

    config_class.validate()
    app.config.from_object(config_class)
    app.config['SECRET_KEY'] = config_class.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = config_class.database_uri
    csrf = CSRFProtect(app)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models so Flask-Migrate can detect them. The schema is owned by
    # Alembic migrations (flask db upgrade), not db.create_all().
    from . import models  # noqa: F401

    # Import and register the blueprint from routes.py
    from .routes import main_bp
    app.register_blueprint(main_bp)

    from datetime import datetime, timezone
    @app.context_processor
    def inject_now():
        return {'now': datetime.now(timezone.utc)}

    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    return app


