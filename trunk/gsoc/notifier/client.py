#!/usr/bin/python

# Imports:
from sys import argv

# Import internationalization support:
import gettext
_ = gettext.translation("notman", "./i18n", fallback = True).ugettext

# Import Notifier
from notclient import *

# If executed as the main program:
if __name__ == "__main__":
    nt = Notifier()
    while 1:
        line = raw_input(_("Enter a command: "))
        words = line.split()
        result = None
        if words.__len__() > 0:
            command = words[0]
            if command == "quit":
                exit()
            elif command == "sendexit":
                nt.SendExitSignal()
            elif command == "echo":
                result = nt.Echo(unicode(line[5:], encoding = "utf-8"))
            elif command == "notify":
                this_notification = Notification()
                this_notification.text = unicode(line[7:], encoding = "utf-8")
                result = nt.SendNotification(this_notification)
            else:
                print _("Wrong command")
        if result != None:
            print _("Service returned: %s") % result
else:
    print _("This program is not meant to be loaded as a module.")
