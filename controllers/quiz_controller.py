'''Controllers for Operations related to Quiz'''

from datetime import datetime, timezone
import logging
import sqlite3
from typing import List, Tuple, Dict

import shortuuid

from database.database_access import DatabaseAccess as DAO
from constants import prompts
from constants.queries import Queries
from models.quiz import Category, Question, Option
from utils import validations
from utils.custom_error import DuplicateEntryError, DataNotFoundError


logger = logging.getLogger(__name__)

def get_all_categories() -> List[Tuple]:
    '''Return all Quiz Categories'''

    data = DAO.read_from_database(Queries.GET_ALL_CATEGORIES)
    return data


def get_all_questions() -> List[Tuple]:
    '''Return all quiz questions'''

    data = DAO.read_from_database(Queries.GET_ALL_QUESTIONS_DETAIL)
    return data


def get_random_questions_by_category(category: str) -> List[Tuple]:
    '''Return random questions by category'''

    data = DAO.read_from_database(Queries.GET_RANDOM_QUESTIONS_BY_CATEGORY, (category, ))
    return data


def get_leaderboard() -> List[Tuple]:
    '''Return top 10 scores for leaderboard'''

    data = DAO.read_from_database(Queries.GET_LEADERBOARD)
    return data


def create_category(username: str):
    '''Add a Quiz Category'''

    admin_data = DAO.read_from_database(Queries.GET_USER_ID_BY_USERNAME, (username, ))
    admin_id = admin_data[0][0]

    logger.debug('Creating Category')
    print('\n-----Create a new Quiz Category-----\n')

    category_data = {}
    category_data['admin_id'] = admin_id
    category_data['admin_username'] = username
    category_data['category_name'] = validations.validate_name(prompt='Enter New Category Name: ')

    category = Category(category_data)

    try:
        category.save_to_database()
    except sqlite3.IntegrityError as e:
        raise DuplicateEntryError('\nCategory already exists!') from e 

    logger.debug('Category Created')
    print('\nCategory Created!\n')


def create_question(username: str):
    '''Add Questions in a Category'''

    categories = get_all_categories()

    logger.debug('Creating Question')
    print('\n-----Create a new Quiz Question-----\n')

    user_choice = validations.validate_numeric_input(prompt='Choose a Category: ')
    if user_choice > len(categories) or user_choice-1 < 0:
        print('No such Category! Please choose from above!!')
        return

    category_name = categories[user_choice-1][0]

    for data in categories:
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
    question_data['question_text'] = validations.validate_question_text(prompt='Enter Question Text: ')

    question = create_option(question_data)

    try:
        question.save_to_database()
    except sqlite3.IntegrityError as e:
        raise DuplicateEntryError('Question already exists!') from e

    logger.debug('Question Created')
    print('\nQuestion Created!\n')


def create_option(question_data: Dict):
    '''Create options, returns a question object'''

    while True:
        question_type_input = input(prompts.QUESTION_TYPE_PROMPTS)
        match question_type_input:
            case '1':
                question_data['question_type'] = 'MCQ'
                break
            case '2':
                question_data['question_type'] = 'T/F'
                break
            case '3':
                question_data['question_type'] = 'ONE WORD'
                break
            case _:
                print('Invalid Question Type! Please choose from above!!')
                continue

    question = Question(question_data)

    match question_data['question_type']:
        case 'MCQ':
            option_data = {}
            option_data['question_id'] = question.question_id
            option_data['option_text'] = validations.validate_option_text('Enter Answer: ')
            option_data['is_correct'] = 1
            option = Option(option_data)
            question.add_option(option)

            for _ in range(3):
                option_data['question_id'] = question.question_id
                option_data['option_text'] = validations.validate_option_text('Enter Other Option: ')
                option_data['is_correct'] = 0
                option = Option(option_data)
                question.add_option(option)
        case 'T/F' | 'ONE WORD':
            option_data = {}
            option_data['question_id'] = question.question_id
            option_data['option_text'] = validations.validate_option_text('Enter Answer: ')
            option_data['is_correct'] = 1

            option = Option(option_data)
            question.add_option(option)
        case _:
            print('Invalid Type!')
            return

    return question


def start_quiz(category: str, username: str):
    '''Start a New Quiz'''

    data = get_random_questions_by_category(category)
    # if len(data) < 10:
    #     raise DataNotFoundError('Not enough questions! Please try some other category...')

    score = 0

    for question_data in data:
        question_id, question_text, question_type, correct_answer = question_data
        options_data = DAO.read_from_database(Queries.GET_OPTIONS_FOR_MCQ, (question_id, ))

        display_question(question_text, question_type, options_data)

        user_answer = get_user_response(question_type)

        if question_type.lower() == 'mcq':
            user_answer = options_data[user_answer-1][0]

        if user_answer.lower() == correct_answer.lower():
            score += 10

    print(f'\nYou Scored: {score}')
    save_quiz_score(username, score)


def display_question(question: str, question_type: str, options_data: List[Tuple]):
    '''Display question and its options to user'''

    print(f'\n{question}')

    if question_type.lower() == 'mcq':
        options = [option[0] for option in options_data]

        for count, option in enumerate(options, 1):
            print(f'{count}. {option}')

    elif question_type.lower() == 't/f':
        print('1. True\n2. False')


def get_user_response(question_type: str) -> str:
    '''Gets user response'''

    if question_type.lower() == 'mcq':
        while True:
            user_choice = validations.validate_numeric_input(prompt='Choose an option: ')
            if user_choice not in range(1, 5):
                print('Please enter a number from 1 to 4: ')
                continue
            return user_choice

    elif question_type.lower() == 't/f':
        while True:
            user_choice = validations.validate_numeric_input(prompt='Choose an option: ')
            match user_choice:
                case 1:
                    return 'true'
                case 2:
                    return 'false'
                case _:
                    print('Please enter either 1 or 2...')
    else:
        user_answer = validations.validate_option_text('Enter your answer: ')
        return user_answer


def save_quiz_score(username: str, score: int):
    '''Saving User's Quiz Score'''

    user_data = DAO.read_from_database(Queries.GET_USER_ID_BY_USERNAME, (username, ))
    user_id = user_data[0][0]
    score_id = 'S' + shortuuid.ShortUUID().random(length=5)

    time = datetime.now(timezone.utc) # current utc time
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S') # yyyy-mm-dd

    DAO.write_to_database(Queries.INSERT_USER_QUIZ_SCORE, (score_id, user_id, score, timestamp))
