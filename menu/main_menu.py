'''
    Main Menu: assign_menu(), start()
'''

import logging
from constants import prompts
from controllers.auth_controller import Authenticate
from utils.custom_error import LoginError
from menu.admin_menu import AdminMenu
from menu.super_admin_menu import SuperAdminMenu
from menu.user_menu import UserMenu


logger = logging.getLogger(__name__)


class App:
    '''Contains methods to assign menu and start the application'''

    @staticmethod
    def assign_menu(data):
        '''Assign menu according to the role'''

        logger.debug('Assigning menu according to the role')
        username, role, is_password_changed = data

        match role:
            case 'super admin':
                SuperAdminMenu.super_admin_menu(username)
            case 'admin':
                AdminMenu.admin_menu(username, is_password_changed)
            case 'user':
                UserMenu.user_menu(username)
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
                case '2':
                    print('\n----SignUp----\n')
                    try:
                        username = Authenticate.signup()
                    except LoginError as e:
                        print(e)
                        continue

                    print('Redirecting...')
                    UserMenu.user_menu(username)
                case 'q':
                    break
                case _:
                    print('Wrong input! Please choose from the above given options...')
