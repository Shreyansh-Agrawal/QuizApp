'''
    Handlers for Quiz Operations
'''

import logging
from typing import List, Tuple
from datetime import datetime, timezone

import shortuuid
from tabulate import tabulate

from database.database_access import DatabaseAccess as DAO
from database.queries import Queries
from models.quiz import Category, Question, Option


logger = logging.getLogger(__name__)


class QuizController:
    '''Quiz Controller Class'''

    @staticmethod
    def get_all_categories() -> List[Tuple]:
        '''Return all Quiz Categories'''

        data = DAO.read_from_database(Queries.GET_ALL_CATEGORIES)
        return data

    @staticmethod
    def get_all_questions() -> List[Tuple]:
        '''Return all quiz questions'''

        data = DAO.read_from_database(Queries.GET_ALL_QUESTIONS_DETAIL)
        return data

    @staticmethod
    def get_random_questions_by_category(category: str) -> List[Tuple]:
        '''Return random questions by category'''

        data = DAO.read_from_database(Queries.GET_RANDOM_QUESTIONS_BY_CATEGORY, (category, ))
        return data

    @staticmethod
    def get_leaderboard() -> List[Tuple]:
        '''Return top 10 scores for leaderboard'''

        data = DAO.read_from_database(Queries.GET_LEADERBOARD)
        return data

    @staticmethod
    def create_category(username: str):
        '''Add a Quiz Category'''

        admin_data = DAO.read_from_database(Queries.GET_USER_ID_BY_USERNAME, (username, ))
        admin_id = admin_data[0][0]

        data = QuizController.get_all_categories()

        logger.debug('Creating Category')
        print('\n-----Create a new Quiz Category-----\n')

        print(
            tabulate(
                data,
                headers={
                    'Category': 'category_name', 
                    'Created By': 'admin_username', 
                },
                tablefmt='rounded_outline'
            )
        )

        category_data = {}
        category_data['admin_id'] = admin_id
        category_data['admin_username'] = username
        category_data['category_name'] = input('Enter New Category Name: ').title()

        category = Category(category_data)

        category.save_to_database()

        logger.debug('Category Created')
        print('\nCategory Created!\n')

    @staticmethod
    def create_question(username: str):
        '''Add Questions in a Category'''

        data = QuizController.get_all_categories()
        if not data:
            print('\nNo Categories Currently, Please add a Category!!\n')
            return

        logger.debug('Creating Question')
        print('\n-----Create a new Quiz Question-----\n')

        print(
            tabulate(
                data,
                headers={
                    'Category': 'category_name', 
                    'Created By': 'admin_username', 
                },
                tablefmt='rounded_outline'
            )
        )

        category_name = input('\nEnter Category Name: ').title()

        for data in data:
            if data[0] == category_name:
                break
        else:
            print('No such Category! Please choose from above!!')
            return

        category_id = DAO.read_from_database(Queries.GET_CATEGORY_ID_BY_NAME, (category_name, ))
        admin_data = DAO.read_from_database(Queries.GET_USER_ID_BY_USERNAME, (username, ))
        admin_id = admin_data[0][0]

        question_data = {}
        question_data['category_id'] = category_id[0][0]
        question_data['admin_id'] = admin_id
        question_data['admin_username'] = username
        question_data['question_text'] = input('Enter Question Text: ').title()
        question_data['question_type'] = input('Enter Question Type (MCQ, T/F, ONE WORD): ').upper()

        question = Question(question_data)

        match question_data['question_type']:
            case 'MCQ':
                option_data = {}
                option_data['question_id'] = question.question_id
                option_data['option_text'] = input('Enter Answer: ').title()
                option_data['is_correct'] = 1
                option = Option(option_data)
                question.add_option(option)

                for _ in range(3):
                    option_data['question_id'] = question.question_id
                    option_data['option_text'] = input('Enter Other Option: ').title()
                    option_data['is_correct'] = 0
                    option = Option(option_data)
                    question.add_option(option)
            case 'T/F' | 'ONE WORD':
                option_data = {}
                option_data['question_id'] = question.question_id
                option_data['option_text'] = input('Enter Answer: ').title()
                option_data['is_correct'] = 1

                option = Option(option_data)
                question.add_option(option)
            case _:
                print('Invalid Type!')
                return

        question.save_to_database()

        logger.debug('Question Created')
        print('\nQuestion Created!\n')

    @staticmethod
    def start_quiz(category: str, username: str):
        '''Start a New Quiz'''

        data = QuizController.get_random_questions_by_category(category)
        score = 0

        for question_data in data:
            correct_answer = QuizController.display_question(question_data)

            user_answer = input('Enter your answer: ')

            if user_answer.lower() == correct_answer.lower():
                score += 10

        print(f'\nYou Scored: {score}')
        QuizController.save_quiz_score(username, score)

    @staticmethod
    def display_question(question_data: Tuple) -> str:
        '''Display question and its options to user'''

        question, question_type, correct_answer = question_data
        print(f'\n{question}')

        if question_type == 'mcq':
            # todo: display options
            pass

        return correct_answer

    @staticmethod
    def save_quiz_score(username: str, score: int):
        '''Saving User's Quiz Score'''

        user_data = DAO.read_from_database(Queries.GET_USER_ID_BY_USERNAME, (username, ))
        user_id = user_data[0][0]
        score_id = 'S' + shortuuid.ShortUUID().random(length=5)

        time = datetime.now(timezone.utc) # current utc time
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S') # yyyy-mm-dd

        DAO.write_to_database(Queries.INSERT_USER_QUIZ_SCORE, (score_id, user_id, score, timestamp))
