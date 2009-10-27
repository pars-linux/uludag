#!/usr/bin/env python

# Import internationalization support:
import gettext
_ = gettext.translation("notman", fallback = True).ugettext

# Notifications are encapsulated into this class:
    
class Notification:
	def __init__(self, notification_title = _("New Notification!"), notification_text = _("Default notification text"), notification_icon_path = "./icons/notif.png"):
		self.notification_title = notification_title
		self.notification_text = notification_text
		self.notification_icon_path = notification_icon_path
		# Notifications do not have default buttons:
		self.buttons = []
		self.isReceived = False
		# The chosen button field will reflect the index of the chosen button (when the notification is sent back after getting processed by the notification manager). -1 will mean that the user has not pressed any.
		self.chosen_button = -1
		# The fields below this line are not intended for use by the users of this software.
		# They are used by the Notifier, NotificationManager and NotificationDisplayer implementations.
		self.reporter = None
		self.notification_response = None

	def SetNotificationIcon(self, new_icon_path):
		self.notification_icon_path = new_icon_path
	
	def AddButton(self, button_text, icon_path = None):
		self.buttons.append((button_text, icon_path))

	# The following methods are not intended for use by the users of this software.
	# They are used by the Notifier, NotificationManager and NotificationDisplayer implementations.

	def Pack(self):
		# For multi-platform compatibility send the text with utf-8 no matter what:
		self.notification_title = self.notification_title.encode("utf-8")
		self.notification_text = self.notification_text.encode("utf-8")
		self.notification_icon_path = self.notification_icon_path.encode("utf-8")
		for i in range(self.buttons.__len__()):
			if self.buttons[i][1] != None:
				self.buttons[i] = (self.buttons[i][0].encode("utf-8"), self.buttons[i][1].encode("utf-8"))
			else:
				self.buttons[i] = (self.buttons[i][0].encode("utf-8"), None)

	def Unpack(self):
		# Convert the text back to its natural encoding:
		self.notification_title = self.notification_title.decode("utf-8")
		self.notification_text = self.notification_text.decode("utf-8")
		self.notification_icon_path = self.notification_icon_path.decode("utf-8")
		for i in range(self.buttons.__len__()):
			if self.buttons[i][1] != None:
				self.buttons[i] = (self.buttons[i][0].decode("utf-8"), self.buttons[i][1].decode("utf-8"))
			else:
				self.buttons[i] = (self.buttons[i][0].decode("utf-8"), None)

	def SetReporterCallable(self, callable, notification_response):
		self.reporter = callable
		self.notification_response = notification_response

