import smtplib
from data.config import email_login, email_password, recipient


async def send_email(message):
    sender = email_login
    # sender = 'Sababaiptvbot@gmail.com'
    password = email_password
    # password = 'GenaIdan08011403'
    server = smtplib.SMTP("smtp.gmail.com", 587)
    title = 'NEW OFFER'
    server.starttls()
    try:
        server.login(sender, password)
        # recipient = 'justlikevova@gmail.com'
        server.sendmail(sender, recipient, f"Subject: {title}\n{message}")
        print('send')
        return "Message was send"
    except Exception as e:
        return f'{e}\nCheck your login or password'
