import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))


def _build_database_uri():
    db_user = os.getenv('DB_USER')
    db_pass = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME')
    return f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"


DEFAULT_SECRET_KEY = 'you-will-never-guess'


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or DEFAULT_SECRET_KEY

    # Directory where uploaded mp3s / images are stored. Defaults to a `media`
    # folder next to this file, which is also the container's bind-mount target
    # (/app/media). Override with the MEDIA_ROOT environment variable.
    MEDIA_ROOT = os.getenv('MEDIA_ROOT') or os.path.join(basedir, 'media')

    # Cap upload size (mp3s can be large) — exceeding this returns HTTP 413.
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 50 * 1024 * 1024))

    @classmethod
    def validate(cls):
        """Hook for env-specific config checks; overridden where needed."""


class DevelopmentConfig(Config):
    DEBUG = True

    env = os.getenv('FLASK_ENV', 'development')
    env_file = f'app/env-files/db.env.{env}'

    if os.path.exists(env_file):
        load_dotenv(env_file, override=True)
    else:
        # Fallback to a default if the specific env file is missing
        load_dotenv('app/env-files/db.env', override=True)

    database_uri = _build_database_uri()


class ProductionConfig(Config):
    DEBUG = False

    env_file = 'app/env-files/db.env.production'
    if os.path.exists(env_file):
        load_dotenv(env_file, override=True)

    # Re-read SECRET_KEY after the env file is loaded; the base class resolves it
    # at import time, before this file's variables are available.
    SECRET_KEY = os.environ.get('SECRET_KEY') or DEFAULT_SECRET_KEY
    database_uri = os.getenv('DATABASE_URL') or _build_database_uri()

    @classmethod
    def validate(cls):
        if not cls.SECRET_KEY or cls.SECRET_KEY == DEFAULT_SECRET_KEY:
            raise RuntimeError(
                'SECRET_KEY must be set to a non-default value for production. '
                'Set the SECRET_KEY environment variable.'
            )


CONFIG_BY_NAME = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}


def get_config(name=None):
    """Resolve a config class by name, defaulting to FLASK_ENV then development."""
    name = name or os.getenv('FLASK_ENV', 'development')
    return CONFIG_BY_NAME.get(name, DevelopmentConfig)
