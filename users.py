'''
    Contains Super Admin, Admin, User classes
'''

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Dict

import shortuuid

from database.database_helper import DatabaseHelper as DB
from database.queries import Queries


class Person(ABC):
    '''abstract base class
    '''
    
    def __init__(self, name: str, email: str, role: str, username: str, password: str) -> None:
        self.name = name
        self.email = email
        self.role = role
        self.username = username
        self.password = password
        self.registration_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    @abstractmethod
    def save_user_to_database(self) -> None:
        ''''abstract method to create a new user
        '''


class SuperAdmin(Person):
    '''Super Admin class

    Args:
        Person (_type_): _description_
    '''

    def __init__(self, super_admin_obj: Dict) -> None:
        super().__init__(
            super_admin_obj.get('name'),
            super_admin_obj.get('email'),
            super_admin_obj.get('role'),
            super_admin_obj.get('username'),
            super_admin_obj.get('password')
        )

        self.user_id = 'S' + shortuuid.ShortUUID().random(length=5)
        self.is_password_changed = 1

    def save_user_to_database(self) -> None:
        '''method to add user to db
        '''

        insert_into_users_query = Queries.INSERT_USER
        insert_into_credentials_query = Queries.INSERT_CREDENTIALS

        super_admin_data = (
            self.user_id,
            self.name,
            self.email,
            self.role,
            self.registration_date
        )

        credentials = (
            self.user_id,
            self.username,
            self.password,
            self.is_password_changed
        )

        DB.write_to_database(insert_into_users_query, super_admin_data)
        DB.write_to_database(insert_into_credentials_query, credentials)


class Admin(Person):
    '''Admin class

    Args:
        Person (_type_): _description_
    '''

    def __init__(self, admin_obj: Dict) -> None:
        super().__init__(
            admin_obj.get('name'),
            admin_obj.get('email'),
            admin_obj.get('role'),
            admin_obj.get('username'),
            admin_obj.get('password')
            )

        self.user_id = 'A' + shortuuid.ShortUUID().random(length=5)
        self.is_password_changed = 0

    def save_user_to_database(self) -> None:
        '''method to add user to db
        '''

        insert_into_users_query = Queries.INSERT_USER
        insert_into_credentials_query = Queries.INSERT_CREDENTIALS

        admin_data = (
            self.user_id,
            self.name,
            self.email,
            self.role,
            self.registration_date
        )

        credentials = (
            self.user_id,
            self.username,
            self.password,
            self.is_password_changed
        )

        DB.write_to_database(insert_into_users_query, admin_data)
        DB.write_to_database(insert_into_credentials_query, credentials)


class User(Person):
    '''User class

    Args:
        Person (_type_): _description_
    '''
    
    def __init__(self, user_obj: Dict) -> None:
        super().__init__(
            user_obj.get('name'),
            user_obj.get('email'),
            user_obj.get('role'),
            user_obj.get('username'),
            user_obj.get('password')
        )

        self.user_id = 'U' + shortuuid.ShortUUID().random(length=5)
        self.is_password_changed = 1

    def save_user_to_database(self) -> None:
        '''method to add user to db
        '''

        insert_into_users_query = Queries.INSERT_USER
        insert_into_credentials_query = Queries.INSERT_CREDENTIALS

        user_data = (
            self.user_id,
            self.name,
            self.email,
            self.role,
            self.registration_date
        )

        credentials = (
            self.user_id,
            self.username,
            self.password,
            self.is_password_changed
        )

        DB.write_to_database(insert_into_users_query, user_data)
        DB.write_to_database(insert_into_credentials_query, credentials)
