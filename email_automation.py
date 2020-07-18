import smtplib, ssl

port = 465 # For SSL in gmail
password = input('Type your password and press enter')

smtp_server = 'smtp.gmail.com'
sender_email = 'lumandevcode@gmail.com'
receiver_email = 'lumandevcode@gmail.com'
message = """\
Subject: Hi there


This message is sent from Python.
"""

# Create secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    # Send email here
    server.sendmail(sender_email, receiver_email, message)
