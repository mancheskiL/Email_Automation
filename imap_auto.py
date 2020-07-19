import imaplib
import email

username = 'lumandevcode@gmail.com'
password = 'luman_dev123'

imap = imaplib.IMAP4_SSL('imap.gmail.com')
imap.login(username, password)

status, messages = imap.select('INBOX')

print(imap.status('INBOX', '(MESSAGES UNSEEN)')[1][0].decode())
typ, mesg_ids = imap.search(None, 'UNSEEN')
decoded = mesg_ids[0].decode()

ids = []
for item in decoded:
    try:
        num = int(item)
        ids.append(num)
    except:
        print('empty string, moving on')

print(ids)

for id in ids:
    resp, msg = imap.fetch(str(id), '(RFC822)')
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
            elif 'attachment' in content_disposition:
                pass
    else:
        content_type = msg.get_content_type()

        body = msg.get_payload(decode=True).decode()
        if content_type == 'text/plain':
            print(body)

        if content_type == 'text/html':
            print(body)

imap.close()
imap.logout()
