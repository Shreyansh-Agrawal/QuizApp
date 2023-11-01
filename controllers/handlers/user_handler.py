'''Handlers related to generic users: Super Admin, Admin, User'''

import logging
import sqlite3

from controllers import user_controller as UserController
from utils.custom_error import DataNotFoundError, LoginError
from utils.pretty_print import pretty_print


logger = logging.getLogger(__name__)

def display_users_by_role(role: str):
    '''Display users on console by role'''

    data = UserController.get_all_users_by_role(role)

    if not data:
        raise DataNotFoundError(f'No {role} Currently!')

    print(f'\n-----List of {role.title()}s-----\n')
    pretty_print(
        data=data,
        headers=['Username', 'Name', 'Email', 'Registration Date']
    )


def display_user_score(username: str):
    '''Display past scores of user'''

    data = UserController.get_user_scores_by_username(username)

    if not data:
        raise DataNotFoundError('No data! Take a Quiz...')

    print('\n-----Score History-----\n')
    pretty_print(data, ['Time', 'Score'])

    scores = [scores[1] for scores in data]
    print(f'\nHighest Score: {max(scores)}\n')


def handle_create_admin():
    '''Handle admin profile creation'''
    try:
        UserController.create_admin()
    except LoginError as e:
        raise e


def handle_delete_user_by_email(role: str):
    '''Handle user deletion by role'''
    try:
        UserController.delete_user_by_email(role)
    except sqlite3.IntegrityError:
        print('Could Not Delete Admin...')
