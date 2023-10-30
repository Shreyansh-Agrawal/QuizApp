'''
    Functions to load data to database from json file
'''

import json
from database.database_access import DatabaseAccess as DAO
from constants.queries import Queries


class LoadData:
    '''Contains method to load data to db'''

    @staticmethod
    def load_questions_from_json():
        '''Function to load data to db from json'''

        with open('utils\\data.json', 'r', encoding="utf-8") as file:
            data = json.load(file)

        for question in data['questions']:
            question_id = question['question_id']
            question_text = question['question_text']
            question_type = question['question_type']
            category_id = question['category_id']
            category = question['category']
            admin_id = question['admin_id']
            admin_username = question['admin_username']
            answer_id = question['options']['answer']['option_id']
            answer = question['options']['answer']['text']

            try:
                DAO.write_to_database(
                    Queries.INSERT_CATEGORY,
                    (category_id, admin_id, admin_username, category))
            except Exception:
                pass

            try:
                DAO.write_to_database(
                    Queries.INSERT_QUESTION,
                    (question_id, category_id, admin_id, admin_username, question_text, question_type))
            except Exception:
                pass

            try:
                DAO.write_to_database(
                    Queries.INSERT_OPTION,
                    (answer_id, question_id, answer, 1))

                if question_type == 'mcq':
                    for i in range(3):
                        other_option_id = question['options']['other_options'][i]['option_id']
                        other_option = question['options']['other_options'][i]['text']

                        DAO.write_to_database(
                            Queries.INSERT_OPTION,
                            (other_option_id, question_id, other_option, 0))
            except Exception:
                pass
