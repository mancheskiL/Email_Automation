import smtplib, ssl

class MailSender():
    def __init__(self, sender, receiver):
        self.port = 465
        self.password = None

        with open('./cred.txt') as f:
            for x in f:
                separate = x.split(':')
                self.password = separate[1]

        self.smtp_server = 'smtp.gmail.com'
        self.sender_email = sender
        self.receiver_email = receiver

        self.context = ssl.create_default_context()

        self.message = ''

    def build_message(self, text):
        self.message = text

    def send_email(self):
        with smtplib.SMTP_SSL(self.smtp_server,
                              self.port,
                              context=self.context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email,
                            self.receiver_email,
                            self.message)
