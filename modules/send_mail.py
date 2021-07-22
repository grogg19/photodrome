# -*- coding: utf8 -*-
import smtplib
import email
from modules.python_mysql_dbconfig import read_email_config


def sendemail(message):
    rec = read_email_config()

    header = 'From: Linux Cron<sender@mailserver.com>\n'
    header += 'To: %s\n' % ', '.join(rec['to_addr_list'])
    header += 'Subject: Cron Report of Photos Upload\n'

    message = email.message_from_string(message)
    message = header + str(message)

    server = smtplib.SMTP_SSL(rec['smtpserver'])
    server.login(rec['login'], rec['password'])
    problems = server.sendmail(rec['from_addr'], rec['to_addr_list'], message)
    server.quit()
