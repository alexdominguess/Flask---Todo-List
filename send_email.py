import smtplib


def send_email(user_email, subject, msg):
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login("alexdominguess@gmail.com", "D46in3hh")
    message = 'Subject: {}\n\n{}'.format(subject, msg)
    server.sendmail('alexdominguess@gmail.com', user_email, message)
    server.quit()
    return "Senha enviada"


if __name__ == '__main__':
    user_email = 'alexdominguess@gmail.com'
    user_password = '123456'
    subject = 'Senha Recuperada'
    message = ' Aqui esta sua senha - ' + user_password
    send_email(user_email, subject, message)
