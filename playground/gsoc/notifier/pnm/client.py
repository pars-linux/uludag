#!/usr/bin/env python

# Imports:
import sys

# Import internationalization support:
import gettext
_ = gettext.translation("notman", fallback = True).ugettext

# Import Notifier
from notclient import *

# If executed as the main program:
if __name__ == "__main__":
	nt = Notifier()
	while 1:
		line = raw_input(_("Enter a command: ")).decode(sys.stdin.encoding)
		words = line.split()
		sections = line.split("\"")
		result = None
		if words.__len__() > 0:
			command = words[0]
			if command == "quit":
				exit()
			elif command == "sendexit":
				nt.SendExitSignal()
			elif command == "echo":
				result = nt.Echo(line[5:])
			elif command == "notifyicon":
				if sections.__len__() < 5:
					print _("Wrong command")
					continue
				title = sections[1]
				text = sections[3]
				this_notification = Notification(notification_title = title, notification_text = text)
				if sections.__len__() >= 9:
					icon_path = sections[5]
					this_notification.SetNotificationIcon(icon_path)
					for i in range(7, sections.__len__(), 2):
						this_notification.AddButton(sections[i])
					result = nt.SendNotification(this_notification)
				elif sections.__len__() == 7:
					icon_path = sections[5]
					this_notification.SetNotificationIcon(icon_path)
					result = nt.SendNotification(this_notification)
				elif sections.__len__() == 5:
					result = nt.SendNotification(this_notification)
				else:
					print _("Command format: notifyicon notification_title notification_text [notification_icon_path] [button names]*")
			elif command == "notify":
				if sections.__len__() < 5:
					print _("Wrong command")
					continue
				title = sections[1]
				text = sections[3]
				this_notification = Notification(notification_title = title, notification_text = text)
				if sections.__len__() >= 7:
					for i in range(5, sections.__len__(), 2):
						this_notification.AddButton(sections[i])
					result = nt.SendNotification(this_notification)
				elif sections.__len__() == 5:
					result = nt.SendNotification(this_notification)
				else:
					print _("Command format: notify notification_title notification_text [button_names]*")
			else:
				print _("Wrong command")
			if result != None:
				# print _("Response received.")
				print _("Service returned a notification object with the following fields:")
				for i in dir(result):
					if i[0] == "_" and i[1] == "_":
						continue
					else:
						print "\t%s:\t%s" % (i, getattr(result, i))
else:
	print _("This program is not meant to be loaded as a module.")
