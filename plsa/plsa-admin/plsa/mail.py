import smtplib, rfc822
import socket

# i18n
import gettext
__trans = gettext.translation("plsa", fallback=True)
_ = __trans.ugettext

def send_mail(subject, message, from_email, recipient_list, mail_server, auth_user, auth_password):
    socket.setdefaulttimeout(10)
    try:
        server = smtplib.SMTP(mail_server)
        try:
            server.login(auth_user, auth_password)
        except smtplib.SMTPHeloError:
            print _("Unable to send mail: Server didn't reply")
            return
        except smtplib.SMTPAuthenticationError:
            print _("Unable to send mail: Server didn't accept username/password")
            return
        except smtplib.SMTPError:
            print _("Unable to send mail: No suitable authentication method was found")
            return
    except socket.gaierror, e:
        print _("Unable to send mail: %s") % e[1]
        return
    except smtplib.SMTPConnectError:
        print _("Unable to send mail: Can't connect mail server")
        return
    except smtplib.SMTPException:
        print _("Unable to send mail: SMTP error")
        return

    msg = ["Subject: %s" % subject,
           "From: %s " % from_email,
           "To: %s" % ', '.join(recipient_list),
           "Date: %s" % rfc822.formatdate(),
           "",
           message]

    try:
        server.sendmail(from_email, recipient_list, "\r\n".join(msg))
    except smtplib.SMTPSenderRefused:
        print _("Unable to send mail: Server didn't accept sender")
        return
    except smtplib.SMTPRecipientsRefused:
        print _("Unable to send mail: Server didn't accept recipients")
        return

    server.quit()

    return True

def valid_address(email):
    if "@" not in email or "." not in email:
        return False
    if email.rindex(".") < email.index("@"):
        return False
    return True
