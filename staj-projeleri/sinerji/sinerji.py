#!/usr/bin/python
# -*- coding: utf-8 -*-


import os, sys
import subprocess
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

        self.discoveredHosts = set()
        self.confdomain = []
        self.confdomaintop = None
        self.confdomainbottom = None
        self.confdomainright = None
        self.confdomainleft = None

        self.connected = False
        self.browser = None
        self.bus = None
        self.synergyConf = os.path.join(os.path.expanduser("~"), ".synergy.conf") 

        self.updateUi()
        self.topComboBox.addItem('')
        self.bottomComboBox.addItem('')
        self.rightComboBox.addItem('')
        self.leftComboBox.addItem('')

        ### Start browsing services, and looking for synergy.conf for parsing in updateUi
        self.startBrowsing()



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
        if self.serverButton.isChecked():

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


            ### Give data for _sinerji._tcp
            self.connectingWorkstation.giveData(self.confdomaintop, self.confdomainbottom, self.confdomainright, self.confdomainleft)

            ### Announce the _sinerji._tcp service.
            self.connectingWorkstation.announce()

            ### Creating the synergy.conf file
            createsynergyconf.screens(self.confdomain)
            createsynergyconf.links(self.confdomain)

            ## Starting synergys
            command = ['synergys', '--config', self.synergyConf]
            process = subprocess.call(command)


        elif self.clientButton.isChecked():
            
            address = self.connectingSinerji.getSinerjiAddress()
            command = ['synergyc', '-f', address]
            process = subprocess.call(command)

        else:
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

            
            ### Creating the synergy.conf file
            createsynergyconf.screens(self.confdomain)
            createsynergyconf.links(self.confdomain)


    @pyqtSignature("")
    def on_closeButton_clicked(self):
        self.reject()


## Only one checkbox has to be checked ##

    @pyqtSignature("")
    def on_serverButton_clicked(self):
        print "********* Server button is checked"
        ### Clear the boxes 

        self.topComboBox.clear()
        self.bottomComboBox.clear()
        self.rightComboBox.clear()
        self.leftComboBox.clear()
        
        self.topComboBox.addItem("")
        self.rightComboBox.addItem("")
        self.bottomComboBox.addItem("")
        self.leftComboBox.addItem("")
        ### Add the hostnames that we get from browsing _workstation._tcp to the comboBoxes
        for domain in self.connectingWorkstation.getDomains():
            self.topComboBox.addItem(domain)
            self.bottomComboBox.addItem(domain)
            self.rightComboBox.addItem(domain)
            self.leftComboBox.addItem(domain)


    @pyqtSignature("")
    def on_clientButton_clicked(self):
        print "********* Client button is checked"
        ### Clear the boxes 
        self.topComboBox.clear()
        self.bottomComboBox.clear()
        self.rightComboBox.clear()
        self.leftComboBox.clear()

        ### Get the clients from the _sinerji._tcp service
        for client in self.connectingSinerji.getClients():
            if client is None:
                pass
            else:
                if client[2] == gethostname(): ### We are looking for our hostname
                    if client[1] == "top":
                        self.topComboBox.addItem(self.connectingSinerji.getSinerjiHost())
                        self.address = self.connectingSinerji.getSinerjiAddress()
                    elif client[1] == "bottom":
                        self.bottomComboBox.addItem(self.connectingSinerji.getSinerjiHost())
                        self.address = self.connectingSinerji.getSinerjiAddress()
                    elif client[1] == "right":
                        self.rightComboBox.addItem(self.connectingSinerji.getSinerjiHost())
                        self.address = self.connectingSinerji.getSinerjiAddress()
                    elif client[1] == "left":
                        self.leftComboBox.addItem(self.connectingSinerji.getSinerjiHost())
                        self.address = self.connectingSinerji.getSinerjiAddress()
                    else:
                        QMessageBox.warning(self, u"No sharing", u"Nobody is sharing with you, please click on client mode for refresh")
                else:
                    pass


    def startBrowsing(self):
        ## Create instances of avahiSinerji for each service
        self.connectingWorkstation = avahiservices.avahiSinerji(gethostname(), "_workstation._tcp")
        self.connectingSinerji = avahiservices.avahiSinerji(gethostname(), "_sinerji._tcp")

        ## Connecting to dbus and avahi,
        self.connectingWorkstation.connectDbus()
        self.connectingWorkstation.connectAvahi()
        ## Starting searching for domain for _workstation._tcp and _sinerji._tcp. 
        self.connectingWorkstation.connect()
        self.connectingSinerji.connect()


    def updateUi(self):
        ### Look for synergy.conf, if exists parse it and fill the comboBoxes
        if os.path.exists(self.synergyConf):
            self.parser = parsesynergyconf.parseSynergyConf(self.synergyConf)
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Sinerji")
    app.setWindowIcon(QIcon("style.png"))
    DBusQtMainLoop( set_as_default=True )
    form = SinerjiGui()
    form.show()
    app.exec_()


