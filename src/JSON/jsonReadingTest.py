import json


with open("/home/pi/mu_code/SecuritySystemScripts/secretCode.json" , ) as code_file:
    code_file_data = json.load(code_file)
# Closing file
code_file.close()