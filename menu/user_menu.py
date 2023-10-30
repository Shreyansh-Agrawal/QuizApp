'''
    Menu functions for User
'''

import logging
from tabulate import tabulate
from controllers.user_controller import UserController
from controllers.quiz_controller import QuizController
from constants import prompts
from utils import validations
from utils.pretty_print import pretty_print

logger = logging.getLogger(__name__)


class UserMenu:
    '''Menu class to assign menu'''

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
                    pretty_print(data, {'Time': 'timestamp', 'Score': 'score'})
                case 'q':
                    break
                case _:
                    print('Wrong input! Please choose from the above given options...')
