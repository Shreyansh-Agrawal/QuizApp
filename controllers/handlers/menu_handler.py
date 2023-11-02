'''Handlers related to Menu'''

import logging

from constants import prompts
from controllers.handlers import quiz_handler as QuizHandler
from controllers.handlers import user_handler as UserHandler
from utils import json_to_db_loader
from utils.custom_error import DataNotFoundError
from utils.exception_handler import exception_handler


logger = logging.getLogger(__name__)

@exception_handler
def manage_users_menu():
    '''Admin: manage users menu'''

    logger.info('Running Admin: Manage Users Menu')
    while True:
        user_sub_choice = input(prompts.ADMIN_MANAGE_USER_PROMPTS)

        match user_sub_choice:
            case '1':
                UserHandler.display_users_by_role('user')
            case '2':
                UserHandler.handle_delete_user_by_email(role='user')
            case 'q':
                break
            case _:
                print('Wrong input! Please choose from the above given options...')


@exception_handler
def manage_categories_menu(username: str):
    '''Admin: manage categories menu'''

    logger.info('Running Admin: Manage Categories Menu')
    while True:
        user_sub_choice = input(prompts.ADMIN_MANAGE_CATEGORIES_PROMPTS)

        match user_sub_choice:
            case '1':
                try:
                    QuizHandler.display_categories(role='admin', header=['Category', 'Created By'])
                except DataNotFoundError as e:
                    logger.error(e)
                    print(e)
                    continue
            case '2':
                QuizHandler.handle_create_category(created_by=username)
            case '3':
                QuizHandler.handle_update_category()
            case '4':
                QuizHandler.handle_delete_category()
            case 'q':
                break
            case _:
                print('Wrong input! Please choose from the above given options...')


@exception_handler
def manage_questions_menu(username: str):
    '''Admin: manage questions menu'''

    logger.info('Running Admin: Manage Questions Menu')
    while True:
        user_sub_choice = input(prompts.ADMIN_MANAGE_QUESTIONS_PROMPTS)

        match user_sub_choice:
            case '1':
                QuizHandler.display_all_questions()
            case '2':
                QuizHandler.display_questions_by_category()
            case '3':
                QuizHandler.handle_create_question(created_by=username)
            case '4':
                json_to_db_loader.load_questions_from_json(created_by_admin_username=username)
                print('Questions Added!')
            case 'q':
                break
            case _:
                print('Wrong input! Please choose from the above given options...')


@exception_handler
def manage_quizzes_menu(username: str):
    '''Admin: manage quizzes menu'''

    logger.info('Running Admin: Manage Quizzes Menu')
    while True:
        user_sub_choice = input(prompts.ADMIN_MANAGE_QUIZZES_PROMPTS)

        match user_sub_choice:
            case '1':
                print('\n----Manage Categories----\n')
                manage_categories_menu(username)
            case '2':
                print('\n----Manage Questions----\n')
                manage_questions_menu(username)
            case 'q':
                break
            case _:
                print('Wrong input! Please choose from the above given options...')
