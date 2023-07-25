import smtplib
import schedule
import time



def send_email(subject, body):
    # login to the Gmail account
    sender = 'jimmyjin.zjin6@gmail.com'
    password = 'Objective-66'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)

    # create the email message
    recipient = 'zjin6@ford.com'
    message = f'Subject: {subject}\n\n{body}'

    # send the email message
    server.sendmail(sender, recipient, message)
    print('sent ...')
    server.quit()


def send_daily_message():
    subject = 'Daily Message'
    body = 'Hello, this is your daily message!'
    send_email(subject, body)


schedule.every().day.at('11:28').do(send_daily_message)


# run the scheduled task continuously
while True:
    schedule.run_pending()
    time.sleep(1)


 [Errno 11001] getaddrinfo failed inside Ford VPN