import os
from dotenv import load_dotenv


def _build_database_uri():
    db_user = os.getenv('DB_USER')
    db_pass = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME')
    return f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'


class DevelopmentConfig(Config):
    DEBUG = True

    env = os.getenv('FLASK_ENV', 'development')
    env_file = f'app/env-files/db.env.{env}'

    if os.path.exists(env_file):
        load_dotenv(env_file)
    else:
        # Fallback to a default if the specific env file is missing
        load_dotenv('app/env-files/db.env')

    database_uri = _build_database_uri()


class ProductionConfig(Config):
    DEBUG = False

    env_file = 'app/env-files/db.env.production'
    if os.path.exists(env_file):
        load_dotenv(env_file)

    database_uri = os.getenv('DATABASE_URL') or _build_database_uri()


CONFIG_BY_NAME = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}


def get_config(name=None):
    """Resolve a config class by name, defaulting to FLASK_ENV then development."""
    name = name or os.getenv('FLASK_ENV', 'development')
    return CONFIG_BY_NAME.get(name, DevelopmentConfig)
