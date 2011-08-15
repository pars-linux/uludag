#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4.QtCore import *

from ui_surveyItem import Ui_SurveyItemWidget
#from ui_detailWidget import Ui_DetailWidget 

import sys

class SurveyItem(QtGui.QListWidgetItem):

    def __init__(self, titleItem, parent):
        QtGui.QListWidgetItem.__init__(self, parent)

        self.titleItem = titleItem

class SurveyItemWidget(QtGui.QWidget):

    def __init__(self, titleItem, parent, item):
        QtGui.QWidget.__init__(self, None)

        self.ui = Ui_SurveyItemWidget()
        self.ui.setupUi(self)
        
        self.root = parent
        self.item = item
        self.titleItem = titleItem
        self.ui.label.setText(titleItem)
        