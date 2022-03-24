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
# from src.hash_based_signature import PySPHINXplus
from src.exceptions import OptionException
from src.utils import log_print

########## Ntru import ############
from src.ntru.ntrucipher import NtruCipher
import numpy as np
from src.ntru.mathutils import random_poly
from sympy import ZZ, Poly, isprime
import math
from src.ntru.padding import *
from sympy.abc import x

########## Ntru Functions ##############
def generate(N, p, q, priv_key_file, pub_key_file):
    if not isprime(N):
        # log_print("N must be a prime")
        raise OptionException("N must be a prime")
    if math.gcd(p,q) != 1:
        raise OptionException("p and q must be co-prime")
    ntru = NtruCipher(N, p, q)
    ntru.generate_random_keys()
    h = np.array(ntru.h_poly.all_coeffs()[::-1])
    f, f_p = ntru.f_poly.all_coeffs()[::-1], ntru.f_p_poly.all_coeffs()[::-1]
    np.savez_compressed(priv_key_file, N=N, p=p, q=q, f=f, f_p=f_p)
    log_print("Private key saved to {} file".format(priv_key_file))
    np.savez_compressed(pub_key_file, N=N, p=p, q=q, h=h)
    log_print("Public key saved to {} file".format(pub_key_file))


def encrypt(pub_key_file, input_arr, bin_output=False, block=True):
    input_arr = np.unpackbits(np.frombuffer(input_arr, dtype=np.uint8))
    input_arr = np.trim_zeros(input_arr, 'b')
    log_print("POLYNOMIAL DEGREE: {}".format(max(0, len(input_arr) - 1)))
    log_print("BINARY: {}".format(input_arr))

    pub_key = np.load(pub_key_file, allow_pickle=True)
    ntru = NtruCipher(int(pub_key['N']), int(pub_key['p']), int(pub_key['q']))
    ntru.h_poly = Poly(pub_key['h'].astype(np.int)[::-1], x).set_domain(ZZ)
    if not block:
        if ntru.N < len(input_arr):
            raise Exception("Input is too large for current N")
        output = (ntru.encrypt(Poly(input_arr[::-1], x).set_domain(ZZ),
                               random_poly(ntru.N, int(math.sqrt(ntru.q)))).all_coeffs()[::-1])
    else:
        input_arr = padding_encode(input_arr, ntru.N)
        input_arr = input_arr.reshape((-1, ntru.N))
        output = np.array([])
        block_count = input_arr.shape[0]
        for i, b in enumerate(input_arr, start=1):
            log_print("Processing block {} out of {}".format(i, block_count))
            next_output = (ntru.encrypt(Poly(b[::-1], x).set_domain(ZZ),
                                        random_poly(ntru.N, int(math.sqrt(ntru.q)))).all_coeffs()[::-1])
            if len(next_output) < ntru.N:
                next_output = np.pad(next_output, (0, ntru.N - len(next_output)), 'constant')
            output = np.concatenate((output, next_output))

    if bin_output:
        k = int(math.log2(ntru.q))
        output = [[0 if c == '0' else 1 for c in np.binary_repr(n, width=k)] for n in output]
    return np.array(output).flatten()

#############################################





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
    print(g_parser)
    print(arguments)  # for debug only
    
    # """ Setup path """
    # "./out/filename_dir_date_time/filename.[log, signature, pbkey]"
    try:
        output_files_path = f"./out/{arguments.file}_dir_{start_time.replace(':', '_')}"
    except AttributeError:
        output_files_path = f"./out/dir_{start_time.replace(':', '_')}"
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
    if "sphinx_verify" in sys.argv:
        log_print(f"File {arguments.file} Size: {os.path.getsize(arguments.file)}")

    # logging.debug('This message should go to the log file')
    # logging.info('So should this')
    # logging.warning('And this, too')logging.info("Done.")
    # logging.error('And non-ASCII stuff, too, like Øresund and Malmö')

    if "sphinx_sign" in sys.argv:
        pass
    #     log_print("EVENT_TYPE: Signing")
    #     log_print("Algorithm: SPHINX+")
    #     psx = PySPHINXplus(arguments.file)
    #     key, private_key, signature = psx.sign()
    #
    #     print(f"{output_files_path}/{arguments.file}.signature")
    #     with open(f"{output_files_path}/{arguments.file}.signature", "wb") as fp:
    #         log_print("Saving signature to file...")
    #         fp.write(signature)
    #
    #     # # save private key
    #     # with open(f"{path}/{arguments.file}.pvkey", "wb") as fp:
    #     #     logging.info("Saving public key to file.")
    #     #     fp.write(private_key)
    #
    #     with open(f"{output_files_path}/{arguments.file}.pbkey", "wb") as fp:
    #         log_print("Saving public key to file...")
    #         fp.write(key)
    #     log_print(f"Saved to {output_files_path}")
    #
    # elif "sphinx_verify" in sys.argv:
    #     log_print("EVENT_TYPE: Verify")
    #     log_print("Algorithm: SPHINX+")
    #     psx = PySPHINXplus(arguments.file)
    #     if psx.verify(arguments.signature, arguments.public_key):
    #         log_print("Signature successfuly veriefied.")
    #     else:
    #         log_print("Signature verification UNSUCCESSFUL.")

    elif "ntru_g" in sys.argv:
        N,p,q = arguments.parameters
        generate(N,p,q, arguments.private_file, arguments.public_file)
    elif "ntru_e" in sys.argv:
        with open(arguments.message, "rb") as fp:
            message = fp.read()
        output = encrypt(arguments.public_key, message)
        with open("bubu", "wb") as fp:
            fp.write(output)
    elif "public_key" in sys.argv:
        pass
    elif "ntru_d" in sys.argv:
        pass

    log_print("Done.")
