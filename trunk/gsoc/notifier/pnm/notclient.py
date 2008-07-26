#!/usr/bin/env python

# Imports:
import pickle
# Import internationalization support:
import gettext
_ = gettext.translation("notman", fallback = True).ugettext
# Import D-Bus bindings:
import dbus
# Import Notification class definition:
from notification import *

class Notifier:
	def __init__(self, mainloopType = None):
		# Required to make async calls:
		if mainloopType == "qt":
			from dbus.mainloop.qt import DBusQtMainLoop
			DBusQtMainLoop(set_as_default = True)	
		elif mainloopType == "glib":
			from dbus.mainloop.glib import DBusGMainLoop
			DBusGMainLoop(set_as_default = True)
		self.session_bus = dbus.SessionBus()
		self.notification_manager_proxy = self.session_bus.get_object("org.pardus.notificationmanager", "/NotificationManager")
		self.iface = dbus.Interface(self.notification_manager_proxy, "org.pardus.notmanxface")

	def Echo(self, message_string):
		return self.iface.EchoSender(message_string)

	# If the reply_callback argument is given, an asynchronous call is made, and the given python callable reply_callback is called when the call is completed.
	# The reply_callback is called with the notification instance updated by the manager as its argument.
	# Following the same logic, error_callback is called when an error happens during the call.
	# If these arguments are not given, the call is blocking (it waits until the call receives a reply from the notification manager).
	# Blocking calls return the notification instance updated with (any) changes that the manager did to the instance.

	#################################################################################################################
	#																												#
	#  IMPORTANT NOTE: YOU CAN ONLY MAKE ASYNC CALLS IF YOUR APPLICATION IS CONNECTED TO A MAIN LOOP (GLIB OR QT)	#
	#																												#
	#################################################################################################################
	def SendNotification(self, notification, reply_callback = None, error_callback = None):
		notification.Pack()
		pickled_notification = pickle.dumps(notification)
		if reply_callback == None:
			pickled_result = self.iface.AddNotification(pickled_notification)
			notification = pickle.loads(pickled_result.__str__())
			notification.Unpack()
			return notification
		else:
			def reply_callback_wrapper(pickled_answer):
				notification = pickle.loads(pickled_answer.__str__())
				notification.Unpack()
				return reply_callback(notification)
			self.iface.AddNotification(pickled_notification, reply_handler = reply_callback_wrapper, error_handler = error_callback)

	def SendExitSignal(self):
		self.iface.Exit()
