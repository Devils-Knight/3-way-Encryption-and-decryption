import base64
import logging
import os
from random import SystemRandom
from cryptography.exceptions import AlreadyFinalized,InvalidTag,UnsupportedAlgorithm
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def Encryption(plain_text):
    """
    Example for encryption and decryption of a string in one method.
    - Random password generation using strong secure random number generator
    - Random salt generation using OS random mode
    - Key derivation using PBKDF2 HMAC SHA-512
    - AES-256 authenticated encryption using GCM
    - BASE64 encoding as representation for the byte-arrays
    - UTF-8 encoding of Strings
    - Exception handling
    """
    psswd_choice = input("\nDo you want to create a password y/n: ")
    if psswd_choice == "Y" or psswd_choice == "y":
        password = input("Please enter the Password: ")
    else:
        password= ""
    try:
        # GENERATE password (not needed if you have a password already)
        if not password:
            alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            password = "".join(SystemRandom().choice(alphabet) for _ in range(9))
            print("Your random generated password is: ",password)
        password_bytes = password.encode('utf-8')

        # GENERATE random salt (needed for PBKDF2HMAC)
        #salt = os.urandom(32)
        salt =b'\xa5\xc7\x7fpczU\x14\x1a\x8f\x89\xe3@A\xae\xa3\xad\xe6a]\xc13\xec\xbd2V\xfe&D\xde\xa7\xb6'

        # DERIVE key (from password and salt)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA512(),
            length=32,
            salt=salt,
            iterations=10000,
            backend=default_backend()
        )
        key = kdf.derive(password_bytes)

        # GENERATE random nonce (number used once)
        #nonce = os.urandom(12)
        nonce =b'\x8f\x02\xef\xa1\xb8\x15s\xf0+\x86\xfe\x9a'

        # ENCRYPTION
        aesgcm = AESGCM(key)
        cipher_text_bytes = aesgcm.encrypt(
            nonce=nonce,
            data=plain_text.encode('utf-8'),
            associated_data=None
        )
        # CONVERSION of raw bytes to BASE64 representation
        cipher_text = base64.urlsafe_b64encode(cipher_text_bytes)
        print("\nYour Encrypted Text is: ",cipher_text)
        main_cipher_txt=""
        for i in cipher_text:
            main_cipher_txt+= chr(i)

    except (UnsupportedAlgorithm, AlreadyFinalized, InvalidTag):
        logger.exception("Symmetric encryption failed")
    return main_cipher_txt



def Decryption(signature):
    password = input("Enter the password: ")
    try:
        password_bytes = password.encode('utf-8')
        salt = b'\xa5\xc7\x7fpczU\x14\x1a\x8f\x89\xe3@A\xae\xa3\xad\xe6a]\xc13\xec\xbd2V\xfe&D\xde\xa7\xb6'

        # DERIVE key (from password and salt)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA512(),
            length=32,
            salt=salt,
            iterations=10000,
            backend=default_backend()
        )
        key = kdf.derive(password_bytes)

        # GENERATE random nonce (number used once)
        nonce =b'\x8f\x02\xef\xa1\xb8\x15s\xf0+\x86\xfe\x9a'

        # ENCRYPTION
        aesgcm = AESGCM(key)

        cipher_text=signature.encode('utf-8')

        # DECRYPTION
        decrypted_cipher_text_bytes = aesgcm.decrypt(
            nonce=nonce,
            data=base64.urlsafe_b64decode(cipher_text),
            associated_data=None
        )
        decrypted_cipher_text = decrypted_cipher_text_bytes.decode('utf-8')
        print("\n\n<<<<<<<<<<<< Message Extracted >>>>>>>>>>>>>\n")
        return decrypted_cipher_text

    except (UnsupportedAlgorithm, AlreadyFinalized, InvalidTag):
        print("\n\n<<<<<<<<<<<< Extraction Failed >>>>>>>>>>>>>\n")
        # logger.exception("Symmetric decryption failed")