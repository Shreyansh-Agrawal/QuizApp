'''Menu Functions'''

import hashlib
import logging
import sqlite3

import maskpass

from controllers import auth_controller as Authenticate
from controllers import user_controller as UserController
from controllers import quiz_controller as QuizController
from constants.queries import Queries
from constants import prompts
from database.database_access import DatabaseAccess as DAO
from utils import display
from utils import validations
from utils.custom_error import LoginError, DuplicateEntryError


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
                print('\n----Login----\n')
                attempts_remaining = prompts.ATTEMPT_LIMIT

                data = Authenticate.login()
                while not data:
                    attempts_remaining -= 1
                    print(f'Remaining attempts: {attempts_remaining}\n')

                    if attempts_remaining == 0:
                        print('Account Not Found! Please Sign up!\n')
                        break

                    data = Authenticate.login()

                if data:
                    assign_menu(data)
            case '2':
                print('\n----SignUp----\n')
                try:
                    username = Authenticate.signup()
                except LoginError as e:
                    print(e)
                    continue

                print('Redirecting...')
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
                data = UserController.get_all_users_by_role('admin')

                if not data:
                    print('\nNo Admins Currently, Please Create One!\n')
                    continue

                print('\n-----List of Admins-----\n')
                display.pretty_print(
                    data=data, 
                    headers=['Username', 'Name', 'Email', 'Registration Date']
                )

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
                data = UserController.get_all_users_by_role('user')

                if not data:
                    print('\nNo Users Currently!\n')
                    continue

                print('\n-----List of Users-----\n')
                display.pretty_print(data=data, headers=['Username', 'Name', 'Email', 'Registration Date'])
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

                if not data:
                    print('\nNo Categories Currently, Please add a Category!!\n')
                    continue

                print('\n-----Quiz Categories-----\n')
                display.pretty_print(data=data, headers=['Category', 'Created By'])
            case '2':
                data = QuizController.get_all_questions()

                if not data:
                    print('\nNo Questions Currently, Please add a question!!\n')
                    continue

                print('\n-----Quiz Questions-----\n')
                display.pretty_print(data=data, headers=['Category', 'Question', 'Question Type', 'Answer', 'Created By'])
            case '3':
                try:
                    QuizController.create_category(username)
                except DuplicateEntryError as e:
                    print(e)
                    continue
            case '4':
                try:
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

    check_first_login(username, is_password_changed)

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


def check_first_login(username: str, is_password_changed: int):
    '''Checks Admin's First Login'''

    if not is_password_changed:
        logger.debug('Changing Default Admin Password')
        print('\nPlease change your password...\n')

        new_password = maskpass.askpass(prompt='Enter New Password: ', mask='*')
        confirm_password = ''

        while True:
            confirm_password =  maskpass.askpass(prompt='Confirm Password: ', mask='*')
            if new_password != confirm_password:
                print('Password does not match. Please enter your password again!\n')
            else:
                break

        hashed_password = hashlib.sha256(confirm_password.encode('utf-8')).hexdigest()
        is_password_changed = 1

        DAO.write_to_database(
            Queries.UPDATE_ADMIN_PASSWORD,
            (hashed_password, is_password_changed, username)
        )

        logger.debug('Default Admin Password Changed')
        print('\nPassword changed successfully!\n')


def user_menu(username: str):
    '''Menu for User'''

    logger.debug('Running User Menu')
    print('\n----User Dashboard----\n')
    print(f'\n----Welcome {username.upper()}----\n')

    while True:
        user_choice = input(prompts.USER_PROMPTS)

        match user_choice:
            case '1':
                print('\n-----Quiz Starting-----\n')

                data = QuizController.get_all_categories()
                categories = [(tup[0], ) for tup in data]
                display.show_categories(data=categories, header=['Categories'])

                category = validations.validate_name(prompt='Select Quiz Category: ')

                for data in data:
                    if data[0] == category:
                        break
                else:
                    print('No such Category! Please choose from above!!')
                    continue

                QuizController.start_quiz(category, username)
            case '2':
                data = QuizController.get_leaderboard()

                if not data:
                    print('\nNo data! Take a Quiz...\n')
                    continue

                print('\n-----Leaderboard-----\n')
                display.pretty_print(data=data, headers=['Username', 'Score', 'Time'])
            case '3':
                data = UserController.get_user_scores_by_username(username)

                if not data:
                    print('\nNo data! Take a Quiz...\n')
                    continue

                print('\n-----Score History-----\n')
                display.pretty_print(data, ['Time', 'Score'])

                scores = [scores[1] for scores in data]
                print(f'\nHighest Score: {max(scores)}\n')
            case 'q':
                break
            case _:
                print('Wrong input! Please choose from the above given options...')
