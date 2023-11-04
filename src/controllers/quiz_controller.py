'''Controllers for Operations related to Quiz'''

import logging
import sqlite3
from datetime import datetime, timezone
from typing import Dict, List, Tuple

from config import prompts
from config.display_prompts import DisplayPrompts
from config.queries import Queries
from database.database_access import DatabaseAccess as DAO
from models.quiz import Category, Option, Question
from utils import validations
from utils.custom_error import DataNotFoundError, DuplicateEntryError

logger = logging.getLogger(__name__)


def get_all_categories() -> List[Tuple]:
    '''Return all Quiz Categories'''

    data = DAO.read_from_database(Queries.GET_ALL_CATEGORIES)
    return data


def get_all_questions() -> List[Tuple]:
    '''Return all quiz questions'''

    data = DAO.read_from_database(Queries.GET_ALL_QUESTIONS_DETAIL)
    return data


def get_questions_by_category() -> List[Tuple]:
    '''Return quiz questions by category'''

    categories = get_all_categories()

    logger.debug('Get Questions by Category')

    user_choice = validations.validate_numeric_input(prompt='Choose a Category: ')
    if user_choice > len(categories) or user_choice-1 < 0:
        raise DataNotFoundError('No such Category! Please choose from above!!')

    category_name = categories[user_choice-1][0]

    print(DisplayPrompts.DISPLAY_QUES_IN_A_CATEGORY_MSG.format(name=category_name))

    data = DAO.read_from_database(Queries.GET_QUESTIONS_BY_CATEGORY, (category_name, ))
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
    print(DisplayPrompts.CREATE_CATEGORY_MSG)

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
    print(DisplayPrompts.CREATE_CATEGORY_SUCCESS_MSG)


def create_question(username: str):
    '''Add Questions in a Category'''

    categories = get_all_categories()

    logger.debug('Creating Question')
    print(DisplayPrompts.CREATE_QUES_MSG)

    user_choice = validations.validate_numeric_input(prompt='Choose a Category: ')
    if user_choice > len(categories) or user_choice-1 < 0:
        raise DataNotFoundError('No such Category! Please choose from above!!')

    category_name = categories[user_choice-1][0]

    category_id = DAO.read_from_database(Queries.GET_CATEGORY_ID_BY_NAME, (category_name, ))
    admin_data = DAO.read_from_database(Queries.GET_USER_ID_BY_USERNAME, (username, ))
    admin_id = admin_data[0][0]

    question_data = {}
    question_data['category_id'] = category_id[0][0]
    question_data['admin_id'] = admin_id
    question_data['admin_username'] = username
    question_data['question_text'] = validations.validate_question_text(
                                                    prompt='Enter Question Text: '
                                                )

    question = create_option(question_data)

    try:
        question.save_to_database()
    except sqlite3.IntegrityError as e:
        raise DuplicateEntryError('Question already exists!') from e

    logger.debug('Question Created')
    print(DisplayPrompts.CREATE_QUES_SUCCESS_MSG)


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
                print(DisplayPrompts.INVALID_QUES_TYPE_MSG)
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
                option_data['option_text'] = validations.validate_option_text(
                                                            'Enter Other Option: '
                                                        )
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
            logger.exception('Invalid Ques Type!')
            return None

    return question


def update_category_by_name():
    '''Update a category by category name'''

    categories = get_all_categories()

    logger.debug('Updating a Category')
    print(DisplayPrompts.UPDATE_CATEGORY_MSG)

    user_choice = validations.validate_numeric_input(prompt='Choose a Category: ')
    if user_choice > len(categories) or user_choice-1 < 0:
        raise DataNotFoundError('No such Category! Please choose from above!!')

    category_name = categories[user_choice-1][0]
    new_category_name = validations.validate_name('Enter updated category name: ')
    DAO.write_to_database(Queries.UPDATE_CATEGORY_BY_NAME, (new_category_name, category_name))

    logger.debug('Category %s updated to %s', category_name, new_category_name)
    print(DisplayPrompts.UPDATE_CATEGORY_SUCCESS_MSG.format(name=category_name, new_name=new_category_name))


def delete_category_by_name():
    '''Delete a category by category name'''

    categories = get_all_categories()

    logger.debug('Deleting a Category')
    print(DisplayPrompts.DELETE_CATEGORY_MSG)

    user_choice = validations.validate_numeric_input(prompt='Choose a Category: ')
    if user_choice > len(categories) or user_choice-1 < 0:
        raise DataNotFoundError('No such Category! Please choose from above!!')

    category_name = categories[user_choice-1][0]

    while True:
        print(DisplayPrompts.DELETE_CATEGORY_WARNING_MSG.format(name=category_name))
        confirmation = input('Type "YES" if you wish to continue\nPress any other key to go back: ')
        if confirmation.lower() == 'yes':
            break
        return

    logger.warning('Deleting the Category: %s', category_name)
    DAO.write_to_database(Queries.DELETE_CATEGORY_BY_NAME, (category_name, ))

    logger.debug('Category %s deleted', category_name)
    print(DisplayPrompts.DELETE_CATEGORY_SUCCESS_MSG.format(name=category_name))


def start_quiz(category: str, username: str):
    '''Start a New Quiz'''

    logger.debug('Stating Quiz for %s: ', username)
    data = get_random_questions_by_category(category)
    if len(data) < 10:
        raise DataNotFoundError('Not enough questions! Please try some other category...')

    score = 0
    # Display question, take user's response and calculate score one by one
    for question_no, question_data in enumerate(data, 1):
        question_id, question_text, question_type, correct_answer = question_data
        options_data = DAO.read_from_database(Queries.GET_OPTIONS_FOR_MCQ, (question_id, ))
        display_question(question_no, question_text, question_type, options_data)

        user_answer = get_user_response(question_type)

        if question_type.lower() == 'mcq':
            user_answer = options_data[user_answer-1][0]

        if user_answer.lower() == correct_answer.lower():
            score += 10

    print(DisplayPrompts.DISPLAY_SCORE_MSG.format(score=score))
    save_quiz_score(username, score)
    logger.debug('Quiz Completed for %s: ', username)


def display_question(question_no: int, question: str, question_type: str, options_data: List[Tuple]):
    '''Display question and its options to user'''

    print(f'\n{question_no}. {question}')

    if question_type.lower() == 'mcq':
        options = [option[0] for option in options_data]

        for count, option in enumerate(options, 1):
            print(f'{count}. {option}')

    elif question_type.lower() == 't/f':
        print(DisplayPrompts.TF_OPTION_MSG)


def get_user_response(question_type: str) -> str:
    '''Gets user response according to question type'''

    if question_type.lower() == 'mcq':
        while True:
            user_choice = validations.validate_numeric_input(prompt='Choose an option: ')
            if user_choice not in range(1, 5):
                print(DisplayPrompts.MCQ_WRONG_OPTION_MSG)
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
                    print(DisplayPrompts.TF_WRONG_OPTION_MSG)
    else:
        user_answer = validations.validate_option_text('-> Enter your answer: ')
        return user_answer


def save_quiz_score(username: str, score: int):
    '''Saving User's Quiz Score'''

    logger.debug('Saving score for %s: ', username)
    user_data = DAO.read_from_database(Queries.GET_USER_ID_BY_USERNAME, (username, ))
    user_id = user_data[0][0]
    score_id = validations.validate_id(entity='score')

    time = datetime.now(timezone.utc) # current utc time
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S') # yyyy-mm-dd

    DAO.write_to_database(Queries.INSERT_USER_QUIZ_SCORE, (score_id, user_id, score, timestamp))
    logger.debug('Score saved for %s: ', username)
