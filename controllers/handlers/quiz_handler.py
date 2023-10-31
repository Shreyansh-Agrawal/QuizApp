'''Handlers related to Quiz'''

import logging
from typing import List
from controllers import quiz_controller as QuizController
from utils import validations
from utils.display import pretty_print
from utils.custom_error import DataNotFoundError


logger = logging.getLogger(__name__)

def display_categories(role: str, header: List):
    '''Display Categories on Console'''

    data = QuizController.get_all_categories()

    if not data:
        raise DataNotFoundError('No Categories Currently, Please add a Category!!')

    print('\n-----Quiz Categories-----\n')

    if role == 'user':
        data = [(tup[0], ) for tup in data]

    pretty_print(data=data, headers=header)


def display_questions():
    '''Display Questions on Console'''

    data = QuizController.get_all_questions()

    if not data:
        raise DataNotFoundError('No Questions Currently, Please add a question!!')

    print('\n-----Quiz Questions-----\n')
    pretty_print(data=data, headers=['Category', 'Question', 'Question Type', 'Answer', 'Created By'])


def display_leaderboard():
    '''Display Leaderboard'''

    data = QuizController.get_leaderboard()

    if not data:
        raise DataNotFoundError('No data! Take a Quiz...')

    print('\n-----Leaderboard-----\n')
    pretty_print(data=data, headers=['Username', 'Score', 'Time'])


def handle_start_quiz(username: str):
    '''Handler for starting Quiz'''

    print('\n-----Quiz Starting-----\n')

    data = QuizController.get_all_categories()
    categories = [(tup[0], ) for tup in data]
    display_categories(role='user', header=['Categories'])

    category = validations.validate_name(prompt='Select Quiz Category: ')

    for data in data:
        if data[0] == category:
            break
    else:
        raise DataNotFoundError('No such Category! Please choose from above!!')

    QuizController.start_quiz(category, username)
