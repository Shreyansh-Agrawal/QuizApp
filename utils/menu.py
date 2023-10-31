'''Menu Functions'''

import logging
import sqlite3

from controllers import user_controller as UserController
from controllers import quiz_controller as QuizController
from controllers.handlers import auth_handler as AuthHandler
from controllers.handlers import quiz_handler as QuizHandler
from controllers.handlers import user_handler as UserHandler
from constants import prompts
from utils.custom_error import LoginError, DuplicateEntryError, DataNotFoundError


logger = logging.getLogger(__name__)

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
                    UserController.create_admin()
                except LoginError as e:
                    print(e)
                    continue
            case '2':
                try:
                    UserHandler.display_users_by_role('admin')
                except DataNotFoundError as e:
                    print(e)
                    continue
            case '3':
                try:
                    UserController.delete_user_by_email('admin')
                except sqlite3.IntegrityError:
                    print('Could Not Delete Admin...')
                    continue
            case 'q':
                break
            case _:
                print('Wrong input! Please choose from the above given options...')


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
                UserController.delete_user_by_email('user')
            case 'q':
                break
            case _:
                print('Wrong input! Please choose from the above given options...')


def manage_quizzes_menu(username: str):
    '''Admin: manage quizzes menu'''

    logger.debug('Running Admin: Manage Quizzes Menu')
    while True:
        user_sub_choice = input(prompts.ADMIN_MANAGE_QUIZZES_PROMPTS)

        match user_sub_choice:
            case '1':
                data = QuizController.get_all_categories()
                try:
                    QuizHandler.display_categories(role='admin', data=data, header=['Category', 'Created By'])
                except DataNotFoundError as e:
                    print(e)
                    continue
            case '2':
                data = QuizController.get_all_questions()
                try:
                    QuizHandler.display_questions(data=data)
                except DataNotFoundError as e:
                    print(e)
                    continue
            case '3':
                data = QuizController.get_all_categories()
                try:
                    QuizHandler.display_categories(role='admin', data=data, header=['Category', 'Created By'])
                    QuizController.create_category(username)
                except DuplicateEntryError as e:
                    print(e)
                    continue
            case '4':
                data = QuizController.get_all_categories()
                try:
                    QuizHandler.display_categories(role='admin', data=data, header=['Category', 'Created By'])
                    QuizController.create_question(username)
                except DuplicateEntryError as e:
                    print(e)
                    continue
            case 'q':
                break
            case _:
                print('Wrong input! Please choose from the above given options...')


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
                data = QuizController.get_leaderboard()
                QuizHandler.display_leaderboard(data)
            case '3':
                data = UserController.get_user_scores_by_username(username)
                try:
                    UserHandler.display_user_score(data=data)
                except DataNotFoundError as e:
                    print(e)
                    continue
            case 'q':
                break
            case _:
                print('Wrong input! Please choose from the above given options...')
