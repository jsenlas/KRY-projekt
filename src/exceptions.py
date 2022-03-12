import logging

class KRYException(Exception):
    """ Neat way of printing and logging exceptions """
    def __init__(self, message):
        """ docstring """
        super().__init__()
        print(message)
        logging.info(message)


class OptionException(KRYException):
    """ child """
    pass