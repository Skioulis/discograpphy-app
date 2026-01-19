import os
from flask import Flask
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)


    env = os.getenv('FLASK_ENV', 'development')

    if env == 'production':
        load_dotenv('.env.production')
    else:
        load_dotenv('.env.development')

    # Now you can access variables using os.getenv()
    app.config['DATABASE_URL'] = os.getenv('DB_URL')

    # Import and register the blueprint from app.py
    from .app import main_bp
    app.register_blueprint(main_bp)

    return app


