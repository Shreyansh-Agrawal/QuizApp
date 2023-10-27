'''
    Entry point of the application
'''

from initialize_app import Initializer, InitializeDatabase
from utils.loggers.logger import Logger

print("\n---------WELCOME TO QUIZ APP---------\n")
Logger.logger.debug("app.py running")

InitializeDatabase.create_users_table()
InitializeDatabase.create_credentials_table()
InitializeDatabase.create_scores_table()
InitializeDatabase.create_categories_table()
InitializeDatabase.create_questions_table()
InitializeDatabase.create_options_table()
Initializer.create_super_admin()

Logger.logger.debug("Initialization Complete")
print("\nInitialization Complete!\n")
