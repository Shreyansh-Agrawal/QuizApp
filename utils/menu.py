'''Menu Functions'''

import logging

from controllers.handlers import auth_handler as AuthHandler
from controllers.handlers import quiz_handler as QuizHandler
from controllers.handlers import user_handler as UserHandler
from constants import prompts
from utils import json_to_db_loader
from utils.custom_error import LoginError, DuplicateEntryError, DataNotFoundError
from utils.exception_handler import exception_handler


logger = logging.getLogger(__name__)

@exception_handler
def super_admin_menu(username: str):
    '''Menu for Super Admin'''

    logger.debug('Running Super Admin Menu')
    print('----Super Admin Dashboard----')
    print(f'\n----Welcome {username.upper()}----\n')

    while True:
        user_choice = input(prompts.SUPER_ADMIN_PROMPTS)

        match user_choice:
            case '1':
                try:
                    UserHandler.handle_create_admin()
                except LoginError as e:
                    print(e)
                    continue
            case '2':
                try:
                    UserHandler.display_users_by_role(role='admin')
                except DataNotFoundError as e:
                    print(e)
                    continue
            case '3':
                try:
                    UserHandler.handle_delete_user_by_email(role='admin')
                except DataNotFoundError as e:
                    print(e)
                    continue
            case 'q':
                break
            case _:
                print('Wrong input! Please choose from the above given options...')


@exception_handler
def manage_users_menu():
    '''Admin: manage users menu'''

    logger.debug('Running Admin: Manage Users Menu')
    while True:
        user_sub_choice = input(prompts.ADMIN_MANAGE_USER_PROMPTS)

        match user_sub_choice:
            case '1':
                try:
                    UserHandler.display_users_by_role('user')
                except DataNotFoundError as e:
                    print(e)
                    continue
            case '2':
                try:
                    UserHandler.handle_delete_user_by_email(role='user')
                except DataNotFoundError as e:
                    print(e)
                    continue
            case 'q':
                break
            case _:
                print('Wrong input! Please choose from the above given options...')


@exception_handler
def manage_categories_menu(username: str):
    '''Admin: manage categories menu'''

    logger.debug('Running Admin: Manage Categories Menu')
    while True:
        user_sub_choice = input(prompts.ADMIN_MANAGE_CATEGORIES_PROMPTS)

        match user_sub_choice:
            case '1':
                try:
                    QuizHandler.display_categories(role='admin', header=['Category', 'Created By'])
                except DataNotFoundError as e:
                    print(e)
                    continue
            case '2':
                try:
                    QuizHandler.display_categories(role='admin', header=['Category', 'Created By'])
                except DataNotFoundError as e:
                    print(e)
                try:
                    QuizHandler.handle_create_category(created_by=username)
                except DuplicateEntryError as e:
                    print(e)
                    continue
            case '3':
                try:
                    QuizHandler.display_categories(role='admin', header=['Category', 'Created By'])
                except DataNotFoundError as e:
                    print(e)
                    continue
                QuizHandler.handle_update_category()
            case '4':
                try:
                    QuizHandler.display_categories(role='admin', header=['Category', 'Created By'])
                except DataNotFoundError as e:
                    print(e)
                    continue
                QuizHandler.handle_delete_category()
            case 'q':
                break
            case _:
                print('Wrong input! Please choose from the above given options...')


@exception_handler
def manage_questions_menu(username: str):
    '''Admin: manage questions menu'''

    logger.debug('Running Admin: Manage Questions Menu')
    while True:
        user_sub_choice = input(prompts.ADMIN_MANAGE_QUESTIONS_PROMPTS)

        match user_sub_choice:
            case '1':
                try:
                    QuizHandler.display_all_questions()
                except DataNotFoundError as e:
                    print(e)
                    continue
            case '2':
                try:
                    QuizHandler.display_categories(role='admin', header=['Category', 'Created By'])
                except DataNotFoundError as e:
                    print(e)
                    continue
                try:
                    QuizHandler.display_questions_by_category()
                except DataNotFoundError as e:
                    print(e)
                    continue
            case '3':
                try:
                    QuizHandler.display_categories(role='admin', header=['Category', 'Created By'])
                except DataNotFoundError as e:
                    print(e)
                    continue
                try:
                    QuizHandler.handle_create_question(created_by=username)
                except DuplicateEntryError as e:
                    print(e)
                    continue
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

    logger.debug('Running Admin: Manage Quizzes Menu')
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


@exception_handler
def admin_menu(username: str, is_password_changed: int):
    '''Menu for Admin'''

    logger.debug('Running Admin Menu')
    print('----Admin Dashboard----')
    print(f'\n----Welcome {username.upper()}----\n')

    AuthHandler.handle_first_login(username, is_password_changed)

    while True:
        user_choice = input(prompts.ADMIN_PROMPTS)

        match user_choice:
            case '1':
                print('\n----Manage Users----\n')
                manage_users_menu()
            case '2':
                print('\n----Manage Quizes----\n')
                manage_quizzes_menu(username)
            case 'q':
                break
            case _:
                print('Wrong input! Please choose from the above given options...')


@exception_handler
def user_menu(username: str):
    '''Menu for User'''

    logger.debug('Running User Menu')
    print('\n----User Dashboard----\n')
    print(f'\n----Welcome {username.upper()}----\n')

    while True:
        user_choice = input(prompts.USER_PROMPTS)

        match user_choice:
            case '1':
                try:
                    QuizHandler.handle_start_quiz(username)
                except DataNotFoundError as e:
                    print(e)
                    continue
            case '2':
                try:
                    QuizHandler.display_leaderboard()
                except DataNotFoundError as e:
                    print(e)
                    continue
            case '3':
                try:
                    UserHandler.display_user_score(username)
                except DataNotFoundError as e:
                    print(e)
                    continue
            case 'q':
                break
            case _:
                print('Wrong input! Please choose from the above given options...')


@exception_handler
def assign_menu(data):
    '''Assign menu according to the role'''

    logger.debug('Assigning menu according to the role')
    username, role, is_password_changed = data

    match role:
        case 'super admin':
            super_admin_menu(username)
        case 'admin':
            admin_menu(username, is_password_changed)
        case 'user':
            user_menu(username)
        case _:
            print('Invalid Role!: ', role)


@exception_handler
def start():
    '''Menu for Login / Sign Up'''

    logger.debug('Running start()')
    print('\n---------WELCOME TO QUIZ APP---------\n')

    while True:
        user_choice = input(prompts.AUTH_PROMPTS)

        match user_choice:
            case '1':
                try:
                    data = AuthHandler.handle_login()
                except DataNotFoundError as e:
                    print(e)
                    continue
                assign_menu(data)
            case '2':
                try:
                    username = AuthHandler.handle_signup()
                except LoginError as e:
                    print(e)
                    continue
                user_menu(username)
            case 'q':
                break
            case _:
                print('Wrong input! Please choose from the above given options...')
