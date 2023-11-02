'''Menu Functions'''

import logging

from config import prompts
from controllers.handlers import auth_handler as AuthHandler
from controllers.handlers import menu_handler as MenuHandler
from controllers.handlers import quiz_handler as QuizHandler
from controllers.handlers import user_handler as UserHandler
from utils.exception_handler import exception_handler


logger = logging.getLogger(__name__)

@exception_handler
def super_admin_menu(username: str):
    '''Menu for Super Admin'''

    logger.info('Running Super Admin Menu')
    print('----Super Admin Dashboard----')
    print(f'\n----Welcome {username.upper()}----\n')

    while True:
        user_choice = input(prompts.SUPER_ADMIN_PROMPTS)

        match user_choice:
            case '1':
                UserHandler.handle_create_admin()
            case '2':
                UserHandler.display_users_by_role(role='admin')
            case '3':
                UserHandler.handle_delete_user_by_email(role='admin')
            case 'q':
                break
            case _:
                print('Wrong input! Please choose from the above given options...')


@exception_handler
def admin_menu(username: str, is_password_changed: int):
    '''Menu for Admin'''

    logger.info('Running Admin Menu')
    print('----Admin Dashboard----')
    print(f'\n----Welcome {username.upper()}----\n')

    AuthHandler.handle_first_login(username, is_password_changed)

    while True:
        user_choice = input(prompts.ADMIN_PROMPTS)

        match user_choice:
            case '1':
                print('\n----Manage Users----\n')
                MenuHandler.manage_users_menu()
            case '2':
                print('\n----Manage Quizes----\n')
                MenuHandler.manage_quizzes_menu(username)
            case 'q':
                break
            case _:
                print('Wrong input! Please choose from the above given options...')


@exception_handler
def user_menu(username: str):
    '''Menu for User'''

    logger.info('Running User Menu')
    print('\n----User Dashboard----\n')
    print(f'\n----Welcome {username.upper()}----\n')

    while True:
        user_choice = input(prompts.USER_PROMPTS)

        match user_choice:
            case '1':
                QuizHandler.handle_start_quiz(username)
            case '2':
                QuizHandler.display_leaderboard()
            case '3':
                UserHandler.display_user_score(username)
            case 'q':
                break
            case _:
                print('Wrong input! Please choose from the above given options...')


@exception_handler
def assign_menu(data):
    '''Assign menu according to the role'''

    logger.info('Assigning menu according to the role')
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

    logger.info('Running start()')
    print('\n---------WELCOME TO QUIZ APP---------\n')

    while True:
        user_choice = input(prompts.AUTH_PROMPTS)

        match user_choice:
            case '1':
                data = AuthHandler.handle_login()
                if not data:
                    continue
                assign_menu(data)
            case '2':
                username = AuthHandler.handle_signup()
                if not username:
                    continue
                user_menu(username)
            case 'q':
                break
            case _:
                print('Wrong input! Please choose from the above given options...')
