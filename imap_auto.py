import imaplib
import email

class MailChecker():
    def __init__(self, from_address):
        self.username = None
        self.password = None

        with open('./cred.txt') as f:
            for x in f:
                separate = x.split(':')
                self.username = separate[0]
                self.password = separate[1]

        self.imap = imaplib.IMAP4_SSL('imap.gmail.com')
        self.imap.login(self.username, self.password)

        status, messages = self.imap.select('INBOX')

        print(self.imap.status('INBOX', '(MESSAGES UNSEEN)')[1][0].decode())
        self.typ, self.mesg_ids = self.imap.search(None, f'UNSEEN FROM {from_address}')
        self.decoded = self.mesg_ids[0].decode()

        self.ids = []
        for item in self.decoded:
            try:
                num = int(item)
                self.ids.append(num)
            except:
                pass

        self.full_body = []


    def process_inbox(self):
        for id in self.ids:
            resp, msg = self.imap.fetch(str(id), '(RFC822)')
            msg = email.message_from_bytes(msg[0][1])

            # get subject line from msg object
            subject = email.header.decode_header(msg['Subject'])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()

            # get from line from msg object
            from_ = msg.get('From')

            print('Subject:', subject)
            print('From:', from_)

            # if msg is multipart, which it probably is!
            if msg.is_multipart():
                # walk through different parts and handle accordingly
                for part in msg.walk():
                    # get content type of email, this determines how we handle
                    content_type = part.get_content_type()
                    content_disposition = str(part.get('Content-Disposition'))
                    try:
                        # get email body
                        body = part.get_payload(decode=True).decode()
                    except:
                        pass
                    if content_type == 'text/plain' and 'attachment' not in content_disposition:
                        # print text/plain emails and skip attachments
                        print(body)
                        self.full_body.append(body)
                    elif 'attachment' in content_disposition:
                        pass
            else:
                content_type = msg.get_content_type()

                body = msg.get_payload(decode=True).decode()
                if content_type == 'text/plain':
                    print(body)
                    self.full_body.append(body)

                if content_type == 'text/html':
                    print(body)
                    self.full_body.append(body)
        return self.full_body

    def close_connection(self):
        self.imap.close()
        self.imap.logout()
