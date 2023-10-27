'''
    Handlers for user authentication
'''

import hashlib
from typing import Tuple

import maskpass

from database.database_access import DatabaseAccess as DAO
from database.queries import Queries
from models.users import User


class Authenticate:
    '''Authenticates user'''

    @staticmethod
    def login() -> Tuple:
        '''Method for user login'''

        username = input('Enter username: ').lower()
        password = maskpass.askpass(mask='*')
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        user_data = DAO.read_from_database(Queries.GET_CREDENTIALS, (username, ))
        if not user_data:
            print('\nInvalid Credentials! Please Try Again or Sign Up...')
            return ()

        user_password, role, is_password_changed = user_data[0]

        if user_password != hashed_password:
            print('\nInvalid Credentials! Please Try Again or Sign Up...')
            return ()

        print('\nSuccessfully Logged In!\n')
        return (username, role, is_password_changed)

    @staticmethod
    def signup() -> str:
        '''Method for signup, only for user'''

        user_data = {}
        user_data['name'] = input('Enter your name: ').title()
        user_data['email'] = input('Enter your email: ').lower()
        user_data['username'] = input('Enter your username: ').lower()
        password = maskpass.askpass(mask='*')
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        user_data['password'] = hashed_password

        user = User(user_data)
        user.save_user_to_database()

        print('\nAccount created successfully! Redirecting...\n')
        return user_data['username']
