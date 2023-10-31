'''Handlers related to Quiz'''

import logging
from typing import List, Tuple
from controllers import quiz_controller as QuizController
from utils import validations
from utils.display import pretty_print
from utils.custom_error import DataNotFoundError


logger = logging.getLogger(__name__)

def display_categories(role: str, data: List[Tuple], header: List):
    '''Display Categories on Console'''

    if not data:
        raise DataNotFoundError('No Categories Currently, Please add a Category!!')

    print('\n-----Quiz Categories-----\n')

    if role == 'user':
        data = [(tup[0], ) for tup in data]

    pretty_print(data=data, headers=header)


def display_questions(data: List[Tuple]):
    '''Display Questions on Console'''
    if not data:
        raise DataNotFoundError('No Questions Currently, Please add a question!!')

    print('\n-----Quiz Questions-----\n')
    pretty_print(data=data, headers=['Category', 'Question', 'Question Type', 'Answer', 'Created By'])


def display_leaderboard(data: List[Tuple]):
    '''Display Leaderboard'''

    if not data:
        raise DataNotFoundError('No data! Take a Quiz...')

    print('\n-----Leaderboard-----\n')
    pretty_print(data=data, headers=['Username', 'Score', 'Time'])


def handle_start_quiz(username: str):
    '''Handler for starting Quiz'''

    print('\n-----Quiz Starting-----\n')

    data = QuizController.get_all_categories()
    categories = [(tup[0], ) for tup in data]
    display_categories(role='user', data=categories, header=['Categories'])

    category = validations.validate_name(prompt='Select Quiz Category: ')

    for data in data:
        if data[0] == category:
            break
    else:
        raise DataNotFoundError('No such Category! Please choose from above!!')

    QuizController.start_quiz(category, username)
