""" Cryptography project VUT FEKT 2022
Authors:
    Thao Le
    Jakub Sencak
    Pavel Podluzansky
    Anh Viet Phan
"""

import os
import sys
import argparse
import logging
import datetime
from src.hash_based_signature import PySPHINXplus
from src.exceptions import OptionException
from src.utilities import log_print
from src.Multivariate import Multivariate

from src.ntru.ntrumain import *

from src.mceliece.LDPC import LDPC
from src.mceliece.McEliece import McEliece


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
    parser.add_argument("--onedir", action="store_true",
                        help="Save signature and public key in directory. "
                        "This option will overwrite existing files.")

    ##################################################
    g_parser = sub_parser.add_parser("ntru_g", help="Generating key")
    g_parser.add_argument("-p", "--parameters", action="store", nargs=3, type=int, help="N p q")
    g_parser.add_argument("private_file", type=str, help="Private key Filename")
    g_parser.add_argument("public_file", type=str, help="Public key Filename")
    # g_parser.add_argument("file", type=str, help="Filename")

    ##################################################
    e_parser = sub_parser.add_parser("ntru_e", help="Encrypting message")
    e_parser.add_argument("public_key", type=str)
    e_parser.add_argument("encrypted_file", type=str)
    e_parser.add_argument("message", type=str)
    # e_parser.add_argument("file", type=str, help="Filename")

    ##################################################
    d_parser = sub_parser.add_parser("ntru_d", help="Decrypting message")
    d_parser.add_argument("private_key", type=str)
    d_parser.add_argument("encrypted_message", type=str)
    d_parser.add_argument("decrypted_file", type=str)
    # d_parser.add_argument("file", type=str, help="Filename")

    ##################################################
    sphinx_sign_parser = sub_parser.add_parser("sphinx_sign", help='Signing a file')
    sphinx_sign_parser.add_argument("file", type=str, help="Filename")

    ##################################################
    sphinx_verify_parser = sub_parser.add_parser("sphinx_verify", help='Verifying file signature')
    sphinx_verify_parser.add_argument("-k", "--public_key", action="store", help="File containing public key.")
    sphinx_verify_parser.add_argument("-s", "--signature", action="store", help="File containing signature.")
    sphinx_verify_parser.add_argument("file", type=str, help="Filename")

    ##################################################
    multivariate_sign_parser = sub_parser.add_parser("sign_multivariate", help='Signing a file')
    multivariate_sign_parser.add_argument("file", type=str, help="Filename")

    ##################################################
    multivariate_verify_parser = sub_parser.add_parser("verify_multivariate", help='Verifying file signature')
    multivariate_verify_parser.add_argument("-k", "--public_key", action="store", help="File containing public key.")
    multivariate_verify_parser.add_argument("-s", "--signature", action="store", help="File containing signature.")
    multivariate_verify_parser.add_argument("file", type=str, help="Filename")


    ##################################################
    m_encrypt_parser = sub_parser.add_parser("encrypt_mceliece", help='Encrypt file using McEliece.')
    m_encrypt_parser.add_argument("file", type=str, help="Filename")

    ##################################################
    m_decrypt_parser = sub_parser.add_parser("decrypt_mceliece", help='Decrypt file using McEliece.')
    m_decrypt_parser.add_argument("file", type=str, help="Filename")

    arguments = parser.parse_args()

    # print(parser)
    # print(g_parser)
    # print(arguments)  # for debug only
    # import pdb
    # pdb.set_trace()
    # """ Setup path """
    if arguments.onedir:
        output_files_path = f"./out"
    else:
        # "./out/filename_dir_date_time/filename.[log, signature, pbkey]"
        output_files_path = f"./out"
        # if "ntru_g" not in sys.argv:
        #     output_files_path = f"./out/{arguments.file}_dir_{start_time.replace(':', '_')}"
    
    # print(output_files_path)

    """ Setup logging """
    log_filename = "kry_log.log" # default
    if "ntru_e" or "ntru_d" in sys.argv:
        log_filename = f"out/ntru_log/log_{start_time.replace(':', '_')}"



    create_directory_flag = True
    if arguments.log:
        if "sphinx_verify" in sys.argv:
            output_files_path = "/".join(arguments.signature.split("/")[:-1])
            log_filename = f"{output_files_path}/{arguments.file}.log"
            create_directory_flag = False  # while verify, don't create a new folder

    if create_directory_flag:
        try:
            os.mkdir(output_files_path)  # create directory, fix for FileNotFoundError
        except FileExistsError:
            pass

    print("LOGFILENAME", log_filename)
    logging.basicConfig(filename=log_filename, encoding='utf-8', level=logging.DEBUG)

    # Log start, deliminer, time, file and size
    log_print("#################################################")
    log_print(f"[{start_time}]")
    if "sphinx_verify" in sys.argv:
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

    elif "sign_multivariate" in sys.argv:
        log_print("EVENT_TYPE: Signing")
        log_print("Algorithm: Multivariate")
        multivariate = Multivariate(arguments.file)
        signature = multivariate.sign()
        print("SIGNATURE:", signature)
        print(f"{output_files_path}/{arguments.file}.signature")
        with open(f"{output_files_path}/{arguments.file}.signature", "w") as fp:
            log_print("Saving signature to file...")
            for element in signature:
                fp.write(str(element) + "\n")
        
    elif "verify_multivariate" in sys.argv:
        log_print("EVENT_TYPE: Verify")
        log_print("Algorithm: Multivariate")
        multivariate = Multivariate(arguments.file)
        print(arguments.signature)
        if multivariate.verify(arguments.signature):
            log_print("Signature successfuly veriefied.")
        else:
            log_print("Signature verification UNSUCCESSFUL.")

    elif "sphinx_verify" in sys.argv:
        log_print("EVENT_TYPE: Verify")
        log_print("Algorithm: SPHINX+")
        psx = PySPHINXplus(arguments.file)
        if psx.verify(arguments.signature, arguments.public_key):
            log_print("Signature successfuly veriefied.")
        else:
            log_print("Signature verification UNSUCCESSFUL.")

    elif "ntru_g" in sys.argv:
        N,p,q = arguments.parameters
        generate(N,p,q, arguments.private_file, arguments.public_file)
    elif "ntru_e" in sys.argv:
        log_print(f"Reading file {arguments.message}")
        with open(arguments.message, "rb") as fp:
            message = fp.read()
        log_print(f"Encrypting using public key {arguments.public_key}")
        output = encrypt(f"out/ntru_key/{arguments.public_key}", message)
        log_print(f"Saving encrypted message to {arguments.encrypted_file}")
        with open(f"ntru_file/{arguments.encrypted_file}", "wb") as fp:
            fp.write(np.packbits(np.array(output).astype(np.int)).tobytes())

            # with open(f"{output_files_path}/{arguments.file}.signature", "wb") as fp:
            #     log_print("Saving signature to file...")
            #     fp.write(signature)

    elif "ntru_d" in sys.argv:
        log_print(f"Opening encrypted message in file {arguments.encrypted_message}")
        with open(f"ntru_file/{arguments.encrypted_message}", "rb") as fp:
            message = fp.read()
        log_print(f"Decrypting using {arguments.private_key}")
        output = decrypt(f"out/ntru_key/{arguments.private_key}", message)
        log_print(f"Saving output into {arguments.decrypted_file}")
        with open(f"ntru_file/{arguments.decrypted_file}", "wb") as fp:
            fp.write(np.packbits(np.array(output).astype(np.int)).tobytes())

    elif "encrypt_mceliece" in sys.argv:
        with open(arguments.file, "r") as fp:
            content = fp.read()
            print(content)
        
            n = 300
            d_v = 6
            d_c = 10

            ldpc = LDPC.from_params(n, d_v, d_c)
            
            word = np.random.randint(2, size=ldpc.getG().shape[0])
            print("word:", word)

            crypto = McEliece.from_linear_code(ldpc, 12)

            encrypted = crypto.encrypt(word)
            print("encrypted:", encrypted)
            decrypted = crypto.decrypt(encrypted)
            print("decrypted:", decrypted)

            assert (word == decrypted).all()

    elif "decrypt_mceliece" in sys.argv:
        with open(arguments.file, "r") as fp:
            content = fp.read()
    else:
        log_print("You are wrong...")

    log_print("Done.")
