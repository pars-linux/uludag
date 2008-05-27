# Notifications are encapsulated into this class:
    
class Notification:
    def __init__(self, message_text = "Default notification text"):	
           self.text = message_text
           self.isReceived = False
