#!/usr/bin/python
# -*- coding: utf-8 -*-


import os, sys
import subprocess, signal
from socket import gethostname
from dbus.mainloop.qt import DBusQtMainLoop
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_sinerjigui
import createsynergyconf
import parsesynergyconf
import avahiservices
import platform
import qrc_resources
__version__ = 0.1


class SinerjiGui(QDialog, ui_sinerjigui.Ui_SinerjiGui):
    def __init__(self,  parent=None):
        super(SinerjiGui, self).__init__(parent)
        self.setupUi(self)
        self.closeButton.setFocusPolicy(Qt.NoFocus)
        self.applyButton.setFocusPolicy(Qt.NoFocus)

        self.trayIcon = QSystemTrayIcon(QIcon(":/icon.png"), self)
        self.trayActions()
        self.trayIcon.setContextMenu(self.trayMenu)
        self.trayIcon.setToolTip(u"Sinerji")
        self.trayIcon.show()

        self.applyButton.setIcon(QIcon(":/buttonApply.png"))
        self.closeButton.setIcon(QIcon(":/buttonClose.png"))
        self.discoveredHosts = set()
        self.txtData = []
        self.confdomain = []
        self.synergycData = {}
        self.connected = False
        self.browser = None
        self.bus = None
        self.filled = None
        self.searched = None
        self.clientState = None
        self.clientAndPos = []
        self.serverAndIp = []
        self.synergyConf = os.path.join(os.path.expanduser("~"), ".synergy.conf") 
        
        self.startBrowsing()
        self.updateUi()
        
        self.topComboBox.addItem('')
        self.bottomComboBox.addItem('')
        self.rightComboBox.addItem('')
        self.leftComboBox.addItem('')
        ### Start browsing services, and looking for synergy.conf for parsing in updateUi

##################################################################
##################################################################
##################################################################
    
    def trayActions(self):
        self.trayMenu = QMenu()
        
        self.actionAbout = QAction(QIcon(":/about.png"),u"About", self)
        self.connect(self.actionAbout, SIGNAL("activated()"), self.about)
        self.trayMenu.addAction(self.actionAbout)
        
        self.trayMenu.addSeparator()
        
        self.actionQuit = QAction(QIcon(":/quit.png"),u"Quit", self)
        self.connect(self.actionQuit, SIGNAL("activated()"), app.quit)
        self.trayMenu.addAction(self.actionQuit)

    def about(self):
        QMessageBox.about(self, "About Sinerji",
             """<b>Sinerji</b> v %s
             <p>Developer: Fatih Arslan  E-mail: ftharsln@gmail.com     
             <p>This application is a fronted to the program Synergy
             <p>It uses avahi as backed for an easy configure experience
             <p>Python %s - Qt %s - PyQt %s on %s""" % (
             __version__, platform.python_version(),
             QT_VERSION_STR, PYQT_VERSION_STR, platform.system()))

    def searchClient(self):
        self.connect(self.trayIcon, SIGNAL("messageClicked()"), self.fillClientBox)
        for server in self.connectingSinerji.getClients().keys():
            for client in self.connectingSinerji.getClients()[server]:
                self.clientAndPos = client.split("=")
            self.serverAndIp = server.split("=")

        if self.serverAndIp[0] is None:
            pass
        else:
            if self.clientAndPos[1] == gethostname(): ### We are looking for our hostname
                    self.trayIcon.showMessage("Sinerji", 
                            ("%s want to use your pc from %s. To allow please click" % (self.serverAndIp[0],self.clientAndPos[0])), 
                            QSystemTrayIcon.Information, 
                            8000)
        self.searched = True
    
    def fillClientBox(self):

        print "********* Client button is checked"
        ### Clear the boxes 
        self.topComboBox.clear()
        self.bottomComboBox.clear()
        self.rightComboBox.clear()
        self.leftComboBox.clear()

        ### Get the clients from the _sinerji._tcp service
        for server in self.connectingSinerji.getClients().keys():
            for client in self.connectingSinerji.getClients()[server]:
                clientAndPos = client.split("=")
            serverAndIp = server.split("=")
            if serverAndIp[0] is None:
                pass
            else:
                if clientAndPos[1] == gethostname(): ### We are looking for our hostname
                    if clientAndPos[0] == "bottom": # If client is bottom, than our server is top, that's why we add it to topCombobox
                        self.topComboBox.addItem(serverAndIp[0])
                        self.synergycData[serverAndIp[0]] = serverAndIp[1]
                    elif clientAndPos[0] == "top":
                        self.bottomComboBox.addItem(serverAndIp[0])
                        self.synergycData[serverAndIp[0]] = serverAndIp[1]
                    elif clientAndPos[0] == "left":
                        self.rightComboBox.addItem(serverAndIp[0])
                        self.synergycData[serverAndIp[0]] = serverAndIp[1]
                    elif clientAndPos[0] == "right":
                        self.leftComboBox.addItem(serverAndIp[0])
                        self.synergycData[serverAndIp[0]] = serverAndIp[1]
                    else:
                        QMessageBox.warning(self, u"No sharing", u"Nobody is sharing with you, please click on client mode for refresh")
                else:
                    pass

        self.topComboBox.addItem("")
        self.rightComboBox.addItem("")
        self.bottomComboBox.addItem("")
        self.leftComboBox.addItem("")
        self.clientState = True
    
    def fillComboBoxes(self):
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
        self.filled = True

