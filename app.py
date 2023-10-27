'''
    Entry point of the application
'''

from initialize_app import Initializer
from utils.loggers.logger import Logger


print("\n---------WELCOME TO QUIZ APP---------\n")
Logger.logger.debug("app.py running")

Initializer.initialize_app()

Logger.logger.debug("Initialization Complete")
print("\nInitialization Complete!\n")
