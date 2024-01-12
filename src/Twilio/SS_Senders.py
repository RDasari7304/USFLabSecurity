import os
import src.Twilio.twilio_dets as twilio_dets
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import datetime


e = datetime.datetime.now()


def send_message(message , to , _from):
    message = twilio_dets.client.messages.create(
                     body=message,
                     from_=_from,
                     to=to
                 )




def send_img_email(from_ , to , img_path , subject = "Unauthorized entry"):
    img_data = open(img_path , 'rb').read()

    msg = MIMEMultipart()
    msg['From'] = from_
    msg['To'] = to
    msg['Subject'] = subject

    text = MIMEText("Unauthorized entry to the lab on %s/%s/%s" % (e.month , e.day , e.year))
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(img_path))
    msg.attach(image)

    s = smtplib.SMTP('smtp.gmail.com:587')
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("gamers2333@gmail.com", "RDasari#04")
    s.sendmail(from_, to, msg.as_string())
    s.quit()