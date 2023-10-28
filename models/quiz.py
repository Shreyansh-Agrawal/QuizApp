'''
    Contains classes for Quiz, Category, Question and Option
'''

from abc import ABC, abstractmethod
from typing import Dict

import shortuuid

from database.database_access import DatabaseAccess as DAO
from database.queries import Queries
from utils.custom_error import EmptyOptionListError


class QuizEntity(ABC):
    '''Abstract Base Class'''

    def __init__(self, text: str) -> None:
        self.text = text

    @abstractmethod
    def save_to_database(self) -> None:
        '''abstract method to add to database'''


class Category(QuizEntity):
    '''Category Class'''

    def __init__(self, category_data: Dict) -> None:
        super().__init__(category_data.get('category_name'))
        self.category_id = 'C' + shortuuid.ShortUUID().random(length=5)
        self.admin_id = category_data.get('admin_id')
        self.admin_name = category_data.get('admin_name')

    def save_to_database(self) -> None:
        '''method to add category to database'''

        category_data = (
            self.category_id,
            self.admin_id,
            self.admin_name,
            self.text
        )

        DAO.write_to_database(Queries.INSERT_CATEGORY, category_data)


class Option(QuizEntity):
    '''Option Class'''

    def __init__(self, option_data: Dict) -> None:
        super().__init__(option_data.get('option_text'))
        self.option_id = 'O' + shortuuid.ShortUUID().random(length=5)
        self.question_id = option_data.get('question_id')
        self.is_correct = option_data.get('is_correct')

    def save_to_database(self) -> None:
        '''method to add option to database'''

        option_data = (
            self.option_id,
            self.question_id,
            self.text,
            self.is_correct
        )

        DAO.write_to_database(Queries.INSERT_OPTION, option_data)


class Question(QuizEntity):
    '''Question Class'''

    def __init__(self, question_data: Dict) -> None:
        super().__init__(question_data.get('question_text'))
        self.question_id = 'Q' + shortuuid.ShortUUID().random(length=5)
        self.category_id = question_data.get('category_id')
        self.admin_id = question_data.get('admin_id')
        self.admin_name = question_data.get('admin_name')
        self.question_type = question_data.get('question_type')
        self.options = []

    def add_option(self, option: Option) -> None:
        '''method to add option objects'''

        self.options.append(option)

    def save_to_database(self) -> None:
        '''method to add question and its option to database'''

        question_data = (
            self.question_id,
            self.category_id,
            self.admin_id,
            self.admin_name,
            self.text,
            self.question_type
        )

        if not self.options:
            raise EmptyOptionListError("No Options added for this Question!")

        DAO.write_to_database(Queries.INSERT_QUESTION, question_data)

        for option in self.options:
            option.save_to_database()
