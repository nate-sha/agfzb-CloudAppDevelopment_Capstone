import os
from binascii import hexlify


def generate_hex():
    return hexlify(os.urandom(4)).decode()
