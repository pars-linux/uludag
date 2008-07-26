#!/usr/bin/env python
    
# Import required basic python libraries:
import sys
import pickle
import time
import copy
# Import internationalization support:
import gettext
_ = gettext.translation("notman", fallback = True).ugettext
# Import D-Bus bindings:
import dbus
import dbus.service
# Import Qt main loop stuff:
from dbus.mainloop.qt import DBusQtMainLoop
import PyQt4.QtCore
from PyQt4.QtGui import QApplication

# Import header that specifies notification class
from notification import *

# Import notification handler (displayer module):
from notdisplayer import *

class Timer(QtCore.QThread):
	def __init__(self, notification_manager):
		QtCore.QThread.__init__(self)
		self.notification_manager = notification_manager
	
	def run(self):
		# If the notification queue is not empty or the manager's lifespan is not over contrinue running. Else, exit gracefully:
		timewait = self.notification_manager.lifespan
		while True:
			self.msleep(int(timewait * 1000))
			timewait = self.notification_manager.lifespan - time.time() + self.notification_manager.last_notification_time
			if self.notification_manager.message_queue != []:
				timewait = self.notification_manager.lifespan
				continue
			elif timewait > 0:
				continue
			else:
				print _("Waited for %s seconds, no notification waiting in queue, will die gracefully.") % self.notification_manager.lifespan
				# Exit the Qt4 main loop:
				self.notification_manager.quit()
				break
    
class NotificationManager(QApplication):
	def __init__(self):
		QApplication.__init__(self,  sys.argv)
		print _("Initializing notification manager...")
		# We don't want the program to get closed when there is no visible notificaition window:
		self.setQuitOnLastWindowClosed(False)
		# Initialize the pending message queue:
		self.message_queue = []
		self.lifespan = 15.0
		self.last_notification_time = time.time()
		# Initialize the timer:
		self.timer = Timer(self)
		# Initialize the notification displayer:
		self.notification_displayer = NotificationDisplayer()    

	def Die(self):
		QtCore.QTimer().singleShot(1000,  quit)
		
	def Go(self):        
		# Start the timer (spawned in its own thread):
		self.timer.start()
		# Start the Qt4 main loop:
		self.exec_()

	def HandleNotification(self):
		# If the notification queue is not empty, handle the first notification in the queue:
		if self.message_queue != []:
			# Debug line:
			# print _("Handling notification with text: %s") % self.message_queue[0].notification_text
			self.notification_displayer.DisplayNotification(self.message_queue[0])
			self.message_queue = self.message_queue[1:]
			print _("Queue state: %s") % self.message_queue

	def SetNotificationSignalHandler(self, signal_source):
		self.connect(signal_source, QtCore.SIGNAL("handleNotification()"), self.HandleNotification)

	def SetExitSignalHandler(self, signal_source):
		self.connect(signal_source, QtCore.SIGNAL("exitProgram()"), self.Die)

class NotXFace(dbus.service.Object):
	def __init__(self, notification_manager, notxfacethread):
		dbus.service.Object.__init__(self, notxfacethread.bus_name, notxfacethread.object_path)
		print _("Initializing / exporting NotXFace object...")
		self.notification_manager = notification_manager
		self.notxfacethread = notxfacethread
	
	# This method checks if the incoming notification is bundled with any buttons or not.
	# If it is, the method does not return immediately but waits until the user presses a button (async mode).
	# When the user presses a button, the index of the pressed button is recorded in the chosen_button field of the incoming notification and the notification object is sent back to the notification sender.

	# If the notification is not bundled with any buttons, the method return immediately (sync mode) with chosen_button field set to -1.
	@dbus.service.method(dbus_interface = "org.pardus.notmanxface", async_callbacks = ("report", "report_error"), in_signature = "s", out_signature = "s", sender_keyword = "sender")
	def AddNotification(self, serialized_notification, report, report_error, sender = None):
		try:
			# Try unpickling the serialized notification:
			notification = pickle.loads(serialized_notification.__str__())
		except:
			# If an error occurs while unpickling serialized notification, notify the requestor of it:
			notification_response = Notification(_("Couldn't unpickle sent notification"))
			return pickle.dumps(notification_reponse)
		else:
			# Make a copy of the received notification to send as the response:
			notification_response = copy.deepcopy(notification)
			# Acknowledge that the notification is received:
			notification_response.isReceived = True
			# Unpack the received notification:
			notification.Unpack()
			# Set the reporting callable (= async return callable) of the notification:
			if notification.buttons != []:
				notification.SetReporterCallable(report, notification_response)
			# Append the notification to the queue of the notification manager:			
			self.notification_manager.message_queue.append(notification)
			print _("Notification successfully received. Sender's bus name: %s") % sender
			print _("Received message text: %s") % notification.notification_text
			print _("Added notification to queue.")
			# Handle the notification in the other thread (in case handling the notification takes too much time, we dont want to stall the whole dbus listener):
			self.notxfacethread.emit(QtCore.SIGNAL("handleNotification()"))
			# Update the last notification timestamp of the notification manager:
			self.notification_manager.last_notification_time = time.time()
			# If the notification is not bundled with any buttons, return immediately:
			if notification.buttons == []:
				report(pickle.dumps(notification_response))
			# If it is, the displayer will call the reporting callable.

	@dbus.service.method(dbus_interface = "org.pardus.notmanxface", in_signature = "s", out_signature = "s", sender_keyword = "sender")
	def EchoSender(self, message_string, sender = None):
		print _("Echo request received. Sender's bus name: %s") % sender
		print _("Text to be echoed: %s") % message_string
		return _("Echoing: %s") % message_string
        
	@dbus.service.method(dbus_interface = "org.pardus.notmanxface", in_signature = "", out_signature = "", sender_keyword = "sender")
	def Exit(self, sender = None):
		print _("Sender's bus name: %s") % sender
		print _("Exit method called, exiting service...")
		self.notxfacethread.emit(QtCore.SIGNAL("exitProgram()"))

class NotXFaceThread(QtCore.QThread):
	def __init__(self, notification_manager, object_path):
		QtCore.QThread.__init__(self)
		self.notification_manager = notification_manager
		self.object_path = object_path

	def run(self):
		DBusQtMainLoop(set_as_default = True)
		self.session_bus = dbus.SessionBus()
		self.bus_name = dbus.service.BusName("org.pardus.notificationmanager", self.session_bus)
		self.exported_obj = NotXFace(self.notification_manager, self)
		self.exec_()

# If executed as the main program:
if __name__ == "__main__":
	# Create the notification manager object (which is a QApplication that manages the GUI thread):
	notification_manager = NotificationManager()
	# Create the thread containing the notification manager DBus interface object:
	notxfacethread = NotXFaceThread(notification_manager, "/NotificationManager")
	# Set the signal handlers of the main thread so that it can receive signals from the DBus interface thread:
	notification_manager.SetNotificationSignalHandler(notxfacethread)
	notification_manager.SetExitSignalHandler(notxfacethread)
	# Launch up the DBus interface thread:
	notxfacethread.start()
	# Launch up the main (GUI) thread:
	notification_manager.Go()
	print _("Exited successfully.")
else:
	print _("This program is not meant to be loaded as a module.")
    
