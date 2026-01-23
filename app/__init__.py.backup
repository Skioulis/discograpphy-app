import os
from flask import Flask
from dotenv import load_dotenv
from .models.db import db

def create_app():
    app = Flask(__name__)


    # env = os.getenv('FLASK_ENV', 'development')
    env = os.getenv('FLASK_ENV', 'development')
    env_file = f'app/env-files/db.env.{env}'

    if os.path.exists(env_file):
        load_dotenv(env_file)
    else:
        # Fallback to a default if the specific env file is missing
        load_dotenv('app/env-files/db.env')

    db_user = os.getenv('DB_USER')
    db_pass = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME')

    database_uri = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    # 3. Apply configuration to Flask
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    if env == 'production':
        load_dotenv('.env.production')
    else:
        load_dotenv('.env.development')

    # Now you can access variables using os.getenv()
    # app.config['DATABASE_URL'] = os.getenv('DB_URL')

    # Import and register the blueprint from app.py
    from .app import main_bp
    app.register_blueprint(main_bp)

    from datetime import datetime
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}

    return app


