# This module comes from django.core
#
# Copyright (c) 2005, the Lawrence Journal-World
# All rights reserved.

import smtplib, rfc822
import socket

def send_mail(subject, message, from_email, recipient_list, mail_server, auth_user, auth_password, fail_silently=False):
    """
    Easy wrapper for sending a single message to a recipient list. All members
    of the recipient list will see the other recipients in the 'To' field.
    """
    return send_mass_mail([[subject, message, from_email, recipient_list]], mail_server, auth_user, auth_password, fail_silently)

def send_mass_mail(datatuple, mail_server, auth_user, auth_password, fail_silently=False):
    """
    Given a datatuple of (subject, message, from_email, recipient_list), sends
    each message to each recipient list. Returns the number of e-mails sent.

    If from_email is None, the DEFAULT_FROM_EMAIL setting is used.
    If auth_user and auth_password are set, they're used to log in.
    """

    socket.setdefaulttimeout(10)

    try:
        server = smtplib.SMTP(mail_server)
        if auth_user and auth_password:
            server.login(auth_user, auth_password)
    except:
        if fail_silently:
            return 0
        raise
    num_sent = 0
    for subject, message, from_email, recipient_list in datatuple:
        if not recipient_list:
            continue
        from_email = from_email

        msg = ["Subject: %s" % subject,
               "From: %s " % from_email,
               "To: %s" % ', '.join(recipient_list),
               "Date: %s" % rfc822.formatdate(),
               "",
               message]
        try:
            server.sendmail(from_email, recipient_list, "\r\n".join(msg))
            num_sent += 1
        except:
            if not fail_silently:
                raise
    try:
        server.quit()
    except:
        if fail_silently:
            return
        raise
    return num_sent
