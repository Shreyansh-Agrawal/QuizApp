'''Handlers related to Authentication'''

import hashlib
import logging

import maskpass

from constants import prompts
from constants.queries import Queries
from controllers import auth_controller as Authenticate
from database.database_access import DatabaseAccess as DAO
from utils.custom_error import LoginError, DataNotFoundError


logger = logging.getLogger(__name__)

def handle_login():
    '''Handles Login'''

    print('\n----Login----\n')
    attempts_remaining = prompts.ATTEMPT_LIMIT

    data = Authenticate.login()
    while not data:
        attempts_remaining -= 1
        print(f'Remaining attempts: {attempts_remaining}\n')

        if attempts_remaining == 0:
            raise DataNotFoundError('Account Not Found! Please Sign up!')

        data = Authenticate.login()

    return data


def handle_signup():
    '''Handles Signup'''

    print('\n----SignUp----\n')
    try:
        username = Authenticate.signup()
    except LoginError as e:
        raise e

    print('Redirecting...')
    return username


def handle_first_login(username: str, is_password_changed: int):
    '''Checks Admin's First Login'''

    if not is_password_changed:
        logger.debug('Changing Default Admin Password')
        print('\nPlease change your password...\n')

        new_password = maskpass.askpass(prompt='Enter New Password: ', mask='*')
        confirm_password = ''

        while True:
            confirm_password =  maskpass.askpass(prompt='Confirm Password: ', mask='*')
            if new_password != confirm_password:
                print('Password does not match. Please enter your password again!\n')
            else:
                break

        hashed_password = hashlib.sha256(confirm_password.encode('utf-8')).hexdigest()
        is_password_changed = 1

        DAO.write_to_database(
            Queries.UPDATE_ADMIN_PASSWORD,
            (hashed_password, is_password_changed, username)
        )

        logger.debug('Default Admin Password Changed')
        print('\nPassword changed successfully!\n')
