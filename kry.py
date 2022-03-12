""" Cryptography project VUT FEKT 2022
Authors:
    Thao Le
    Jakub Sencak
    Pavel Podluzansky
    Anh Phan
"""

import os
import argparse
import logging
import datetime
from src.hash_based_signature import PySPHINXplus
from src.exceptions import OptionException

def main(args, path):
    """ Main docstring """

    # Check combinations of arguments
    if args.decypher and args.cypher:
        raise OptionException("Wrong arguments given. Cypher and decypher cannot be used together.")

    if args.sign and args.verify:
        raise OptionException(
            "Wrong arguments given. Signing and verifying signature cannot be used together.")

    if args.sign == "SPHINXPLUS":  # Sign by SPHINX+
        logging.info("EVENT_TYPE: Signing")
        logging.info("Algorithm: SPHINX+")

        psx = PySPHINXplus(args.file)
        key, private_key, signature = psx.sign()

        with open(f"{path}/{args.file}.signature", "wb") as fp:
            logging.info("Saving signature to file...")
            fp.write(signature)

        # with open(f"{path}/{args.file}.pvkey", "wb") as fp:
        #     logging.info("Saving public key to file.")
        #     fp.write(private_key)

        with open(f"{path}/{args.file}.pbkey", "wb") as fp:
            logging.info("Saving public key to file...")
            fp.write(key)
        logging.info(f"Saved to {path}")

    elif args.verify == "SPHINXPLUS" and args.public_key and args.signature:
        logging.info("EVENT_TYPE: Verify")
        logging.info("Algorithm: SPHINX+")
        psx = PySPHINXplus(args.file)
        if psx.verify(args.signature, args.public_key):
            logging.info("Signature successfuly veriefied.")
            return
        logging.info("Signature verification UNSUCCESSFUL.")

    elif False:
        # TODO More algorithms :)
        pass
    else:
        raise OptionException("Wrong options, ending with no action...")


if __name__ == '__main__':
    start_time = datetime.datetime.now().isoformat().split('.')[0]

    """ Init argparse """
    parser = argparse.ArgumentParser(
                prog='kry.py',
                formatter_class=argparse.RawDescriptionHelpFormatter,
                epilog="KRY 2022 project - cypher/decypher or sign a file.")

    cypher_algorithm_list = [""]  # Here add name of your algorithm
    de_cypher_group = parser.add_argument_group('cypher/decypher files')
    de_cypher_group.add_argument("-c", "--cypher", choices=cypher_algorithm_list,
                                 action="store", help="Cypher a file", metavar="ALGORITHM")
    de_cypher_group.add_argument("-d", "--decypher", choices=cypher_algorithm_list,
                                 action="store", help="Decypher a file", metavar="ALGORITHM")

    signature_algorithm_list = ["SPHINXPLUS"]  # Here add name of your algorithm
    signature_group = parser.add_argument_group('Signing and verifying file signature')
    signature_group.add_argument("-s", "--sign", choices=signature_algorithm_list,
                    help="Signing, available options are SPHINXPLUS, ", metavar="ALGORITHM")
    signature_group.add_argument("-v", "--verify", choices=signature_algorithm_list,
                    help="Verify signature using algorithms - SPHINXPLUS, ", metavar="ALGORITHM")
    signature_group.add_argument("-k", "--public_key", action="store", help="File containing public key.")
    signature_group.add_argument("-n", "--signature", action="store", help="File containing signature.")
    signature_group.add_argument("--log", action="store_true",
                    help="Log to separate file in the generated directory.")
    parser.add_argument("file", type=str, help="Filename")

    argumnets = parser.parse_args()

    print(argumnets)  # for debug only

    """ Setup path """
    # "./out/filename_dir_date_time/filename.[log, signature, pbkey]"
    path = f"./out/{argumnets.file}_dir_{start_time.replace(':', '_')}"
    
    if not argumnets.verify:  # while verify, don't create new folder
        os.mkdir(path)  # create directory, fix for FileNotFoundError

    """ Setup logging """
    # log/dateTtime.log
    if argumnets.log:
        if argumnets.verify:  # while verify, don't create new folder
            path = "/".join(argumnets.signature.split("/")[:-1])
            print(path)

        logging.basicConfig(filename=f"{path}/{argumnets.file}.log",
                            encoding='utf-8',
                            level=logging.DEBUG)
    else:
        # default
        logging.basicConfig(filename="kry_log.log", encoding='utf-8', level=logging.DEBUG)

    # Log start, deliminer, time, file and size
    logging.info("#################################################")
    logging.info(f"[{start_time}]")
    logging.info(f"File {argumnets.file} Size: {os.path.getsize(argumnets.file)}")
    # logging.debug('This message should go to the log file')
    # logging.info('So should this')
    # logging.warning('And this, too')logging.info("Done.")
    # logging.error('And non-ASCII stuff, too, like Øresund and Malmö')

    main(argumnets, path)  # for testing purposes
    try:
        # main(argumnets, path)  # production :)
        pass
    except OptionException:
        parser.print_help()
    except MemoryError as exc:
        print(exc)
        logging.error(exc)

    except Exception as exc:
        print(exc)
        logging.error(exc)
    finally:
        logging.info("Done.")
