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
from notifier import *
__version__ = 0.1


class SinerjiGui(QDialog, ui_sinerjigui.Ui_SinerjiGui):
    def __init__(self,  parent=None):
        super(SinerjiGui, self).__init__(parent)
        self.setupUi(self)
        self.closeButton.setFocusPolicy(Qt.NoFocus)
        self.applyButton.setFocusPolicy(Qt.NoFocus)

        self.trayIcon = QSystemTrayIcon(QIcon(":/icon.png"), self)
        self.trayActions() ## Own custom function
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
        self.started = None
        self.clientState = None
        self.clientAndPos = []
        self.serverAndIp = []
        self.synergyConf = os.path.join(os.path.expanduser("~"), ".synergy.conf") 

        ### Start browsing services, and looking for synergy.conf for parsing in updateUi
        self.startBrowsing()
        self.updateUi()

        self.notifier = Notifier()
        self.connect(self.notifier, SIGNAL("acceptServer"), self.startSynergyc)

        self.topComboBox.addItem('')
        self.bottomComboBox.addItem('')
        self.rightComboBox.addItem('')
        self.leftComboBox.addItem('')


##################################################################
##################################################################
##################################################################
    def showPopup(self):

        icon = QIcon(":/icon.png")
        message = "Server foo will connect to you"
        header = "Sinerji"

        self.notifier.show(icon, header, message, self.getPos())


    def getPos(self):
        pt = self.mapToGlobal(QPoint(0,0))
        screen = QDesktopWidget()
        incr = 0
        if pt.y() < screen.screenGeometry().height()/2 and pt.y() < self.height():
            incr = self.width() - 4
        elif pt.y() > screen.screenGeometry().height() - self.height() - 80:
            incr = 0
        else:
            incr = self.width() / 2
        return (pt.x() + self.height()/2, pt.y() + incr)



    """Override so that closing it doesn't quit the app"""
    def closeEvent(self, event):
        event.ignore()
        self.hide()

    ### Menu for the Tray
    def trayActions(self):
        self.trayMenu = QMenu()

        self.actionManage = QAction(QIcon(":/manage.png"),u"Configure", self)
        self.connect(self.actionManage, SIGNAL("activated()"), self.show)
        self.trayMenu.addAction(self.actionManage)

        self.actionAbout = QAction(QIcon(":/about.png"),u"About", self)
        self.connect(self.actionAbout, SIGNAL("activated()"), self.about)
        self.trayMenu.addAction(self.actionAbout)

        self.trayMenu.addSeparator()

        self.actionQuit = QAction(QIcon(":/quit.png"),u"Quit", self)
        self.connect(self.actionQuit, SIGNAL("activated()"), app.quit)
        self.trayMenu.addAction(self.actionQuit)

        self.connect(self.trayIcon, SIGNAL('activated(QSystemTrayIcon::ActivationReason)'), self.trayActivated)

    ## If left clicked, hide and show
    def trayActivated(self, reason):
        if reason != QSystemTrayIcon.Context:
            if self.isHidden():
                self.showNormal()
            else:
                self.hide()

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

        #self.trayIcon.showMessage("Sinerji", "Sinerji started, to configure please click", QSystemTrayIcon.Information, 4000) 
        if self.connectingSinerji.getClients():
            for server in self.connectingSinerji.getClients().keys():
                for client in self.connectingSinerji.getClients()[server]:
                    self.clientAndPos = client.split("=")
                self.serverAndIp = server.split("=")

            if self.serverAndIp[0] is None:
                pass
            else:
                if self.clientAndPos[1] == gethostname():
                    self.showPopup()
            self.searched = True
            self.address = self.serverAndIp[1]
        else:
            print "No Sinerji service available"

    def startSynergyc(self):
            command = ['synergyc', self.address]
            self.process = subprocess.Popen(command)
            
            print "Start Synergyc"
            
            self.trayIcon.showMessage("Sinerji", ("%s is connected to you." % self.clientAndPos[1] ), QSystemTrayIcon.Information, 4000) 
            self.trayIcon.setToolTip("%s is connected to you." % self.clientAndPos[1])


    def fillComboBoxes(self):
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
        ## From fillClientBox function we get the state 
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

            if os.path.exists(self.synergyConf):
                os.remove(self.synergyConf)
            
            createsynergyconf.screens(self.confdomain)
            createsynergyconf.links(self.confdomain)

            ## Starting synergys

            command = ['synergys', '--config', self.synergyConf]
            self.process = subprocess.Popen(command, shell=False)
            self.started = True

            self.trayIcon.showMessage("Sinerji", "Synergy server started succesfull", QSystemTrayIcon.Information, 4000) 
            self.trayIcon.setToolTip("Synergy is connected to a pc")

        elif self.clientState:
            QMessageBox.warning(self, u"Warning", u"Somebody is using your computer. To use other computers please restart")
            ## Get the server name, look in synergycData dictionary and get from there the ip addres


        else:
            pass


    @pyqtSignature("")
    def on_closeButton_clicked(self):
        if self.started:
            if self.process.pid:
                os.kill(self.process.pid+1, signal.SIGKILL)
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
        QTimer.singleShot(250, self.searchClient)



    def updateUi(self):
        ### Look for synergy.conf, if exists parse it and fill the comboBoxes
        print "UpdateUi"
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
    form.hide()
    sys.exit(app.exec_())


