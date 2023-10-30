'''
    Menu functions for Super Admin
'''

import logging
from tabulate import tabulate
from controllers.user_controller import UserController
from constants import prompts
from utils.custom_error import LoginError


logger = logging.getLogger(__name__)


class SuperAdminMenu:
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
