import json
import os
import src.JSON.jsonEncryptor as jsonEncryptor

dir_name = os.getcwd()
path_to_file = dir_name + "/secretCode.json"
encryptor = jsonEncryptor.Encryptor("secretCode.json")

def getValueByProperty(property):
    data = getFileData()
    return data[property]

def change_code(newCode):
    code_dict = {'secretCode': newCode}
    print(code_dict)
    dumpData(code_dict)

def dumpData(data):
    encryptor.decrypt_file()
    with open("secretCode.json", "w") as file:
        json.dump(data, file)
    encryptor.encrypt_file()


def getFileData():
    encryptor.decrypt_file()
    with open(path_to_file, "r") as code_file:
        code_file_data = json.load(code_file)

    encryptor.encrypt_file()
    return code_file_data

def get_secret_code():
    return getValueByProperty('secretCode')