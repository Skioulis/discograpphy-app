To make your Flask site multi-language (Internationalization/i18n), the standard and most powerful tool to use is **Flask-Babel**.

Here is a step-by-step guide to setting it up for **English** and **Greek**.

### 1. Install Flask-Babel
First, you need to install the extension:
```bash
pip install Flask-Babel
```

### 2. Initialize Babel in your App
Modify your `app/__init__.py` to initialize Babel and define a "locale selector" to detect the user's preferred language.

```python
from flask_babel import Babel

babel = Babel()

def get_locale():
    # This checks the user's browser settings or a session variable
    return request.accept_languages.best_match(['en', 'el'])

def create_app():
    app = Flask(__name__)
    # ... your config ...
    
    babel.init_app(app, locale_selector=get_locale)
    # ...
```

### 3. Mark Text for Translation
Instead of writing hardcoded text in your templates or forms, wrap them in the `_()` function (or `gettext`).

#### In Templates (`base.html`, `_navbar.html`):
```html
<!-- Replace -->
<a class="nav-link">Home</a>
<!-- With -->
<a class="nav-link">{{ _('Home') }}</a>
```

#### In Forms (`disk_form.py`):
```python
from flask_babel import lazy_gettext as _l

class DiskForm(FlaskForm):
    name = StringField(_l('Disk Name'), validators=[DataRequired()])
```

### 4. Create the Translation Files
You need a configuration file named `babel.cfg` in your root directory:
```text
[python: app/**.py]
[jinja2: app/templates/**.html]
```

Then, run these commands to generate the translation catalogs:

1.  **Extract text:**
    `pybabel extract -F babel.cfg -o messages.pot .`
2.  **Initialize Greek (el) and English (en):**
    `pybabel init -i messages.pot -d app/translations -l el`
    `pybabel init -i messages.pot -d app/translations -l en`

### 5. Translate the Strings
Go to `app/translations/el/LC_MESSAGES/messages.po`. You will see entries like:
```po
msgid "Home"
msgstr "Αρχική"

msgid "Disk Name"
msgstr "Όνομα Δίσκου"
```
Fill in the `msgstr` for all entries.

### 6. Compile the Translations
Finally, compile the `.po` files into `.mo` files that Flask can read:
```bash
pybabel compile -d app/translations
```

### Summary of Workflow
1.  Wrap text in `{{ _('...') }}` in HTML or `_l('...')` in Python.
2.  Run `pybabel extract`.
3.  Run `pybabel update` (to add new strings to existing `.po` files).
4.  Edit the `.po` file in `app/translations/el/` with your Greek translations.
5.  Run `pybabel compile`.

### Pro Tip: Language Switcher
To let users manually switch languages, you can create a route that saves the chosen language in the `session` and update `get_locale()` to check that session variable first.