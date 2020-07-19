from imap_auto import MailChecker
from email_auto import MailSender

def _extract_email(text, symbol):
    words = text.split(' ')
    return_word = None
    for word in words:
        if symbol in word:
            return_word = word
    return return_word

def extract_email(text):
    # extract email from text based on @ sign
    lines = text.splitlines()

    for line in lines:
        if '@' in line:
            email = _extract_email(line, '@')

    return email

def extract_name(text):
    # TODO : extract name from text based on ... something
    lines = text.splitlines()

    for line in lines:
        if 'name' in line:
            words = line.split(' ')
            name = words[1]

    return name


imap = MailChecker('insert mail address you want to filter to')
body_texts = imap.process_inbox()

smtp = MailSender()

for body in body_texts:
    email = extract_email(body)
    name = extract_name(body)

    # get email info
    text = f'email {email} \n name {name}'
    smtp.build_message(text)
    smtp.send_email()

imap.close_connection()
