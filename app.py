'''
    Entry point of the application
'''

import logging

# from initialize_app import Initializer
from controllers.auth_controller import Authenticate

USER_PROMPT = '''
1> Signup
2> Login
3> Quit

Enter your choice: '''

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    level=logging.DEBUG,
    filename='logs.txt'
)

logger = logging.getLogger(__name__)

print("\n---------WELCOME TO QUIZ APP---------\n")
logger.debug("app.py running")

# Initializer.initialize_app()

while True:
    user_choice = input(USER_PROMPT)

    match user_choice:
        case '1':
            print("----SignUp----")
            Authenticate.signup()
        case '2':
            print("----Login----")
            Authenticate.login()
        case '3':
            break
        case _:
            print("Wrong Choice!")

print("---------END OF APP---------")
