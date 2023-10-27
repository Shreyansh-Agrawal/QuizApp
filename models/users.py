'''
    Contains Super Admin, Admin, User classes
'''

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Dict

import shortuuid

from database.database_access import DatabaseAccess as DAO
from database.queries import Queries


class Person(ABC):
    '''abstract base class'''

    def __init__(self, name: str, email: str, username: str, password: str) -> None:
        self.name = name
        self.email = email
        self.username = username
        self.password = password
        self.registration_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    @abstractmethod
    def save_user_to_database(self) -> None:
        ''''abstract method to create a new user'''


class SuperAdmin(Person):
    '''Super Admin class

    Args:
        Person (_type_): _description_
    '''

    def __init__(self, super_admin_data: Dict) -> None:
        super().__init__(
            super_admin_data.get('name'),
            super_admin_data.get('email'),
            super_admin_data.get('username'),
            super_admin_data.get('password')
        )

        self.user_id = 'S' + shortuuid.ShortUUID().random(length=5)
        self.role = 'super admin'
        self.is_password_changed = 1

    def save_user_to_database(self) -> None:
        '''method to add user to database'''

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

        DAO.write_to_database(insert_into_users_query, super_admin_data)
        DAO.write_to_database(insert_into_credentials_query, credentials)


class Admin(Person):
    '''Admin class

    Args:
        Person (_type_): _description_
    '''

    def __init__(self, admin_data: Dict) -> None:
        super().__init__(
            admin_data.get('name'),
            admin_data.get('email'),
            admin_data.get('username'),
            admin_data.get('password')
            )

        self.user_id = 'A' + shortuuid.ShortUUID().random(length=5)
        self.role = 'admin'
        self.is_password_changed = 0

    def save_user_to_database(self) -> None:
        '''method to add user to database'''

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

        DAO.write_to_database(insert_into_users_query, admin_data)
        DAO.write_to_database(insert_into_credentials_query, credentials)


class User(Person):
    '''User class

    Args:
        Person (_type_): _description_
    '''

    def __init__(self, user_data: Dict) -> None:
        super().__init__(
            user_data.get('name'),
            user_data.get('email'),
            user_data.get('username'),
            user_data.get('password')
        )

        self.user_id = 'U' + shortuuid.ShortUUID().random(length=5)
        self.role = 'user'
        self.is_password_changed = 1

    def save_user_to_database(self) -> None:
        '''method to add user to database'''

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

        DAO.write_to_database(insert_into_users_query, user_data)
        DAO.write_to_database(insert_into_credentials_query, credentials)
