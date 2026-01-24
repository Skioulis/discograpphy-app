## Ideas to consider
* create a config file named config.py
  ```python
  import os

  class Config:
      SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
  
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
  ```

