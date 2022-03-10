""" Cryptography project VUT FEKT 2022 
Authors: 
    Thao Le
    Jakub Sencak
    Pavel Podluzansky
    Anh Phan
"""

import argparse
import logging
import time
import datetime
from pynewhope import newhope

class KRYException(Exception):
    """ Neat way of printing and logging exceptions """
    def __init__(self, message):
        """ docstring """
        super(KRYException, self).__init__()
        print(message)
        logging.info(message)

class OptionException(KRYException):
    """ child """
    pass

def loglogging():
    """ Initializes all logging  """
    time_struct = time.localtime()
    # log/dateTtime.log
    log_filename = f"log/{datetime.datetime.now().isoformat().split('.')[0]}.log"

    logging.basicConfig(filename=log_filename, encoding='utf-8', level=logging.DEBUG)
    # logging.debug('This message should go to the log file')
    # logging.info('So should this')
    # logging.warning('And this, too')
    # logging.error('And non-ASCII stuff, too, like Øresund and Malmö')

def main():
    parser = argparse.ArgumentParser(
                prog='kry.py',
                formatter_class=argparse.RawDescriptionHelpFormatter,
                epilog="KRY 2022 project - cypher/decypher or sign a file.")
    parser.add_argument("-c", "--cypher", action="store_true", help="cypher")
    parser.add_argument("-d", "--decypher", action="store_true", help="decypher")
    parser.add_argument("-a", "--algorithm", type=str, help="algorithm")
    parser.add_argument("-s", "--sign", type=str, help="signing")
    parser.add_argument("file", type=str, help="Filename")

    args = parser.parse_args()
    print(args)
    print(args.file)

    if args.decypher and args.cypher:
        raise OptionException("Wrong arguments given.")

    if args.file:
        pass
    out_filename = f"cyphered/{args.file}"



    print("Git check")





    return 0

if __name__ == '__main__':
    loglogging()
    try:
        main()
    except OptionException:
        pass
    finally:
        print("THE END")