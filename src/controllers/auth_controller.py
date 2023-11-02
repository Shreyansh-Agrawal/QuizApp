'''Controllers for Operations related to Authentication'''

import hashlib
import logging
from typing import Tuple
import sqlite3

from database.database_access import DatabaseAccess as DAO
from config.queries import Queries
from models.user import User
from utils import validations
from utils.custom_error import LoginError


logger = logging.getLogger(__name__)

def login() -> Tuple:
    '''Method for user login'''

    logger.debug('Login Initiated')

    # validating credentials even during login to prevent any Injections
    username = validations.validate_username(prompt='Enter your username: ')
    password = validations.validate_password(prompt='Enter your password: ')
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


def signup() -> str:
    '''Method for signup, only for user'''

    logger.debug('Signup Initiated')

    user_data = {}
    user_data['name'] = validations.validate_name(prompt='Enter your name: ')
    user_data['email'] = validations.validate_email(prompt='Enter your email: ')
    user_data['username'] = validations.validate_username(prompt='Create your username: ')
    password = validations.validate_password(prompt='Create your password: ')
    confirm_password = ''

    while True:
        confirm_password =  validations.validate_password(prompt='Confirm Password: ')
        if password != confirm_password:
            print('Password does not match. Please re-enter your password!\n')
        else:
            break

    hashed_password = hashlib.sha256(confirm_password.encode('utf-8')).hexdigest()
    user_data['password'] = hashed_password

    user = User(user_data)

    try:
        user.save_user_to_database()
    except sqlite3.IntegrityError as e:
        raise LoginError(
            'User already exists! Login or Sign Up with different credentials...'
        ) from e

    logger.debug('Signup Successful')
    print('\nAccount created successfully!\n')

    return user_data['username']
