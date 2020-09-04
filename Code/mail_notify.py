import pyfirmata
import time
import smtplib
import ssl

from creds import sender_email, receiver_email, password

def send_email():
    port = 465 # For SSL
    smtp_server = "smtp.gmail.com"
    message = """Subject: Arduino Notification\n The switch was turned on!"""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        print("Sending email")
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

board = pyfirmata.Arduino('/dev/cu.usbmodem14601')

it = pyfirmata.util.Iterator(board)
it.start()

digital_input = board.get_pin('d:10:i')

while True:
    sw = digital_input.read()
    if sw is True:
        send_email()
    time.sleep(0.1)