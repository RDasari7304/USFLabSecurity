from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from src import SecuritySystem as SS

recieve_sms_app = Flask(__name__)

@recieve_sms_app.route('/sms' , methods=['POST'])
def sms():
    from_number = request.form['From']
    message = request.form['Body']

    message_to_send = ""

    if from_number == "+18134828801":
        if message.lower() == "reset":
            message_to_send += "Code is reset"
            SS.resetCode()
        else:
            message_to_send += "\n Invalid command given. The current available commands are : \n  \n - Reset "
    else :
        message_to_send += "You are unauthorized to command the security system"

    response = MessagingResponse()
    response.message(message_to_send)
    print(message)
    return str(response)