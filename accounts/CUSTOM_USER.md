# Custom account model

The project uses `accounts.models.User` with `AUTH_USER_MODEL = 'accounts.User'`.
The model defines its own fields and `UserManager`. It inherits password/session
primitives from `AbstractBaseUser` and permissions support from `PermissionsMixin`;
it does not inherit Django's concrete `User` or `AbstractUser` model.

Username remains the login identifier. The existing account API and habit code
resolve the selected model with `get_user_model()` and `settings.AUTH_USER_MODEL`.
The admin forms are configured for the project model.

The table names `auth_user`, `auth_user_groups`, and `auth_user_user_permissions`
are deliberately retained for compatibility with existing data. Their owning
model is now `accounts.User`. Existing IDs, password hashes, memberships, sessions
and habit foreign keys are retained.

## Fresh database

Run `python manage.py migrate` normally. The initial accounts migration creates
the custom user tables. No manual adoption is required.

## Existing database originally using auth.User

Changing the user model alters migration dependencies, so simply changing the
setting can produce `InconsistentMigrationHistory` for admin or habit migrations.
Before enabling the new setting, with the app stopped, run:

```powershell
.venv\Scripts\python.exe -B accounts\bootstrap_existing_user.py db.sqlite3
```

This SQLite helper checks the existing columns and foreign keys, creates a
timestamped `.bak` beside the database, records the initial accounts migration
whose tables already exist, and moves the user content type to `accounts` while
keeping permission IDs. It leaves user and habit rows unchanged. It refuses
unexpected schemas, and rerunning it after adoption makes no changes.

Then enable `AUTH_USER_MODEL = 'accounts.User'` and run:

```powershell
.venv\Scripts\python.exe -B manage.py migrate
.venv\Scripts\python.exe -B manage.py check
.venv\Scripts\python.exe -B manage.py test accounts
```

The supplied helper is specifically for this existing SQLite schema. Review
other database schemas separately before adopting them. To roll back this
adoption, restore the backup and previous account/configuration files together.
