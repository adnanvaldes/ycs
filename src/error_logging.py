import logging
from logging.handlers import RotatingFileHandler

class StatusCode(Exception):
    """ Exception raised for status code NOT 200"""
    def __init__(self, status_code, message='Status code not 200. Returned: '):
        self.message = message + str(status_code)
        super().__init__(self.message)

class NoBulbs(Exception):
    def __init__(self, message="No bulbs found."):
        self.message = message
        super().__init__(self.message)


def docker_log():
    def decorate(func):
        def call(*args, **kwargs):
            try:
                info_log(func)
                result = func(*args, **kwargs)
                debug_log(func)
                output_log(func, result)
                return result
            except Exception as e:
                error_log(func, e)
                return
        return call
    return decorate



def error_log(func, err):
    logger.error(err)


def debug_log(func):
    logger.info(f'{func.__name__} finished.')


def info_log(func):
    logger.info(f"{func.__name__} starting...")


def output_log(func, output):
    logger.debug(f"OUTPUT - {func.__name__}: {output}")



# Custom logging

logFile = "/code"

logger = logging.getLogger('schedule')
logger.setLevel(level=logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
file_handler = RotatingFileHandler('ycs.log', maxBytes=10*1024*1024, backupCount=2)
file_handler.setLevel(logging.DEBUG)
log_format = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
stream_handler.setFormatter(log_format)
file_handler.setFormatter(log_format)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)