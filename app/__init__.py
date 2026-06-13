from flask import Flask, request
from flask_migrate import Migrate

from .models.db import db
from config import DevelopmentConfig as dc
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

migrate = Migrate()

def create_app():
    app = Flask(__name__)


    app.config.from_object(dc)
    csrf = CSRFProtect(app)


    # env = os.getenv('FLASK_ENV', 'development')
    app.config['SQLALCHEMY_DATABASE_URI'] = dc.database_uri
    # print(app.config['SECRET_KEY'])
    # print(app.config['SQLALCHEMY_DATABASE_URI'])
    db.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        from . import models
        db.create_all()



    # Import and register the blueprint from routes.py
    from .routes import main_bp
    app.register_blueprint(main_bp)

    from datetime import datetime
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}

    return app


