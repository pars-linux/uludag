#!/usr/bin/python

# Imports:
from sys import argv
# Import Notifier
from notclient import *

# If executed as the main program:
if __name__ == "__main__":
    nt = Notifier()
    while 1:
        line = raw_input("Enter a command: ")
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
                this_notification = Notification()
                this_notification.text = line[7:]
                result = nt.SendNotification(this_notification)
            else:
                print "Wrong command"
        if result != None:
            print "Service returned: %s" % result
else:
    print "This thing is not meant to be loaded as a module."
