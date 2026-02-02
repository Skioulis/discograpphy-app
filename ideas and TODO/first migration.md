The error `Error: No such command 'db'.` occurs because `Flask-Migrate` has not been initialized with your Flask application. While you have imported `Migrate` in `app/__init__.py`, it is not being instantiated and linked to the `app` and `db` objects.

To fix this and enable the `flask db` commands, follow these steps:

### 1. Update `app/__init__.py`
You need to create an instance of `Migrate` and initialize it with your app.

Modify your `app/__init__.py` as follows:

```python
# ... other imports
from flask_migrate import Migrate

# Create the migrate instance
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    # ... configuration code

    db.init_app(app)
    # Initialize migrate with the app and db
    migrate.init_app(app, db)

    # ... rest of the function
```

### 2. Set the `FLASK_APP` Environment Variable
The `flask` command needs to know where your application factory is. Since you have a `run-dev.py` file that creates the app, you can point to it:

```bash
export FLASK_APP=run-dev.py
```
*(On Windows PowerShell: `$env:FLASK_APP = "run-dev.py"`)*

### 3. Run Migration Commands
Once the code is updated and the environment variable is set, the `db` command will be available:

1.  **Initialize the migration repository** (only once):
    ```bash
    flask db init
    ```
2.  **Generate a migration script**:
    ```bash
    flask db migrate -m "Initial migration"
    ```
3.  **Apply the migration to the database**:
    ```bash
    flask db upgrade
    ```

### Why this happened:
Flask-SQLAlchemy provides `db.create_all()`, but it doesn't provide the `flask db` CLI commands. Those commands come from the **Flask-Migrate** extension. Importing the class is not enough; you must call `migrate.init_app(app, db)` so the extension can register its commands with the Flask CLI.