'''
    Handlers for user authentication
'''

import hashlib
import logging
from typing import Tuple

import maskpass

from database.database_access import DatabaseAccess as DAO
from database.queries import Queries
from models.user import User


logger = logging.getLogger(__name__)


class Authenticate:
    '''Authenticates user'''

    @staticmethod
    def login() -> Tuple:
        '''Method for user login'''

        logger.debug('Login Initiated')

        username = input('Enter username: ').lower()
        password = maskpass.askpass(mask='*')
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        user_data = DAO.read_from_database(Queries.GET_CREDENTIALS_BY_USERNAME, (username, ))
        if not user_data:
            print('\nInvalid Credentials! Please Try Again or Sign Up...')
            return ()

        user_password, role, is_password_changed = user_data[0]

        if not is_password_changed and user_password != password:
            print('\nInvalid Credentials! Please Try Again or Sign Up...')
            return ()

        if is_password_changed and user_password != hashed_password:
            print('\nInvalid Credentials! Please Try Again or Sign Up...')
            return ()

        logger.debug('Login Successful')
        print('\nSuccessfully Logged In!\n')

        return (username, role, is_password_changed)

    @staticmethod
    def signup() -> str:
        '''Method for signup, only for user'''

        logger.debug('Signup Initiated')

        user_data = {}
        user_data['name'] = input('Enter your name: ').title()
        user_data['email'] = input('Enter your email: ').lower()
        user_data['username'] = input('Enter your username: ').lower()
        password = maskpass.askpass(mask='*')
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        user_data['password'] = hashed_password

        user = User(user_data)
        user.save_user_to_database()

        logger.debug('Signup Successful')
        print('\nAccount created successfully!\n')

        return user_data['username']
