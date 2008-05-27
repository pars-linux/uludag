#!/usr/bin/python
    
# Import required python libraries:
import sys
import pickle
import time
# Import D-Bus bindings:
import dbus
import dbus.service
# Import Qt main loop stuff:
from dbus.mainloop.qt import DBusQtMainLoop
DBusQtMainLoop(set_as_default = True)
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
				print "Waited for %s seconds, no notification waiting in queue, will die gracefully." % self.notification_manager.lifespan
				# Exit the Qt4 main loop:
				self.notification_manager.quit()
				break
    
class NotificationManager(QApplication):
    def __init__(self,  object_path):
        QApplication.__init__(self,  sys.argv)
        print "Initializing notification manager..."
        self.object_path = object_path
        self.session_bus = dbus.SessionBus()
        self.bus_name = dbus.service.BusName("org.pardus.notificationmanager", self.session_bus)
        # Initialize the pending message queue:
        self.message_queue = []
        self.lifespan = 15.0
        self.last_notification_time = time.time()
        # Initialize the timer:
        self.timer = Timer(self)
        # Initialize the notification displayer (spawned in a new thread):
        self.notification_displayer = NotificationDisplayer()
        # Signal handlers:
        self.connect(self, QtCore.SIGNAL("handleEvent()"), self.HandleNotification)
        self.connect(self, QtCore.SIGNAL("exitProgram()"), self.Die)
    
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
            print "Handling notification with text: %s" % self.message_queue[0].text
            self.notification_displayer.DisplayNotification(self.message_queue[0])
            self.message_queue = self.message_queue[1:]
            print "Queue state: %s" % self.message_queue

class NotXFace(dbus.service.Object):
    def __init__(self, notification_manager):
        print "Initializing / exporting NotXFace object..."
        dbus.service.Object.__init__(self, notification_manager.bus_name, notification_manager.object_path)
        self.notification_manager = notification_manager
        
    @dbus.service.method(dbus_interface = "org.pardus.notmanxface", in_signature = "s", out_signature = "s", sender_keyword = "sender")
    def AddNotification(self, serialized_notification, sender = None):
        try:
            # Try unpickling the serialized notification:
            notification = pickle.loads(serialized_notification.__str__())
        except:
            # If an error occurs while unpickling serialized notification, notify the requestor of it:
            notification = Notification("Couldn't unpickle sent notification")
            return pickle.dumps(notification)
        else:
            # Append the notification to the queue of the notification manager:
            self.notification_manager.message_queue.append(notification)
            print "Notification successfully received. Sender's bus name: %s" % sender
            print "Received message text: %s" % notification.text
            print "Added notification to queue."
            # Handle the notification in the other thread (in case handling the notification takes too much time, we dont want to stall the requestor):
            self.notification_manager.emit(QtCore.SIGNAL("handleEvent()"))
            # Update the last notification timestamp of the notification manager:
            self.notification_manager.last_notification_time = time.time()
            # Return the notification to the requestor, acknowledging that the notification is received:
            notification.isReceived = True
            return pickle.dumps(notification)
        
    @dbus.service.method(dbus_interface = "org.pardus.notmanxface", in_signature = "s", out_signature = "s", sender_keyword = "sender")
    def EchoSender(self, message_string, sender = None):
        print "Echo request received. Sender's bus name: %s" % sender
        print "Text to be echoed: %s" % message_string
        return "Echoing: %s" % message_string
        
    @dbus.service.method(dbus_interface = "org.pardus.notmanxface", in_signature = "", out_signature = "", sender_keyword = "sender")
    def Exit(self, sender = None):
        print "Sender's bus name: %s" % sender
        print "Exit method called, exiting service..."
        self.notification_manager.emit(QtCore.SIGNAL("exitProgram()"))
 
class NotXFaceThread(QtCore.QThread):
    def __init__(self,  notification_manager):
        QtCore.QThread.__init__(self)
        self.notification_manager = notification_manager
    
    def run(self):
        self.exported_obj = NotXFace(self.notification_manager)
        self.exec_()

# If executed as the main program:
if __name__ == "__main__":
    notification_manager = NotificationManager("/NotificationManager")
    notxfacethread = NotXFaceThread(notification_manager)
    notxfacethread.start()
    notification_manager.Go()
    print "Exited successfully."
else:
    print "This thing is not meant to be loaded as a module."
    
