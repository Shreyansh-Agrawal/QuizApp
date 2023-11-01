'''Handlers related to Quiz'''

import logging
from typing import List
from controllers import quiz_controller as QuizController
from utils import validations
from utils.custom_error import DataNotFoundError
from utils.pretty_print import pretty_print


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

    user_choice = validations.validate_numeric_input(prompt='Choose a Category: ')
    if user_choice > len(categories) or user_choice-1 < 0:
        print('No such Category! Please choose from above!!')
        return

    category = categories[user_choice-1][0]

    for data in categories:
        if data[0] == category:
            break
    else:
        raise DataNotFoundError('No such Category! Please choose from above!!')

    QuizController.start_quiz(category, username)


def handle_create_category(created_by: str):
    '''Handler for creating category'''

    QuizController.create_category(created_by)


def handle_create_question(created_by: str):
    '''Handler for creating question'''

    QuizController.create_question(created_by)
