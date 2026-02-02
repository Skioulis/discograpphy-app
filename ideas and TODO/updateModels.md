To add `created_at` and `updated_at` fields to your models and database, follow these steps. Since you are using Flask-SQLAlchemy with `sqlalchemy.orm.Mapped` and Flask-Migrate, the process involves updating your model definitions and then running a migration.

### 1. Update your Models

You can add these fields to each model manually, or create a base mixin class to avoid repetition.

#### Option A: Manually adding to a model (e.g., `Song.py`)
Add the following imports and columns to your class:

```python
from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so

class Song(db.Model):
    # ... existing fields ...
    
    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime, 
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
```

#### Option B: Using a Mixin (Recommended)
If you want these fields on all models (Song, Disk, Person, etc.), create a mixin in a common file or `app/models/db.py`:

```python
from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so

class TimestampMixin:
    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime, 
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

# Then apply it to your models:
class Song(db.Model, TimestampMixin):
    __tablename__ = 'songs'
    # ...
```

### 2. Update the Database

Since you have Flask-Migrate configured, use the following terminal commands to apply the changes to your database without losing data:

1.  **Generate a migration script:**
    ```bash
    flask db migrate -m "add timestamps to models"
    ```
    This will create a new file in your `migrations/versions/` folder.

2.  **Apply the migration:**
    ```bash
    flask db upgrade
    ```

### Important Notes
*   **Existing Data:** When you add these columns to a table that already has data, the `created_at` and `updated_at` fields will be populated with the current time for all existing rows at the moment the migration runs.
*   **Timezones:** Using `datetime.now(timezone.utc)` is best practice to ensure consistency across different server environments.