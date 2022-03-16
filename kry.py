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
# from src.hash_based_signature import PySPHINXplus
from src.exceptions import OptionException
from src.ntru.ntrucipher import NtruCipher

def main(args, path):
    """ Main docstring """

    # Check combinations of arguments
    if args.decipher and args.cipher:
        raise OptionException("Wrong arguments given. cipher and decipher cannot be used together.")

    if args.sign and args.verify:
        raise OptionException(
            "Wrong arguments given. Signing and verifying signature cannot be used together.")

    # if args.sign == "SPHINXPLUS":  # Sign by SPHINX+
    #     logging.info("EVENT_TYPE: Signing")
    #     logging.info("Algorithm: SPHINX+")
    #
    #     psx = PySPHINXplus(args.file)
    #     key, private_key, signature = psx.sign()
    #
    #     with open(f"{path}/{args.file}.signature", "wb") as fp:
    #         logging.info("Saving signature to file...")
    #         fp.write(signature)
    #
    #     # with open(f"{path}/{args.file}.pvkey", "wb") as fp:
    #     #     logging.info("Saving public key to file.")
    #     #     fp.write(private_key)
    #
    #     with open(f"{path}/{args.file}.pbkey", "wb") as fp:
    #         logging.info("Saving public key to file...")
    #         fp.write(key)
    #     logging.info(f"Saved to {path}")
    #
    # elif args.verify == "SPHINXPLUS" and args.public_key and args.signature:
    #     logging.info("EVENT_TYPE: Verify")
    #     logging.info("Algorithm: SPHINX+")
    #     psx = PySPHINXplus(args.file)
    #     if psx.verify(args.signature, args.public_key):
    #         logging.info("Signature successfuly veriefied.")
    #         return
    #     logging.info("Signature verification UNSUCCESSFUL.")

    if True:
        pass
    else:
        raise OptionException("Wrong options, ending with no action...")


if __name__ == '__main__':
    start_time = datetime.datetime.now().isoformat().split('.')[0]

    """ Init argparse """
    parser = argparse.ArgumentParser(
                prog='kry.py',
                formatter_class=argparse.RawDescriptionHelpFormatter,
                epilog="KRY 2022 project - cipher/decipher or sign a file.")

    sub_parser = parser.add_subparsers(help="cipher/decipher")
    # ntru_parser = sub_parser.add_parser("cipher", help="cipher file")

    parser.add_argument("--log", action="store_true",
                        help="Log to separate file in the generated directory.")

    ######################################
    g_parser = sub_parser.add_parser("ntru_g", help="Generating key")
    g_parser.add_argument("-p", "--parameters", action="store", nargs=3, type=int, help="N p q")
    g_parser.add_argument("private_file", type=str, help="Private key Filename")
    g_parser.add_argument("public_file", type=str, help="Public key Filename")
    #####################################

    e_parser = sub_parser.add_parser("ntru_e", help="Encrypting message")
    # e_parser.add_argument("-e","-encrypt", action="store", help="Encrypting")
    e_parser.add_argument("public_key", type=str)
    e_parser.add_argument("message", type=str)
    ####################################

    d_parser = sub_parser.add_parser("ntru_d", help="Decrypting message")
    d_parser.add_argument("private_key", type=str)
    d_parser.add_argument("encrypted_message", type=str)



    # cipher_algorithm_list = [""]  # Here add name of your algorithm
    # de_cipher_group = parser.add_argument_group('cipher/decipher files')
    # de_cipher_group.add_argument("-c", "--cipher", choices=cipher_algorithm_list,
    #                              action="store", help="cipher a file", metavar="ALGORITHM")
    # de_cipher_group.add_argument("-d", "--decipher", choices=cipher_algorithm_list,
    #                              action="store", help="Decipher a file", metavar="ALGORITHM")

    sign_parser = sub_parser.add_parser("sphinx_sign", help='Signing a file')
    sign_parser.add_argument("file", type=str, help="Filename")

    verify_parser = sub_parser.add_parser("sphinx_verify", help='Verifying file signature')
    verify_parser.add_argument("-k", "--public_key", action="store", help="File containing public key.")
    verify_parser.add_argument("-n", "--signature", action="store", help="File containing signature.")
    verify_parser.add_argument("file", type=str, help="Filename")

    argumnets = parser.parse_args()

    print(argumnets)  # for debug only
    exit()
    """ Setup path """
    # "./out/filename_dir_date_time/filename.[log, signature, pbkey]"
    output_files_path = f"./out/{argumnets.file}_dir_{start_time.replace(':', '_')}"
    
    if not argumnets.verify:  # while verify, don't create new folder
        os.mkdir(output_files_path)  # create directory, fix for FileNotFoundError

    """ Setup logging """
    # log/dateTtime.log
    if argumnets.log:
        if argumnets.verify:  # while verify, don't create new folder
            output_files_path = "/".join(argumnets.signature.split("/")[:-1])
            print(output_files_path)

        logging.basicConfig(filename=f"{output_files_path}/{argumnets.file}.log",
                            encoding='utf-8',
                            level=logging.DEBUG)
    else:
        # default
        logging.basicConfig(filename="kry_log.log", encoding='utf-8', level=logging.DEBUG)

    # Log start, deliminer, time, file and size
    logging.info("#################################################")
    logging.info(f"[{start_time}]")
    logging.info(f"File {argumnets.file} Size: {os.output_files_path.getsize(argumnets.file)}")
    # logging.debug('This message should go to the log file')
    # logging.info('So should this')
    # logging.warning('And this, too')logging.info("Done.")
    # logging.error('And non-ASCII stuff, too, like Øresund and Malmö')

    main(argumnets, output_files_path)  # for testing purposes
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
