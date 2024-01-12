from cryptography.fernet import Fernet
from os.path import exists
import os
#
# os.chdir("./src/JSON")

class Encryptor:
    def __init__(self, file):
        if not exists(os.getcwd() + "/key_file.key"):
            key = self.generate_key()
            self.write_key(key)

        self.key = self.read_key()
        self.file = file

    def generate_key(self):
        key = Fernet.generate_key()
        return key

    def write_key(self, key):
        with open("./key_file.key", "wb") as key_file:
            key_file.write(key)

    def read_key(self):
        with open("./key_file.key", "rb") as key_file:
            key = key_file.read()
        return key

    def encrypt_file(self):
        file_encryptor = Fernet(self.key)

        with open(self.file, "rb") as file:
            unencrypted_file = file.read()

        encrypted_file = file_encryptor.encrypt(unencrypted_file)

        with open(self.file, "wb") as file:
            file.write(encrypted_file)

    def decrypt_file(self):
        file_encryptor = Fernet(self.key)

        with open(self.file, "rb") as file:
            encrypted_file = file.read()

        decrypted_file = file_encryptor.decrypt(encrypted_file)

        with open(self.file, "wb") as file:
            file.write(decrypted_file)
