'''
    Entry point of the application
'''

import logging

from initialize_app import Initializer


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    level=logging.DEBUG,
    filename='logs.txt'
)

logger = logging.getLogger(__name__)

print("\n---------WELCOME TO QUIZ APP---------\n")
logger.debug("app.py running")

Initializer.initialize_app()

logger.debug("Initialization Complete")
print("\nInitialization Complete!\n")
