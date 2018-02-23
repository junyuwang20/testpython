import logging
import logging.handlers


class SimpleLogging(object):
    def __init__(self):
        logger = logging.getLogger('simple_log')

        formater = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')

        file_handler = logging.handlers.TimedRotatingFileHandler(filename, when='D', interval=1)
        file_handler.setFormatter(formater)

        screen_handler =logging.StreamHandler()
        screen_handler.setFormatter(formater)

        logger.addHandler(file_handler)
        logger.addHandler(screen_handler)
