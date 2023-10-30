'''
    Entry point of the application
'''

import logging
from utils.initialize_app import Initializer
from utils.menu import App
from utils.json_to_db_loader import LoadData


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)-d] %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    level=logging.DEBUG,
    filename='logs.txt'
)

logger = logging.getLogger(__name__)

logger.debug('app.py running')

Initializer.initialize_app()
LoadData.load_questions_from_json()
App.start()

logger.debug('Stopping Application')
print('\n---------END OF APP---------\n')
