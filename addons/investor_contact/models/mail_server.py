import smtplib, ssl

port = 25  # For starttls
smtp_server = "197.243.19.169"
sender_email = "info.crm@rdb.rw"
sender_username = "RDB\\infoc"
receiver_email = "mukurutracey@gmail.com"
# password = input("Type your password and press enter:")
password = "c@(2019)rm!"
message = """\
Subject: Hi there

This message is sent from Python."""

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    # server.ehlo()  # Can be omitted
    # server.starttls(context=context)
    server.ehlo()  # Can be omitted
    server.login(sender_username, password)
    server.sendmail(sender_email, receiver_email, message)
