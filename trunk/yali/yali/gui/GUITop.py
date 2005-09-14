# -*- coding: utf-8 -*-

from qt import *

import GUIStage

##
# Top widget
class Widget(QWidget):

    def __init__(self, *args):
        apply(QWidget.__init__, (self,) + args)
        
        self.img = QImage("pics/top_image.png")

        self.stageWidget = GUIStage.Widget(self)

        top = QHBoxLayout(self)
        top.setMargin(10)
        top.addStretch(1)
        top.addWidget(self.stageWidget)

        # TESTING
        self.setFixedHeight(110)
#         f = self.font()
#         f.setBold(True)
#         f.setPointSize(30)
#         self.setFont(f)
#         self.setText("Pardus 1.0")
#         # END TEST

    def addStage(self, num, text):
        self.stageWidget.addStage(num, text)

    def paintEvent(self, e):
        # FIXME: We should also change the widget's height regarding
        # the original image to scale properly.
        img = self.img.smoothScale(self.size())
        self.setPaletteBackgroundPixmap(QPixmap(img))
