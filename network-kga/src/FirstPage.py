import FirstWidget
from NetworkKga import *

class FirstPage(FirstWidget.FirstWidget):
    def __init__(self):
        FirstWidget.FirstWidget.__init__(self)
        self.directConnectionIcon.setPixmap(loadIcon("network"))
        self.wirelessConnectionIcon.setPixmap(loadIcon("wireless"))
        self.dialupConnectionIcon.setPixmap(loadIcon("dialup"))
