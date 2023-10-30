'''
    Menu functions for Admin
'''

import hashlib
import logging

import maskpass
from tabulate import tabulate

from controllers.user_controller import UserController
from controllers.quiz_controller import QuizController
from constants.queries import Queries
from constants import prompts
from database.database_access import DatabaseAccess as DAO


logger = logging.getLogger(__name__)


class AdminMenu:
    '''Methods for admin operation'''

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
                    AdminMenu.manage_users_menu()
                case '2':
                    print('\n----Manage Quizes----\n')
                    AdminMenu.manage_quizzes_menu(username)
                case 'q':
                    break
                case _:
                    print('Wrong input! Please choose from the above given options...')
