#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_sinerjigui
import sinerjiAvahi
import os, sys

class SinerjiGui(QDialog, ui_sinerjigui.Ui_SinerjiGui):
    def __init__(self,  parent=None):
        super(SinerjiGui, self).__init__(parent)
        self.setupUi(self)
        self.cancelButton.setFocusPolicy(Qt.NoFocus)
        self.savequitButton.setFocusPolicy(Qt.NoFocus)
        self.browser = None

## ComboBox signals ##

    @pyqtSignature("Double")
    def on_topComboBox_currentIndexChanged(self, text):
        self.updateUi()
    
    @pyqtSignature("Double")
    def on_bottomComboBox_currentIndexChanged(self, text):
        self.updateUi()
    
    @pyqtSignature("Double")
    def on_rightComboBox_highlighted(self, text):
        self.updateUi()
    
    @pyqtSignature("Double")
    def on_leftComboBox_activated(self, text):
        self.updateUi()

## Savequit and Cancel button signals ##

    @pyqtSignature("")
    def on_cancelButton_clicked(self):
        self.reject()
    
    @pyqtSignature("")
    def on_savequitButton_clicked(self):
        self.save()  #Our custom function

## Only one checkbox has to be checked ##
    
    @pyqtSignature("")
    def on_serverBox_clicked(self):
        self.clientBox.toggle()
        self.browser = sinerjiAvahi.SinerjiAvahi('_workstation._tcp')
        print self.browser.get_domains() ## Test 
        for domain in self.browser.get_domains():
            self.topComboBox.addItem(domain.rstrip())
            self.bottomComboBox.addItem(domain.rstrip())
            self.rightComboBox.addItem(domain.rstrip())
            self.leftComboBox.addItem(domain.rstrip())
        self.updateUi()

    @pyqtSignature("")
    def on_clientBox_clicked(self):
        self.serverBox.toggle()
        self.browser = sinerjiAvahi.SinerjiAvahi('_sinerji._tcp')

## Main code ##
    def updateUi(self):
        print "Buraasdas"
    
    #def save(self):
    #     #Some code ...

   
if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    form = SinerjiGui()
    form.show()
    #sinerjiAvahi.browseDomain()
    #sinerjiAvahi.addService()
    app.exec_()
