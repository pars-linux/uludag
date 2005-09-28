import FirstWidget
from NetworkKga import *

class FirstPage(FirstWidget.FirstWidget):
    def __init__(self):
        FirstWidget.FirstWidget.__init__(self)
        self.directConnectionIcon.setPixmap(loadIcon("network"))
        self.wirelessConnectionIcon.setPixmap(loadIcon("wireless"))
        self.dialupConnectionIcon.setPixmap(loadIcon("dialup"))
        self.currentWidget = ''

    def resetWidgetColors(self):
        if self.currentWidget.startswith('direct'):
            self.directConnectionLabelTop.setBackgroundMode(Qt.PaletteBackground)
            self.directConnectionLabel.setBackgroundMode(Qt.PaletteBackground)
        elif self.currentWidget.startswith('wireless'):
            self.wirelessConnectionLabelTop.setBackgroundMode(Qt.PaletteBackground)
            self.wirelessConnectionLabel.setBackgroundMode(Qt.PaletteBackground)
        elif self.currentWidget.startswith('dialup'):
            self.dialupConnectionLabelTop.setBackgroundMode(Qt.PaletteBackground)
            self.dialupConnectionLabel.setBackgroundMode(Qt.PaletteBackground)
        
    def mousePressEvent(self,event):
        widget = self.childAt(event.pos())

        if not widget:
            pass
        else:
            name = widget.name()
            if self.currentWidget.startswith(name):
                pass
            elif name and event.button() & Qt.LeftButton:
                if name.startswith('direct'):
                    self.resetWidgetColors()
                    self.currentWidget = 'directConnectionLabelTop'
                    self.directConnectionLabelTop.setBackgroundMode(Qt.PaletteHighlight)
                    self.directConnectionLabel.setBackgroundMode(Qt.PaletteLight)
                elif name.startswith('wireless'):
                    self.resetWidgetColors()
                    self.currentWidget = 'wirelessConnectionLabelTop'
                    self.wirelessConnectionLabelTop.setBackgroundMode(Qt.PaletteHighlight)
                    self.wirelessConnectionLabel.setBackgroundMode(Qt.PaletteLight)
                elif name.startswith('dialup'):
                    self.resetWidgetColors()
                    self.currentWidget = 'dialupConnectionLabelTop'
                    self.dialupConnectionLabelTop.setBackgroundMode(Qt.PaletteHighlight)
                    self.dialupConnectionLabel.setBackgroundMode(Qt.PaletteLight)

        FirstWidget.FirstWidget.mousePressEvent(self,event)
