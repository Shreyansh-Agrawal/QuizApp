'''Entry point of the application'''

import logging
from utils.menu import start
from utils.initialize_app import Initializer
from utils import json_to_db_loader


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)-d] %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    level=logging.DEBUG,
    filename='logs.log'
)

logger = logging.getLogger(__name__)

logger.debug('app.py running')

Initializer.initialize_app()
json_to_db_loader.load_questions_from_json()
start()

logger.debug('Stopping Application')
print('\n---------END OF APP---------\n')
