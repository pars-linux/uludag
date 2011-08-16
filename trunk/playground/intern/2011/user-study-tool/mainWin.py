#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json

from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4 import QtWebKit

from pds.gui import *

from myWidgets import SurveyItem,SurveyItemWidget
from ui_mainMenu import Ui_mainManager
from ui_detailWidget import Ui_InfoWidget 

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
	
	self.info = UserStudyItemInfo(self.ui.surveyList)
		
        for survey in self.data["pardusUserStudyList"]:
            item = SurveyItem(survey["title"], self.ui.surveyList)
            item.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
            item.setSizeHint(QSize(38,48))
            item.url = QUrl(survey["url"])
	    w = SurveyItemWidget(survey["title"], self, item, self.ui.surveyList)
	   
	    self.widgets[survey["id"]] = w
            self.ui.surveyList.setItemWidget(item, self.widgets[survey["id"]])
            self.connect(w.ui.infoButton, SIGNAL("clicked()"), w.showDescription)
            
           
            
        self.connect(self.ui.alwaysHelp, SIGNAL("clicked()"), self.setGlobalParticipation)
        self.connect(self.ui.askToHelp, SIGNAL("clicked()"), self.setGlobalParticipation)
	self.connect(self.ui.rejectHelp, SIGNAL("clicked()"), self.setGlobalParticipation)
	
	#self.connect(self.ui.surveyList, SIGNAL("itemSelectionChanged()"),self.showDescription)
	#self.info.clicked.connect(self.hideDescription)
	
	
            
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
	
    def showDescription(self, url):
	self.info.ui.webView.load(url)
	self.info.resize(self.ui.surveyList.size())
	self.info.animate(start = MIDLEFT, stop = MIDCENTER)
	QtGui.qApp.processEvents()
	
    

class UserStudyItemInfo(PAbstractBox):
  
    def __init__(self, parent):
	PAbstractBox.__init__(self, parent)
	
	self.ui = Ui_InfoWidget()
	self.ui.setupUi(self)
	
        self.ui.webView = DetailPage(self, self)
        self.ui.gridLayout.addWidget(self.ui.webView, 0, 0, 1, 1)
	
	self._animation = 2
	self._duration = 500
	
	self.enableOverlay()
	self.hide()
	
   
class DetailPage(QtWebKit.QWebView):
    def __init__(self, parent,  pdsWidget):
	QtWebKit.QWebView.__init__(self, parent)
	self.pdsWidget = pdsWidget
	
    def mousePressEvent(self, event):
	if self.isVisible():
	    self.pdsWidget.animate(start = MIDCENTER,
			stop  = MIDRIGHT,
			direction = OUT)
	
	
	
    
	
	
	
	  
	
