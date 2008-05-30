# Import internationalization support:
import gettext
_ = gettext.translation("notman", "./i18n", fallback = True).ugettext

# Notifications are encapsulated into this class:
    
class Notification:
	def __init__(self, message_text = _("Default notification text")):
		self.text = message_text
		self.isReceived = False		

	def Pack(self):
		# For multi-platform compatibility send the text with utf-8 no matter what:
		self.text = self.text.encode("utf-8")
		
	def Unpack(self):
		# Convert the text back to its natural encoding:
		self.text = self.text.decode("utf-8")
