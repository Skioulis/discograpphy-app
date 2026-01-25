from flask import Flask
from .models.db import db
from config import DevelopmentConfig as dc
from config import Config
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    csrf = CSRFProtect(app)


    # env = os.getenv('FLASK_ENV', 'development')
    app.config['SQLALCHEMY_DATABASE_URI'] = dc.database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
    print(app.config['SECRET_KEY'])
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    db = SQLAlchemy(app)
    # migrate = Migrate(app, db)
    db.init_app(app)



    # Import and register the blueprint from app.py
    from .app import main_bp
    app.register_blueprint(main_bp)

    from datetime import datetime
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}

    return app


