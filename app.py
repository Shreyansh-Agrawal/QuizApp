'''
    Entry point of the application
'''

import logging
from initialize_app import Initializer
from utils.menu import App

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)-d] %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    level=logging.DEBUG,
    filename='logs.txt'
)

logger = logging.getLogger(__name__)

logger.debug('app.py running')

Initializer.initialize_app()
App.start()

logger.debug('Stopping application')
print('---------END OF APP---------')
