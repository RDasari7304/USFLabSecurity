import string
import random
import sys
sys.path.append("./Twilio")
sys.path.append("./JSON")
import Twilio.SS_Senders as SS_S
import SS_GUI as sg
import tkinter as tk
import JSON.jsonHandlers as jh

secret_code = ""

class Sender:
    def __init__(self, msg_body="", to="+12017022373", from_="+18045678824"):
        self.msg_body = msg_body
        self.to = to
        self.from_ = from_

def generate_secret_code():
    code_length = 6
    secret_code = ""

    ascii_result = string.ascii_uppercase
    code_digits = string.digits;

    letters_and_digits = ascii_result + code_digits

    for i in range(code_length):
        secret_code += random.choice(letters_and_digits)

    return secret_code


def send_notification_message(text="The secret entry code for today is "):
    sender = Sender(text + jh.get_secret_code())

    SS_S.send_message(sender.msg_body, sender.to, sender.from_)


jh.change_code(generate_secret_code())


def resetCode():
    jh.change_code(generate_secret_code())
    send_notification_message(text="The code has been reset, the new entry code for today is : " + secret_code)

if __name__ == "__main__":
    send_notification_message()
    sys_window = sg.SystemWindow(tk.Tk())
