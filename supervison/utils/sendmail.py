#!/usr/bin/python
#-*- coding: UTF-8 -*-

import sys, os, smtplib, socket, email
from getpass import getpass

from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Utils, Encoders
import mimetypes

def send_email(recp, subject, content):
    username = 'username'
    from_who = 'fromwho'
    password = 'passwd'
    stmp = 'stmp server'

    server = smtplib.SMTP(stmp)
    code = server.ehlo()[0]
    usesesmtp = 1
    if not (200 <= code <= 299):
        usesesmtp = 0
        code = server.helo()[0]
        if not (200 <= code <= 299):
            raise SMTPHeloError(code, resp)

    if usesesmtp and server.has_extn('starttls'):
        print "Negotiating TLS...."
        server.starttls()
        code = server.ehlo()[0]
        if not (200 <= code <= 299):
            print "Couldn't EHLO after STARTTLS"
            sys.exit(5)
        print "Using TLS connection."
    else:
        print "Server does not support TLS; using normal connection."

    try:
        server.login(username, password)
    except smtplib.SMTPException, e:
        print "Authentication failed:", e
        sys.exit(1)

    msg = email.Message.Message()
    msg['To'] = recp
    msg['From'] = from_who
    msg['Date'] = Utils.formatdate(localtime = 1)
    #msg['Message-ID'] = Utils.make_msgid()
    msg['Subject'] = subject

    body = MIMEText(content, _charset='utf-8')
    #body = MIMEText(content, _subtype='plain', _charset='utf-8')
    #msg = MIMEMultipart()
    #msg.attach(body)
    try:
        #server.sendmail(from_who, recp.split(","), msg.as_string())
        server.sendmail(from_who, recp.split(","), msg.as_string()[:-1]+body.as_string())
    except (socket.gaierror, socket.error, socket.herror, smtplib.SMTPException), e:
        print "failed sent!"
        print e
        sys.exit(1)
    else:
        print "successfully sent "

if __name__ == '__main__':
    send_email("liyang@miaozhen.com", "shit", "shit happen")
