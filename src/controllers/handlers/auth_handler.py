'''Handlers related to Authentication'''

import hashlib
import logging

from config import prompts
from config.queries import Queries
from controllers import auth_controller as Authenticate
from database.database_access import DatabaseAccess as DAO
from utils import validations
from utils.custom_error import LoginError


logger = logging.getLogger(__name__)

def handle_login():
    '''Handles Login'''

    logger.debug('Login started...')
    print('\n----Login----\n')

    attempts_remaining = prompts.ATTEMPT_LIMIT

    data = Authenticate.login()
    while not data:
        attempts_remaining -= 1
        print(f'Remaining attempts: {attempts_remaining}\n')

        if attempts_remaining == 0:
            print('Account Not Found! Please Sign up!')
            logger.debug('Login attempts exhausted')
            return None

        data = Authenticate.login()

    logger.debug('Login Successful')
    return data


def handle_signup():
    '''Handles Signup'''

    logger.debug('SignUp started...')
    print('\n----SignUp----\n')

    try:
        username = Authenticate.signup()
    except LoginError as e:
        print(e)
        logger.debug(e)
        return None

    logger.debug('SignUp Successful')
    print('Redirecting...')
    return username


def handle_first_login(username: str, is_password_changed: int):
    '''Checks Admin's First Login'''

    if not is_password_changed:
        print('\nPlease change your password...\n')
        logger.debug('Changing Default Admin Password')

        new_password = validations.validate_password(prompt='Enter New Password: ')
        confirm_password = ''

        while True:
            confirm_password =  validations.validate_password(prompt='Confirm Password: ')
            if new_password != confirm_password:
                print('Password does not match. Please enter your password again!\n')
            else:
                break

        hashed_password = hashlib.sha256(confirm_password.encode('utf-8')).hexdigest()
        is_password_changed = 1

        DAO.write_to_database(
            Queries.UPDATE_ADMIN_PASSWORD_BY_USERNAME,
            (hashed_password, is_password_changed, username)
        )

        logger.debug('Default Admin Password Changed')
        print('\nPassword changed successfully!\n')
