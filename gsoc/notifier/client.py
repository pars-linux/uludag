#!/usr/bin/python

# Imports:
import sys

# Import internationalization support:
import gettext
_ = gettext.translation("notman", "./i18n", fallback = True).ugettext

# Import Notifier
from notclient import *

# If executed as the main program:
if __name__ == "__main__":
    nt = Notifier()
    while 1:
        line = raw_input(_("Enter a command: ")).decode(sys.stdin.encoding)
        words = line.split()
        result = None
        if words.__len__() > 0:
            command = words[0]
            if command == "quit":
                exit()
            elif command == "sendexit":
                nt.SendExitSignal()
            elif command == "echo":
                result = nt.Echo(line[5:])
            elif command == "notify":
                this_notification = Notification(line[7:])
                this_notification.Pack()
                result = nt.SendNotification(this_notification)
            else:
                print _("Wrong command")
        if result != None:
            print _("Service returned: %s") % result
else:
    print _("This program is not meant to be loaded as a module.")
