# Import internationalization support:
import gettext
_ = gettext.translation("notman", "./i18n", fallback = True).ugettext

# Notifications are encapsulated into this class:
    
class Notification:
	def __init__(self, notification_title = _("New Notification!"), notification_text = _("Default notification text"), notification_icon_path = "./icons/notif.png"):
		self.notification_title = notification_title
		self.notification_text = notification_text
		self.notification_icon_path = notification_icon_path
		self.isReceived = False		

	def Pack(self):
		# For multi-platform compatibility send the text with utf-8 no matter what:
		self.notification_title = self.notification_title.encode("utf-8")
		self.notification_text = self.notification_text.encode("utf-8")
		self.notification_icon_path = self.notification_icon_path.encode("utf-8")
		
	def Unpack(self):
		# Convert the text back to its natural encoding:
		self.notification_title = self.notification_title.encode("utf-8")
		self.notification_text = self.notification_text.decode("utf-8")
		self.notification_icon_path = self.notification_icon_path.encode("utf-8")
