""" Create and verify signatures using postquantum cryptography algorithm Oil and vinegar 
    from Rainbow scheme.

    Author: Pavel Podlužanský
    email: xpodlu01@vutbr.cz
"""

from cryptovinaigrette import cryptovinaigrette

import pyspx.shake256_128f as pysphinx
import numpy as np
from src.utils import log_print

class Multivariate():
    """docstring for PySPHINXPLUS"""
    def __init__(self, filename, private_key):
        super().__init__()
        with open(filename, "rb") as fp:
            self.message = fp.read()
            self.private_key = private_key

    def sign(self):
        """ signing """
        # Initialise keygen object and generate keys
        myKeyObject = cryptovinaigrette.rainbowKeygen(save="/path/to/dest/folder")

        # signing
        signature = cryptovinaigrette.rainbowKeygen.sign(private_key, self.message)

        return signature    

    def verify(self, signature, public_key):
        check = cryptovinaigrette.rainbowKeygen.verify(public_key, signature, self.message)

        if check == True :
            print("Verified successfully!")
        else :
            print("Signature does not match the file!")
        return 0