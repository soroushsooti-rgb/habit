"""Adopt the existing SQLite user tables before enabling accounts.User.

Run once on the old database before switching AUTH_USER_MODEL. Fresh databases
must use normal migrations instead. No user or habit rows are changed.
"""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import sqlite3


def adopt(database):
    database = Path(database).resolve(strict=True)
    connection = sqlite3.connect(database)
    try:
        applied = connection.execute(
            "SELECT 1 FROM django_migrations WHERE app='accounts' AND name='0001_initial'"
        ).fetchone()
        if applied:
            print('accounts.0001_initial is already recorded; no changes made.')
            return
        if not connection.execute(
            "SELECT 1 FROM django_migrations WHERE app='auth' "
            "AND name='0012_alter_user_first_name_max_length'"
        ).fetchone():
            raise RuntimeError('The existing auth migrations must be applied first.')
        expected = {
            'auth_user': {'id', 'username', 'email', 'password', 'last_login',
                          'first_name', 'last_name', 'is_staff', 'is_active',
                          'is_superuser', 'date_joined'},
            'auth_user_groups': {'id', 'user_id', 'group_id'},
            'auth_user_user_permissions': {'id', 'user_id', 'permission_id'},
        }
        for table, columns in expected.items():
            actual = {row[1] for row in connection.execute(f'PRAGMA table_info({table})')}
            if actual != columns:
                raise RuntimeError(f'Unexpected schema for {table}; adoption aborted.')
        if connection.execute('PRAGMA foreign_key_check').fetchall():
            raise RuntimeError('Existing foreign key errors; adoption aborted.')
        if connection.execute(
            "SELECT 1 FROM django_content_type WHERE app_label='accounts' AND model='user'"
        ).fetchone():
            raise RuntimeError('An accounts user content type already exists; review it first.')
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        backup = database.with_name(f'{database.name}.before-custom-user-{stamp}.bak')
        with sqlite3.connect(backup) as target:
            connection.backup(target)
        with connection:
            # The initial migration describes tables already present in this database.
            connection.execute(
                'INSERT INTO django_migrations (app, name, applied) VALUES (?, ?, ?)',
                ('accounts', '0001_initial', datetime.now(timezone.utc).isoformat()),
            )
            # Retain permission IDs, group membership and admin log references.
            connection.execute(
                "UPDATE django_content_type SET app_label='accounts' "
                "WHERE app_label='auth' AND model='user'"
            )
        print(f'Existing tables adopted. Backup: {backup}')
    finally:
        connection.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('database', help='Path to the existing db.sqlite3')
    adopt(parser.parse_args().database)
