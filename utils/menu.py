'''
    Assign menu as per the role
'''

import hashlib
import logging

import maskpass
from tabulate import tabulate

from controllers.auth_controller import Authenticate
from controllers.user_controller import UserController
from controllers.quiz_controller import QuizController
from database.database_access import DatabaseAccess as DAO
from database.queries import Queries
from utils import prompts


logger = logging.getLogger(__name__)


class Menu:
    '''Menu class to assign menu'''

    @staticmethod
    def super_admin_menu(username: str):
        '''Menu for Super Admin'''

        logger.debug('Running Super Admin Menu')
        print('----Super Admin Dashboard----')
        print(f'\n----Welcome {username.upper()}----\n')

        while True:
            user_choice = input(prompts.SUPER_ADMIN_PROMPTS)

            match user_choice:
                case '1':
                    UserController.create_admin()
                case '2':
                    data = UserController.get_all_users_by_role('admin')

                    if not data:
                        print('\nNo Admins Currently, Please Create One!\n')
                        continue

                    print('\n-----List of Admins-----\n')
                    print(
                        tabulate(
                            data,
                            headers={
                                'Username': 'username', 
                                'Name': 'name', 
                                'Email': 'email', 
                                'Registration Date': 'registration_date'
                            },
                            tablefmt='rounded_outline'
                        )
                    )
                case '3':
                    UserController.delete_user_by_email('admin')
                case 'q':
                    break
                case _:
                    print('Wrong input! Please choose from the above given options...')

    @staticmethod
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
                    print(
                        tabulate(
                            data,
                            headers={
                                'Username': 'username', 
                                'Name': 'name', 
                                'Email': 'email', 
                                'Registration Date': 'registration_date'
                            },
                            tablefmt='rounded_outline'
                        )
                    )
                case '2':
                    UserController.delete_user_by_email('user')
                case 'q':
                    break
                case _:
                    print('Wrong input! Please choose from the above given options...')

    @staticmethod
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
                    print(
                        tabulate(
                            data,
                            headers={
                                'Category': 'category_name', 
                                'Created By': 'admin_name', 
                            },
                            tablefmt='rounded_outline'
                        )
                    )
                case '2':
                    data = QuizController.get_all_questions()

                    if not data:
                        print('\nNo Questions Currently, Please add a question!!\n')
                        continue

                    print('\n-----Quiz Questions-----\n')
                    print(
                        tabulate(
                            data,
                            headers={
                                'Category': 'category_name',
                                'Question': 'question_text',
                                'Question Type': 'question_type',
                                'Answer': 'option_text',
                                'Created By': 'questions.admin_name',
                            },
                            tablefmt='rounded_outline'
                        )
                    )
                case '3':
                    QuizController.create_category(username)
                case '4':
                    QuizController.create_question(username)
                case 'q':
                    break
                case _:
                    print('Wrong input! Please choose from the above given options...')

    @staticmethod
    def admin_menu(username: str, is_password_changed: int):
        '''Menu for Admin'''

        logger.debug('Running Admin Menu')
        print('----Admin Dashboard----')
        print(f'\n----Welcome {username.upper()}----\n')

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

        while True:
            user_choice = input(prompts.ADMIN_PROMPTS)

            match user_choice:
                case '1':
                    print('\n----Manage Users----\n')
                    Menu.manage_users_menu()
                case '2':
                    print('\n----Manage Quizes----\n')
                    Menu.manage_quizzes_menu(username)
                case 'q':
                    break
                case _:
                    print('Wrong input! Please choose from the above given options...')

    @staticmethod
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

                    if not data:
                        print('\nNo Categories Currently, Please add a Category!!\n')
                        continue

                    print('\n-----Quiz Categories-----\n')

                    categories = [(tup[0], ) for tup in data]
                    print(
                        tabulate(
                            categories,
                            headers={
                                'Categories': 'category_name',
                            },
                            tablefmt='rounded_outline'
                        )
                    )

                    category = input('Select Quiz Category: ').title()

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
                    print(
                        tabulate(
                            data,
                            headers={
                                'Username': 'username',
                                'Score': 'score',
                                'Time': 'timestamp',
                            },
                            tablefmt='rounded_outline'
                        )
                    )
                case '3':
                    data = UserController.get_user_scores_by_username(username)

                    if not data:
                        print('\nNo data! Take a Quiz...\n')
                        continue

                    print('\n-----Score History-----\n')
                    print(
                        tabulate(
                            data,
                            headers={
                                'Time': 'timestamp',
                                'Score': 'score',
                            },
                            tablefmt='rounded_outline'
                        )
                    )
                case 'q':
                    break
                case _:
                    print('Wrong input! Please choose from the above given options...')


class App:
    '''Contains methods to assign menu and start the application'''

    @staticmethod
    def assign_menu(data):
        '''Assign menu according to the role'''

        logger.debug('Assigning menu according to the role')
        username, role, is_password_changed = data

        match role:
            case 'super admin':
                Menu.super_admin_menu(username)
            case 'admin':
                Menu.admin_menu(username, is_password_changed)
            case 'user':
                Menu.user_menu(username)
            case _:
                print('Invalid Role!: ', role)

    @staticmethod
    def start():
        '''Menu for Login / Sign Up'''

        logger.debug('Running App.start()')
        print('\n---------WELCOME TO QUIZ APP---------\n')

        while True:
            user_choice = input(prompts.AUTH_PROMPTS)

            match user_choice:
                case '1':
                    print('\n----SignUp----\n')
                    username = Authenticate.signup()
                    print('Redirecting...')
                    Menu.user_menu(username)
                case '2':
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
                        App.assign_menu(data)
                case 'q':
                    break
                case _:
                    print('Wrong input! Please choose from the above given options...')
