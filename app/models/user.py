from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from db.database import db

@dataclass
class User:
    id: int
    telegram_id: int
    first_name: str
    last_name: str
    is_active: bool
    is_admin: bool
    creation_date: Optional[datetime] = None

def register_user(telegram_id: int, first_name: str, last_name: Optional[str]) -> None:
    with db.connect() as connection:
        cursor = connection.cursor()
        sql = '''
            insert into users (
                telegram_id,
                first_name,
                last_name,
                is_active,
                is_admin
            ) values (
                :telegram_id,
                :first_name,
                :last_name,
                :is_active,
                :is_admin
            );
        '''
        params = {
            'telegram_id': telegram_id,
            'first_name': first_name,
            'last_name': last_name or None,
            'is_active': True,
            'is_admin': False
        }
        cursor.execute(sql, params)
        connection.commit()

def get_user(telegram_id: int) -> Optional[User]:
    ret = None
    with db.connect() as connection:
        cursor = connection.cursor()
        cursor.row_factory = lambda _, row: User(*row)
        sql = '''
            select *
            from users
            where telegram_id = :telegram_id
            limit 1;
        '''
        params = {
            'telegram_id': telegram_id
        }
        cursor.execute(sql, params)
        ret = cursor.fetchone()
    return ret

def set_user_admin(user_id: int, change_to: bool) -> None:
     with db.connect() as connection:
        cursor = connection.cursor()
        cursor.row_factory = lambda _, row: User(*row)
        sql = '''
            update users
            set is_admin = :change_to
            where users.id = :user_id;
        '''
        params = {
            'user_id': user_id,
            'change_to': change_to
        }
        cursor.execute(sql, params)
        connection.commit()

def set_user_active(user_id: int, change_to: bool) -> None:
     with db.connect() as connection:
        cursor = connection.cursor()
        cursor.row_factory = lambda _, row: User(*row)
        sql = '''
            update users
            set is_active = :change_to
            where users.id = :user_id;
        '''
        params = {
            'user_id': user_id,
            'change_to': change_to
        }
        cursor.execute(sql, params)
        connection.commit()
