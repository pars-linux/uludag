#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json

from PyQt4 import QtGui
from PyQt4.QtCore import *

from myWidgets import SurveyItem,SurveyItemWidget
from ui_mainMenu import Ui_mainManager

class MainManager(QtGui.QWidget):
    def __init__(self, parent, standAlone=True):
        QtGui.QWidget.__init__(self, parent)

	self.ui = Ui_mainManager()

	if standAlone:
            self.ui.setupUi(self)
        else:
            self.ui.setupUi(parent)

       
        self.widgets = {}
	
	json_object =  open('user_studies.json','r')
	self.data = json.load(json_object)
	json_object.close()
	
		
        for survey in self.data["pardusUserStudyList"]:
            item = SurveyItem(survey["title"], self.ui.surveyList)
            item.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
            item.setSizeHint(QSize(38,48))
	    self.widgets[survey["id"]] = SurveyItemWidget(survey["title"], self, item)
            self.ui.surveyList.setItemWidget(item, self.widgets[survey["id"]])
            
        self.connect(self.ui.alwaysHelp, SIGNAL("clicked()"), self.setGlobalParticipation)
        self.connect(self.ui.askToHelp, SIGNAL("clicked()"), self.setGlobalParticipation)
	self.connect(self.ui.rejectHelp, SIGNAL("clicked()"), self.setGlobalParticipation)
            
    def setGlobalParticipation(self):
	json_data =  open('user_studies.json','r')
	self.data = json.load(json_data)
	json_data.close()
	
	if self.ui.alwaysHelp.isChecked() == True:
	  self.data["userParticipation"] = "Always Join" 
	elif self.ui.askToHelp.isChecked() == True:
	  self.data["userParticipation"] = "Ask Before Join" 
	else :
	  self.data["userParticipation"] = "Do not Join" 
	
	f = open('user_studies2.json','w')
	string = json.dump(self.data,f, indent = 2)
	f.close()
	
	
	  
	
