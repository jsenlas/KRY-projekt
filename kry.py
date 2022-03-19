""" Cryptography project VUT FEKT 2022
Authors:
    Thao Le
    Jakub Sencak
    Pavel Podluzansky
    Anh Phan
"""

import os
import sys
import argparse
import logging
import datetime
from src.hash_based_signature import PySPHINXplus
from src.exceptions import OptionException
from src.utils import log_print
# from src.ntru.ntrucipher import NtruCipher

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

    ##################################################
    g_parser = sub_parser.add_parser("ntru_g", help="Generating key")
    g_parser.add_argument("-p", "--parameters", action="store", nargs=3, type=int, help="N p q")
    g_parser.add_argument("private_file", type=str, help="Private key Filename")
    g_parser.add_argument("public_file", type=str, help="Public key Filename")
    
    ##################################################
    e_parser = sub_parser.add_parser("ntru_e", help="Encrypting message")
    e_parser.add_argument("public_key", type=str)
    e_parser.add_argument("message", type=str)

    ##################################################
    d_parser = sub_parser.add_parser("ntru_d", help="Decrypting message")
    d_parser.add_argument("private_key", type=str)
    d_parser.add_argument("encrypted_message", type=str)

    ##################################################
    sign_parser = sub_parser.add_parser("sphinx_sign", help='Signing a file')
    sign_parser.add_argument("file", type=str, help="Filename")

    ##################################################
    verify_parser = sub_parser.add_parser("sphinx_verify", help='Verifying file signature')
    verify_parser.add_argument("-k", "--public_key", action="store", help="File containing public key.")
    verify_parser.add_argument("-n", "--signature", action="store", help="File containing signature.")
    verify_parser.add_argument("file", type=str, help="Filename")

    arguments = parser.parse_args()

    print(parser)
    print(sign_parser)
    print(arguments)  # for debug only
    
    # """ Setup path """
    # "./out/filename_dir_date_time/filename.[log, signature, pbkey]"
    output_files_path = f"./out/{arguments.file}_dir_{start_time.replace(':', '_')}"
    print(output_files_path)

    """ Setup logging """
    log_filename = "kry_log.log" # default
    create_directory_flag = True
    if arguments.log:
        if "sphinx_verify" in sys.argv:
            output_files_path = "/".join(arguments.signature.split("/")[:-1])
            log_filename = f"{output_files_path}/{arguments.file}.log"
            create_directory_flag = False  # while verify, don't create a new folder

    if create_directory_flag:
        os.mkdir(output_files_path)  # create directory, fix for FileNotFoundError


    print("LOGFILENAME", log_filename)
    logging.basicConfig(filename=log_filename, encoding='utf-8', level=logging.DEBUG)

    # Log start, deliminer, time, file and size
    log_print("#################################################")
    log_print(f"[{start_time}]")
    log_print(f"File {arguments.file} Size: {os.path.getsize(arguments.file)}")
    # logging.debug('This message should go to the log file')
    # logging.info('So should this')
    # logging.warning('And this, too')logging.info("Done.")
    # logging.error('And non-ASCII stuff, too, like Øresund and Malmö')

    if "sphinx_sign" in sys.argv:
        log_print("EVENT_TYPE: Signing")
        log_print("Algorithm: SPHINX+")
        psx = PySPHINXplus(arguments.file)
        key, private_key, signature = psx.sign()
    
        print(f"{output_files_path}/{arguments.file}.signature")
        with open(f"{output_files_path}/{arguments.file}.signature", "wb") as fp:
            log_print("Saving signature to file...")
            fp.write(signature)
        
        # # save private key
        # with open(f"{path}/{arguments.file}.pvkey", "wb") as fp:
        #     logging.info("Saving public key to file.")
        #     fp.write(private_key)
    
        with open(f"{output_files_path}/{arguments.file}.pbkey", "wb") as fp:
            log_print("Saving public key to file...")
            fp.write(key)
        log_print(f"Saved to {output_files_path}")

    elif "sphinx_verify" in sys.argv:
        log_print("EVENT_TYPE: Verify")
        log_print("Algorithm: SPHINX+")
        psx = PySPHINXplus(arguments.file)
        if psx.verify(arguments.signature, arguments.public_key):
            log_print("Signature successfuly veriefied.")
        else:
            log_print("Signature verification UNSUCCESSFUL.")

    elif "ntru_g" in sys.argv:
        pass
    elif "ntru_e" in sys.argv:
        pass
    elif "public_key" in sys.argv:
        pass
    elif "ntru_d" in sys.argv:
        pass

    log_print("Done.")
