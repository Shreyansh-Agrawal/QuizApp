'''Entry point of the application'''

import logging
from utils.menu import start
from utils.initialize_app import Initializer


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)-d] %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    level=logging.DEBUG,
    filename='logs.log'
)

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.debug('app.py running')

    Initializer.initialize_app()
    start()

    logger.debug('Stopping Application')
    print('\n---------END OF APP---------\n')

# todo: fix view all questions and view questions by category