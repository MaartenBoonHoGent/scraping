from datetime import datetime

from log.mailer.mailer import Mailer


def sendMail(mailer: Mailer):
    print("Sending mail...")

def main():
    # Check if the day is monday
    if datetime.datetime.today().weekday() == 0:
        mailer = Mailer()
        sendMail(mailer)