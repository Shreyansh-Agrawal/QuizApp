'''Handlers related to generic users: Super Admin, Admin, User'''

import logging

from controllers import user_controller as UserController
from utils.display import pretty_print
from utils.custom_error import DataNotFoundError


logger = logging.getLogger(__name__)

def display_users_by_role(role: str):
    '''Display users on console by role'''

    data = UserController.get_all_users_by_role(role)

    if not data:
        print(f'\nNo {role} Currently, Please Create One!\n')
        raise DataNotFoundError(f'No {role} Currently, Please Create One!')

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
