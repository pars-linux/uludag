# Imports:
import pickle
# Import internationalization support:
import gettext
_ = gettext.translation("notman", "./i18n", fallback = True).ugettext
# Import D-Bus bindings:
import dbus
# Import Notification class definition:
from notification import *

class Notifier:
    def __init__(self):
        self.session_bus = dbus.SessionBus()
        self.notification_manager_proxy = self.session_bus.get_object("org.pardus.notificationmanager", "/NotificationManager")
        self.iface = dbus.Interface(self.notification_manager_proxy, "org.pardus.notmanxface")

    def Echo(self,  message_string):
        return self.iface.EchoSender(message_string)
    
    def SendNotification(self,  notification):
    	notification.Pack()
        pickled_notification = pickle.dumps(notification)
        pickled_result = self.iface.AddNotification(pickled_notification)
        notification = pickle.loads(pickled_result.__str__())
        return True
    
    def SendExitSignal(self):
        self.iface.Exit()
