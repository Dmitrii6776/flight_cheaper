import smtplib
my_mail = "dmitriiposhin@gmail.com"
my_password = "666542AAA"

class NotificationManager:
    def send_mail(self, message):
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=my_mail, password=my_password)
            connection.sendmail(
                from_addr=my_mail,
                to_addrs=my_mail,
                msg=f'Subject: Price Alert!.\n\n{message}')