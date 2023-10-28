'''
    Assign menu as per the role
'''
import logging
from tabulate import tabulate
from utils import prompts
from controllers.auth_controller import Authenticate
from controllers.super_admin_controller import SuperAdminController
from controllers.admin_controller import AdminController

logger = logging.getLogger(__name__)


class Menu:
    '''Menu class to assign menu'''

    @staticmethod
    def super_admin_menu(username: str):
        '''Menu for Super Admin'''

        logging.debug("Running Super Admin Menu")
        print('----Super Admin Dashboard----')
        print(f'\n----Welcome {username}----\n')

        while True:
            user_choice = input(prompts.SUPER_ADMIN_PROMPTS)

            match user_choice:
                case '1':
                    SuperAdminController.create_admin()
                case '2':
                    data = SuperAdminController.get_all_admins()

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
                    SuperAdminController.delete_admin()
                case 'q':
                    break
                case _:
                    print('Wrong input! Please choose from the above given options...')

    @staticmethod
    def manage_users_menu():
        '''Admin: manage users menu'''

        logging.debug("Running Admin: Manage Users Menu")
        while True:
            user_sub_choice = input(prompts.ADMIN_MANAGE_USER_PROMPTS)

            match user_sub_choice:
                case '1':
                    data = AdminController.get_all_users()

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
                    AdminController.delete_user()
                case 'q':
                    break
                case _:
                    print('Wrong input! Please choose from the above given options...')

    @staticmethod
    def manage_quizzes_menu(username: str):
        '''Admin: manage quizzes menu'''

        logging.debug("Running Admin: Manage Quizzes Menu")
        while True:
            user_sub_choice = input(prompts.ADMIN_MANAGE_QUIZZES_PROMPTS)

            match user_sub_choice:
                case '1':
                    data = AdminController.get_all_categories()

                    if not data:
                        print('\nNo Categories Currently, Please add a Category!!\n')
                        continue

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
                    data = AdminController.get_all_questions()

                    if not data:
                        print('\nNo Questions Currently, Please add a question!!\n')
                        continue

                    print(
                        tabulate(
                            data,
                            headers={
                                'Category': 'category_name',
                                'Question': 'question_text',
                                'Question Type': 'question_type',
                                'Created By': 'questions.admin_name',
                            },
                            tablefmt='rounded_outline'
                        )
                    )
                case '3':
                    AdminController.create_category(username)
                case '4':
                    AdminController.create_question(username)
                case 'q':
                    break
                case _:
                    print('Wrong input! Please choose from the above given options...')

    @staticmethod
    def admin_menu(username: str, is_password_changed: int):
        '''Menu for Admin'''

        logging.debug("Running Admin Menu")
        print('----Admin Dashboard----')
        print(f'\n----Welcome {username}----\n')

        if not is_password_changed:
            print('Please change your password')

        while True:
            user_choice = input(prompts.ADMIN_PROMPTS)

            match user_choice:
                case '1':
                    print("Managing users...")
                    Menu.manage_users_menu()
                case '2':
                    print("Managing quizzes...")
                    Menu.manage_quizzes_menu(username)
                case 'q':
                    break
                case _:
                    print('Wrong input! Please choose from the above given options...')

    @staticmethod
    def user_menu(username: str):
        '''Menu for User'''

        logging.debug("Running User Menu")
        print('\n----User Dashboard----\n')
        print(f'\n----Welcome {username}----\n')

        while True:
            user_choice = input(prompts.USER_PROMPTS)

            match user_choice:

                case '1':
                    print("Quiz Starting...")
                case '2':
                    print("Leaderboard...")
                case '3':
                    print("Your scores History...")
                case 'q':
                    break
                case _:
                    print('Wrong input! Please choose from the above given options...')


class App:
    '''Contains methods to assign menu and start the application'''

    @staticmethod
    def assign_menu(data):
        '''Assign menu according to the role'''

        logging.debug("Running Assign Menu")
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

        logging.debug("Running App.start()")
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
