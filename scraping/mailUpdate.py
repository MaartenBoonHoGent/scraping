from datetime import datetime

from log.mailer.mailer import Mailer
from log.logger import Logger


def sendErrors(mailer: Mailer):
    print("Sending errors...")
    logger = Logger()
    # Load the data from the database
    data = logger.errors
    # Today's timestamp
    today = datetime.today().timestamp()
    # Filter the data
    data = data[data["timestamp"] > today - 86400]
    if len(data.index) > 0:
        # Sort the data
        data = data.sort_values(by="timestamp", ascending=False)
        # Create the mail
        table = data.to_html()
        body = f"<h1>Errors</h1>{table}"
        mailer.sendMail("Errors", body, send_to=[
            "maarten.boon@student.hogent.be"
        ])


def sendMail(mailer: Mailer):
    print("Sending mail...")
    logger = Logger()
    # Load the data from the database
    data = logger.logs
    # Today's timestamp
    today = datetime.today().timestamp()
    # Filter the data
    data = data[data["timestamp"] > today - 86400]
    if len(data.index) > 0:
        # Sort the data
        data = data.sort_values(by="timestamp", ascending=False)
        # Create the mail
        table = data.to_html()
        body = f"<h1>Logs</h1>{table}"
        mailer.sendMail("Logs", body, send_to=[
            "maarten.boon@student.hogent.be"
        ])


def main():
    # Check if the day is monday
    mailer = Mailer()
    sendErrors(mailer)
    if datetime.today().weekday() == 0:
        sendMail(mailer)


if __name__ == "__main__":
    main()
