import logging

def logger(func):
    def inner(*args, **kwargs):
        log = logging.getLogger(__name__)
        log.info(f"Starting {func.__name__}")

        result = func(*args, **kwargs)

        log.info(f"Ending {func.__name__}")
        return result
    return inner
