from imap_auto import MailChecker
from email_auto import MailSender

imap = MailChecker()
imap.process_inbox()

smtp = MailSender()

# TODO: get email info
text = ''
smtp = build_message(text)
smtp = send_email()
