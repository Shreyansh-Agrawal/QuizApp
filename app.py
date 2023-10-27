'''
    Entry point of the application
'''

import logging
import time
# from initialize_app import Initializer
from controllers.auth_controller import Authenticate
from utils import prompts
from utils.menu import Menu


ATTEMPT_LIMIT = 3

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)-20d] %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    level=logging.DEBUG,
    filename='logs.txt'
)

logger = logging.getLogger(__name__)

print('\n---------WELCOME TO QUIZ APP---------\n')
logger.debug('app.py running')

# Initializer.initialize_app()

while True:
    user_choice = input(prompts.AUTH_PROMPTS)

    match user_choice:
        case '1':
            print('\n----SignUp----\n')
            username = Authenticate.signup()
            Menu.user_menu(username)
        case '2':
            print('\n----Login----\n')
            attempts_remaining = ATTEMPT_LIMIT

            data = Authenticate.login()
            while not data:
                attempts_remaining -= 1
                print(f'Remaining attempts: {attempts_remaining}\n')

                if attempts_remaining == 0:
                    print('Account Not Found! Please Sign up!\n')
                    break

                data = Authenticate.login()

            if data:
                Menu.assign_menu(data)
        case 'q':
            break
        case _:
            print('Wrong input! Please choose from the above given options...')

print('---------END OF APP---------')
