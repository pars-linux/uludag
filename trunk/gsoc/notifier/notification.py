# Import internationalization support:
import gettext
_ = gettext.translation("notman", "./i18n", fallback = True).ugettext

# Notifications are encapsulated into this class:
    
class Notification:
    def __init__(self, message_text = _("Default notification text")):	
           self.text = message_text
           self.isReceived = False
