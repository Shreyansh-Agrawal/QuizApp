'''Handlers related to Quiz'''

import logging
from typing import List
from controllers import quiz_controller as QuizController
from utils import validations
from utils.custom_error import DataNotFoundError, DuplicateEntryError
from utils.pretty_print import pretty_print


logger = logging.getLogger(__name__)

def display_categories(role: str, header: List):
    '''Display Categories on Console'''

    logger.debug('Display All Categories')
    data = QuizController.get_all_categories()

    if not data:
        raise DataNotFoundError('No Category Added!')

    print('\n-----Quiz Categories-----\n')

    if role == 'user':
        data = [(tup[0], ) for tup in data]

    pretty_print(data=data, headers=header)


def display_all_questions():
    '''Display All Questions on Console'''

    logger.debug('Display All Questions')
    data = QuizController.get_all_questions()

    if not data:
        logger.debug('No Questions added')
        print('No Questions Currently, Please add a question!!')
        return

    print('\n-----Quiz Questions-----\n')
    pretty_print(
        data=data,
        headers=['Category', 'Question', 'Question Type', 'Answer', 'Created By']
    )


def display_questions_by_category():
    '''Display Questions by Category on Console'''

    logger.debug('Display Questions By Category')

    try:
        display_categories(role='admin', header=['Category', 'Created By'])
        data = QuizController.get_questions_by_category()
    except DataNotFoundError as e:
        logger.debug(e)
        print(e)
        return

    if not data:
        print('No Questions in this category, Please add a question!!')
        return

    pretty_print(
        data=data,
        headers=['Question', 'Question Type', 'Answer', 'Created By']
    )


def display_leaderboard():
    '''Display Leaderboard on Console'''

    data = QuizController.get_leaderboard()

    if not data:
        logger.debug('No Data in Leaderboard')
        print('No data! Take a Quiz...')
        return

    print('\n-----Leaderboard-----\n')
    pretty_print(data=data, headers=['Username', 'Score', 'Time'])


def handle_start_quiz(username: str):
    '''Handler for starting Quiz'''

    logger.debug('Starting Quiz for %s: ', username)

    data = QuizController.get_all_categories()
    categories = [(tup[0], ) for tup in data]
    try:
        display_categories(role='user', header=['Categories'])
    except DataNotFoundError as e:
        logger.debug(e)
        print(e)
        return

    print('\n-----Quiz Starting-----\n')

    user_choice = validations.validate_numeric_input(prompt='Choose a Category: ')
    if user_choice > len(categories) or user_choice-1 < 0:
        print('No such Category! Please choose from above!!')
        return

    category = categories[user_choice-1][0]

    for data in categories:
        if data[0] == category:
            break
    else:
        print('No such Category! Please choose from above!!')
        return

    QuizController.start_quiz(category, username)


def handle_create_category(created_by: str):
    '''Handler for creating category'''

    try:
        display_categories(role='admin', header=['Category', 'Created By'])
    except DataNotFoundError as e:
        logger.debug(e)
        print(e)

    try:
        QuizController.create_category(created_by)
    except DuplicateEntryError as e:
        logger.debug(e)
        print(e)


def handle_create_question(created_by: str):
    '''Handler for creating question'''

    try:
        display_categories(role='admin', header=['Category', 'Created By'])
        QuizController.create_question(created_by)
    except DataNotFoundError as e:
        logger.debug(e)
        print(e)
        return
    except DuplicateEntryError as e:
        logger.debug(e)
        print(e)
        return


def handle_update_category():
    '''Handler for updating a category'''

    try:
        display_categories(role='admin', header=['Category', 'Created By'])
        QuizController.update_category_by_name()
    except DataNotFoundError as e:
        logger.debug(e)
        print(e)
        return


def handle_delete_category():
    '''Handler for deleting a category'''

    try:
        display_categories(role='admin', header=['Category', 'Created By'])
        QuizController.delete_category_by_name()
    except DataNotFoundError as e:
        logger.debug(e)
        print(e)
        return
