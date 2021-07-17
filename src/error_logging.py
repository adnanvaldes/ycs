import sys
from datetime import datetime, timedelta

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

def rounded_time():
    d = datetime.utcnow()
    return datetime.utcnow() - timedelta(microseconds=d.microsecond)

def error_log(func, err):
    sys.stderr.write(f"{rounded_time()} - ERROR - {err}")

def debug_log(func):
    sys.stdout.write(f"{rounded_time()} - DEBUG - {func.__name__} success.")

def info_log(func):
    sys.stdout.write(f"{rounded_time()} - DEBUG - {func.__name__} starting... \n")

def output_log(func, output):
    sys.stdout.write(f"\n{rounded_time()} - OUTPUT - {func.__name__}: \n{output} \n")