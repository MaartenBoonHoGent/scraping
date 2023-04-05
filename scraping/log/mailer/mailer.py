import datetime
import imaplib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List


class Mailer:
    def __init__(self):
        self._mailer: smtplib.SMTP = self.create_mailer()
        self._checker: imaplib.IMAP4_SSL = self.create_checker()
        self._lastRefresh = datetime.datetime.now().timestamp()
        self._lastChecked = 0

    @staticmethod
    def create_mailer():
        # Initialize server connection
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login("algo.x.v2@gmail.com", "oxdugrffjrvxmuca")
        return server

    @staticmethod
    def create_checker():
        server = imaplib.IMAP4_SSL('imap.gmail.com')
        server.login("algo.x.v2@gmail.com", "oxdugrffjrvxmuca")
        server.select("inbox")
        return server

    def sendMail(self, title: str, body: str, send_to: List[str]):
        assert send_to is not None and len(send_to) > 0, "No send_to specified"
        htmlBody = f"<body>{body}</body>"
        send_to = ", ".join(send_to)
        if isinstance(send_to, str):
            send_to = send_to.strip()

        message = MIMEMultipart("alternative", None, [MIMEText(htmlBody, 'html')])
        message['Subject'] = title
        message['From'] = "AlgoC"
        message['BCC'] = send_to
        if send_to != "":
            self._mailer.send_message(message)