##################################################################
##################################################################
##################################################################

    def on_topComboBox_highlighted(self):
        if not self.filled:
            self.fillComboBoxes()
        if not self.searched:
            self.searchClient()

    @pyqtSignature("QString")
    def on_topComboBox_activated(self, text):
        self.topComboBox.setEditable(True)
        if (text == gethostname()):
            QMessageBox.warning(self, u"Warning", u"The pc you have choosen is you own pc, please chose another pc")
            self.topComboBox.setCurrentIndex(0)

    def on_bottomComboBox_highlighted(self):
        if not self.filled:
            self.fillComboBoxes()

    @pyqtSignature("QString")
    def on_bottomComboBox_activated(self, text):
        self.bottomComboBox.setEditable(True)
        if (text == gethostname()):
            QMessageBox.warning(self, u"Warning", u"The pc you have choosen is you own pc, please chose another pc")
            self.bottomComboBox.setCurrentIndex(0)

    def on_rightComboBox_highlighted(self, text):
        if not self.filled:
            self.fillComboBoxes()

    @pyqtSignature("QString")
    def on_rightComboBox_activated(self, text):
        self.rightComboBox.setEditable(True)
        if (text == gethostname()):
            QMessageBox.warning(self, u"Warning", u"The pc you have choosen is you own pc, please chose another pc")
            self.rightComboBox.setCurrentIndex(0)

    def on_leftComboBox_highlighted(self, text):
        if not self.filled:
            self.fillComboBoxes()

    @pyqtSignature("QString")
    def on_leftComboBox_activated(self, text):
        self.leftComboBox.setEditable(True)
        if (text == gethostname()):
            QMessageBox.warning(self, u"Warning", u"The pc you have choosen is you own pc, please chose another pc")
            self.leftComboBox.setCurrentIndex(0)


##################################################################
##################################################################
##################################################################

    @pyqtSignature("")
    def on_applyButton_clicked(self):
        if not self.clientState: # Either client or server has to be set, if not client, than it's server

            ### Add the current Clientnames to the list confdomain to give it to giveData
            ### After that announce the _sinerji._tcp service
            if self.topComboBox.currentText(): 
                self.txtData.append(("top", self.topComboBox.currentText()))
            if self.bottomComboBox.currentText(): 
                self.txtData.append(("bottom", self.bottomComboBox.currentText()))
            if self.rightComboBox.currentText(): 
                self.txtData.append(("right", self.rightComboBox.currentText()))
            if self.leftComboBox.currentText(): 
                self.txtData.append(("left", self.leftComboBox.currentText()))

            self.connectingWorkstation.giveData(self.txtData)
            self.connectingWorkstation.announce()


            ### Creating the synergy.conf file
            if self.topComboBox.currentText() != '': 
                self.confdomain.append("top_bottom_%s" % self.topComboBox.currentText())
            if self.bottomComboBox.currentText() != '': 
                self.confdomain.append("bottom_top_%s" % self.bottomComboBox.currentText())
            if self.rightComboBox.currentText() != '': 
                self.confdomain.append("right_left_%s" % self.rightComboBox.currentText())
            if self.leftComboBox.currentText() != '': 
                self.confdomain.append("left_right_%s" % self.leftComboBox.currentText())
            self.confdomain.append(("host_host_%s" % gethostname()))

            createsynergyconf.screens(self.confdomain)
            createsynergyconf.links(self.confdomain)

            ## Starting synergys
            command = ['synergys', '--config', self.synergyConf]
            process = subprocess.call(command)

            self.trayIcon.showMessage("Sinerji", "Synergy server started succesfull", QSystemTrayIcon.Information, 4000) 

        elif self.clientState:
            ## Get the server name, look in synergycData dictionary and get from there the ip addres

            if self.topComboBox.currentText():
                address = self.synergycData[str(self.topComboBox.currentText())]
            if self.bottomComboBox.currentText():
                address = self.synergycData[str(self.bottomComboBox.currentText())]
            if self.rightComboBox.currentText():
                address = self.synergycData[str(self.rightComboBox.currentText())]
            if self.leftComboBox.currentText():
                address = self.synergycData[str(self.leftComboBox.currentText())]

            ## After getting the ip address, start synergyc
            command = ['synergyc', address]
            self.process = subprocess.Popen(command)
            
            self.trayIcon.showMessage("Sinerji", "Server is connected to you. ", QSystemTrayIcon.Information, 4000) 
        else:
            pass


    @pyqtSignature("")
    def on_closeButton_clicked(self):
        self.reject()


##################################################################
##################################################################
##################################################################

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
    app.setWindowIcon(QIcon(":/icon.png"))
    DBusQtMainLoop( set_as_default=True )
    form = SinerjiGui()
    form.show()
    app.exec_()


