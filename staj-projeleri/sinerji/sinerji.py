#!/usr/bin/python
# -*- coding: utf-8 -*-

import dbus
import avahi
import os, sys, re 
from socket import gethostname

from dbus.mainloop.qt import DBusQtMainLoop
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_sinerjigui
import createsynergyconf
import parsesynergyconf
import avahiservices


class SinerjiGui(QDialog, ui_sinerjigui.Ui_SinerjiGui):
    def __init__(self,  parent=None):
        super(SinerjiGui, self).__init__(parent)
        self.setupUi(self)
        self.closeButton.setFocusPolicy(Qt.NoFocus)
        self.saveButton.setFocusPolicy(Qt.NoFocus)
        DBusQtMainLoop( set_as_default=True )
       
        self.discoveredHosts = set()
        
        self.confdomain = []
        self.confdomaintop = None
        self.confdomainbottom = None
        self.confdomainright = None
        self.confdomainleft = None

        self.connected = False
        self.browser = None
        self.bus = None


        self.startBrowsing()
        self.updateUi()
        self.topComboBox.addItem('')
        self.bottomComboBox.addItem('')
        self.rightComboBox.addItem('')
        self.leftComboBox.addItem('')



###############################################################
############           Gui Functions             ##############
###############################################################
    
    
####### ComboxBox Signals, if someone choose the host, deny it #######

    @pyqtSignature("QString")
    def on_topComboBox_activated(self, text):
        self.topComboBox.setEditable(True)
        if (text == gethostname()):
            QMessageBox.warning(self, u"Warning", u"The pc you have choosen is you own pc, please chose another pc")
            self.topComboBox.setCurrentIndex(0)

    @pyqtSignature("QString")
    def on_bottomComboBox_activated(self, text):
        self.bottomComboBox.setEditable(True)
        if (text == gethostname()):
            QMessageBox.warning(self, u"Warning", u"The pc you have choosen is you own pc, please chose another pc")
            self.bottomComboBox.setCurrentIndex(0)

    @pyqtSignature("QString")
    def on_rightComboBox_activated(self, text):
        self.rightComboBox.setEditable(True)
        if (text == gethostname()):
            QMessageBox.warning(self, u"Warning", u"The pc you have choosen is you own pc, please chose another pc")
            self.rightComboBox.setCurrentIndex(0)
    
    @pyqtSignature("QString")
    def on_leftComboBox_activated(self, text):
        self.leftComboBox.setEditable(True)
        if (text == gethostname()):
            QMessageBox.warning(self, u"Warning", u"The pc you have choosen is you own pc, please chose another pc")
            self.leftComboBox.setCurrentIndex(0)


### If Someone choose an empty string, dont store it, else createsynergyconf and parsesynergyconf wouldn't work well ###

    @pyqtSignature("")
    def on_saveButton_clicked(self):
        
        ### Add the current Hostnames from the ComboBoxes to the variable confdomain*, where * is the position
        if self.topComboBox.currentText() != '': 
            self.confdomaintop = ("top_bottom_%s" % self.topComboBox.currentText())
        if self.bottomComboBox.currentText() != '': 
            self.confdomainbottom = ("bottom_top_%s" % self.bottomComboBox.currentText())
        if self.rightComboBox.currentText() != '': 
            self.confdomainright = ("right_left_%s" % self.rightComboBox.currentText())
        if self.leftComboBox.currentText() != '': 
            self.confdomainleft = ("left_right_%s" % self.leftComboBox.currentText())
        
        ### Add the variables "confdomain*" to the list "confdomain"
        self.confdomain.append(self.confdomaintop)
        self.confdomain.append(self.confdomainbottom)
        self.confdomain.append(self.confdomainright)
        self.confdomain.append(self.confdomainleft)
        self.confdomain.append(u"host_host_%s" % gethostname())

        print self.connectingWorkstation.giveData(self.confdomaintop, self.confdomainbottom, self.confdomainright, self.confdomainleft)

        self.connectingWorkstation.announce()

        createsynergyconf.screens(self.confdomain)
        createsynergyconf.links(self.confdomain)
            
    @pyqtSignature("")
    def on_closeButton_clicked(self):
        self.reject()

        

## Only one checkbox has to be checked ##
    
    @pyqtSignature("")
    def on_serverButton_clicked(self):
        print "********* Server button is checked"

        print self.connectingWorkstation.getDomains()
        for domain in self.connectingWorkstation.getDomains():
            self.topComboBox.addItem(domain)
            self.bottomComboBox.addItem(domain)
            self.rightComboBox.addItem(domain)
            self.leftComboBox.addItem(domain)

        
    @pyqtSignature("")
    def on_clientButton_clicked(self):
        self.topComboBox.clear()
        self.bottomComboBox.clear()
        self.rightComboBox.clear()
        self.leftComboBox.clear()
        #self.connectingSinerji = avahiservices.avahiSinerji(gethostname(), "_sinerji._tcp")
        #self.connectingSinerji.connectDbus()
        #self.connectingSinerji.connectAvahi()
        #self.connectingSinerji.connect()
        print self.connectingSinerji.getSinerjiHost()
        for client in self.connectingSinerji.getClients():
            print client
            if client is None:
                pass
            else:
                if client[2] == gethostname():
                    if client[1] == "top":
                        self.topComboBox.addItem(self.connectingSinerji.getSinerjiHost())
                    elif client[1] == "bottom":
                        self.bottomComboBox.addItem(self.connectingSinerji.getSinerjiHost())
                    elif client[1] == "right":
                        print client[0], client[1], client[2]
                        self.rightComboBox.addItem(self.connectingSinerji.getSinerjiHost())
                    elif client[1] == "left":
                        self.leftComboBox.addItem(self.connectingSinerji.getSinerjiHost())
                    else:
                        QMessageBox.warning(self, u"No sharing", u"Nobody is sharing with you, please click on client mode for refresh")
                else:
                    pass


    def startBrowsing(self):
        self.connectingWorkstation = avahiservices.avahiSinerji(gethostname(), "_workstation._tcp")
        self.connectingSinerji = avahiservices.avahiSinerji(gethostname(), "_sinerji._tcp")
        self.connectingWorkstation.connectDbus()
        self.connectingWorkstation.connectAvahi()
        self.connectingWorkstation.connect() 

        #self.connectingSinerji.connectDbus()
        #self.connectingSinerji.connectAvahi()
        self.connectingSinerji.connect()


    def updateUi(self):
        if os.path.exists("synergy.conf"):
            self.parser = parsesynergyconf.parseSynergyConf("synergy.conf")
            for position in self.parser.getClients():
                if position[0] == "top":
                    self.topComboBox.insertItem(0, position[1])
                elif position[0] == "bottom":
                    self.bottomComboBox.insertItem(0, position[1])
                elif position[0] == "right":
                    self.rightComboBox.insertItem(0, position[1])
                elif position[0] == "left":
                    self.leftComboBox.insertItem(0, position[1])
                else:
                    pass
            
        
        
    #def save(self):
    #synergyconf.screens()


###############################################################
############                Main                 ##############
###############################################################


if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    form = SinerjiGui()
    form.show()
    app.exec_()


