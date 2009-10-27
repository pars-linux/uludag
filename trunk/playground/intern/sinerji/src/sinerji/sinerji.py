#!/usr/bin/python
# -*- coding: utf-8 -*-


import os, sys, re
import platform, time
from socket import gethostname
from dbus.mainloop.qt import DBusQtMainLoop
from PyQt4.QtCore import *
from PyQt4.QtGui import *

## Our custom modules
import ui_sinerjigui
import disconnect
import createsynergyconf
import parsesynergyconf
import avahiservices
import qrc_resources
import notifier

import gettext
__trans = gettext.translation('sinerji', fallback=True)
_ = __trans.ugettext

__version__ = "0.1"

class SinerjiGui(QDialog, ui_sinerjigui.Ui_SinerjiGui):
    def __init__(self,  parent=None):
        super(SinerjiGui, self).__init__(parent)
        self.setupUi(self)
        self.closeButton.setFocusPolicy(Qt.NoFocus)
        self.applyButton.setFocusPolicy(Qt.NoFocus)

        self.trayIcon = QSystemTrayIcon(QIcon(":/icon.png"), self)
        self.trayActions() ## Own custom function
        self.connect(self.trayIcon, SIGNAL('activated(QSystemTrayIcon::ActivationReason)'), self.trayActivated)
        self.trayIcon.setContextMenu(self.trayMenu)
        self.trayIcon.setToolTip(u"Sinerji")
        self.trayIcon.show()

        self.applyButton.setIcon(QIcon(":/buttonApply.png"))
        self.closeButton.setIcon(QIcon(":/buttonClose.png"))
        self.discoveredHosts = set()
        self.txtData = []
        self.confdomain = []
        self.synergycData = {}
        self.completedTop = None
        self.completedBottom = None
        self.completedRight = None
        self.completedLeft = None
        
        
        
        self.connected = False
        self.browser = None
        self.bus = None
        self.filled = None
        self.searched = None
        self.popup = None
        self.clientState = None
        self.serverState = None
        self.clientAndPos = []
        self.serverAndIp = []
        self.clientData = {}
        self.clientModel = QStringList()
        self.synergyConf = os.path.join(os.path.expanduser("~"), ".synergy.conf") 
        self.iconNotify = "/usr/share/sinerji/images/notifyIcon.png"

        ### Start browsing services, and looking for synergy.conf for parsing in updateUi
        self.startBrowsing()
        self.updateUi()
        self.setComboBoxes()
        self.notifier = notifier.Notifier()
        self.clientDisconnect = disconnect.Disconnect(self)
        self.connect(self.notifier, SIGNAL("acceptServer"), self.acceptServer)
        self.connect(self.notifier, SIGNAL("rejectServer"), self.rejectServer)
        self.connect(self.clientDisconnect.disconnectButton, SIGNAL("clicked()"), self.disconnect)
        self.connect(self.clientDisconnect.okButton, SIGNAL("clicked()"), self.clientDisconnect.hide)

        self.process = QProcess()
        self.processOutput = QByteArray()
        self.process.setReadChannelMode(QProcess.MergedChannels)
        self.process.setReadChannel(QProcess.StandardOutput)
        self.connect(self.process, SIGNAL("readyReadStandardOutput()"), self.readData)

        self.topComboBox.addItem('')
        self.bottomComboBox.addItem('')
        self.rightComboBox.addItem('')
        self.leftComboBox.addItem('')


##################################################################
##################################################################
##################################################################

    def closeEvent(self, event):
    ### Override so that closing it doesn't quit the app
        event.ignore()
        self.hide()


    def trayActions(self):
    ### Menu for the Tray
        self.trayMenu = QMenu()

        self.actionManage = QAction(QIcon(":/manage.png"),_("Manage"), self)
        self.connect(self.actionManage, SIGNAL("activated()"), self.show)
        self.trayMenu.addAction(self.actionManage)

        self.actionSearch = QAction(QIcon(":/search.png"),_("Search"), self)
        self.connect(self.actionSearch, SIGNAL("activated()"), self.searchClient)
        self.trayMenu.addAction(self.actionSearch)
        
        self.actionAbout = QAction(QIcon(":/about.png"),_("About"), self)
        self.connect(self.actionAbout, SIGNAL("activated()"), self.about)
        self.trayMenu.addAction(self.actionAbout)

        self.trayMenu.addSeparator()

        self.actionQuit = QAction(QIcon(":/quit.png"), _("Quit"), self)
        self.connect(self.actionQuit, SIGNAL("activated()"), self.killSynergys)
        self.trayMenu.addAction(self.actionQuit)
        
        ## for Client
        self.actionDisconnect = QAction(QIcon(":/disconnect.png"),_("Disconnect"), self)
        self.connect(self.actionDisconnect, SIGNAL("activated()"), self.disconnect)


    ## If left clicked, hide and show
    def trayActivated(self, reason):
        if not self.clientState and not self.serverState:
            if reason != QSystemTrayIcon.Context:
                if self.isHidden():
                    self.showNormal()
                else:
                    self.hide()
        else:
            if reason != QSystemTrayIcon.Context:
                if self.clientDisconnect.isHidden():
                    self.clientDisconnect.showNormal()
                else:
                    self.clientDisconnect.hide()




    def about(self):
        if not self.clientState and not self.serverState:
            self.show()
        QMessageBox.about(self, _("About Sinerji"),
             _("<b>Sinerji</b> v %s <p>Developer: Fatih Arslan  E-mail: fatih@arsln.org <p>This application is a fronted to the program Synergy <p>It uses avahi as backed for an easy configure experience <p>Python %s - Qt %s - PyQt %s on %s") % (
             __version__, platform.python_version(),
             QT_VERSION_STR, PYQT_VERSION_STR, platform.system()))

    def searchClient(self):
        if self.connectingSinerji.getClients():
            for server in self.connectingSinerji.getClients().keys():
                for client in self.connectingSinerji.getClients()[server]:
                    if gethostname() in client:
                        self.clientAndPos = client.split("=")
                        self.serverAndIp = server.split("=")
                        self.clientData[self.serverAndIp[0]] = [self.clientAndPos[1] ,self.clientAndPos[0], self.serverAndIp[1]]

            for hostname in self.clientData.keys():
                if self.clientData[hostname][0] == gethostname():
                    message = (_("<b>%s</b> want to use your pc from <b>%s</b>") % (hostname, self.clientData[hostname][1]))
                    header = hostname
                    buttonList = ["accept", unicode("Accept"), "reject", unicode("Reject")]
                    self.notifier.show(self.iconNotify, header, message, 0, buttonList)
        else:
            print _("No Sinerji service available")

    def acceptServer(self, hostname):
        self.notifier.stopNotifier(hostname)   ## Stop the others hostnames
        self.hostname = hostname   ## Need or parsingData function
        self.address = self.clientData[hostname][2]
        self.clientCmdList = QStringList()
        self.clientCmdList.append("-f")
        self.clientCmdList.append(self.address)
        self.process.start('synergyc', self.clientCmdList)


    def disconnect(self):
        if self.clientDisconnect.isVisible():
            self.clientDisconnect.hide()

        self.trayMenu.insertAction(self.actionAbout, self.actionManage) ## Add actionDisconnect before self.actionAbout
        self.trayMenu.insertAction(self.actionAbout, self.actionSearch) ## Add actionDisconnect before self.actionAbout
        self.trayMenu.removeAction(self.actionDisconnect)

        if self.clientState:
            self.process.kill()
            time.sleep(0.5)
            self.notifier.show(self.iconNotify, "Sinerji", (_("Disconnected from %s") % self.clientData[self.hostname][0]))
            self.clientState = None

        if self.serverState:
            self.process.kill()
            time.sleep(0.5)
            self.notifier.show(self.iconNotify, "Sinerji", (_("Disconnected from %s") % self.rightComboBox.currentText()))
            self.serverState = None

    def rejectServer(self):
        if self.searched:
            self.timer.stop()
        else:
            pass

##################################################################
##################################################################
##################################################################

    def setComboBoxes(self):
        self.topComboBox.setEditable(True)
        self.bottomComboBox.setEditable(True)
        self.rightComboBox.setEditable(True)
        self.leftComboBox.setEditable(True)

# ---------------TOP--------------
    def on_topComboBox_highlighted(self):
        if not self.filled:
            self.fillComboBoxes()
            self.completer = QCompleter(self.clientModel)
            self.completer.setCompletionMode(QCompleter.PopupCompletion)
        if not self.completedTop:
            self.topComboBox.setCompleter(self.completer)
            self.completedTop = True

    def on_topComboBox_editTextChanged(self):
        if not self.filled:
            self.fillComboBoxes()
            self.completer = QCompleter(self.clientModel)
            self.completer.setCompletionMode(QCompleter.PopupCompletion)
        if not self.completedTop:
            self.topComboBox.setCompleter(self.completer)
            self.completedTop = True


# ---------------Bottom--------------

    def on_bottomComboBox_highlighted(self, text):
        if not self.filled:
            self.fillComboBoxes()
            self.completer = QCompleter(self.clientModel)
            self.completer.setCompletionMode(QCompleter.PopupCompletion)
        if not self.completedBottom:
            self.bottomComboBox.setCompleter(self.completer)
            self.completedBottom = True


    def on_bottomComboBox_editTextChanged(self):
        if not self.filled:
            self.fillComboBoxes()
            self.completer = QCompleter(self.clientModel)
            self.completer.setCompletionMode(QCompleter.PopupCompletion)
        if not self.completedBottom:
            self.bottomComboBox.setCompleter(self.completer)
            self.completedBottom = True



# ---------------Right--------------
    def on_rightComboBox_highlighted(self, text):
        if not self.filled:
            self.fillComboBoxes()
            self.completer = QCompleter(self.clientModel)
            self.completer.setCompletionMode(QCompleter.PopupCompletion)
        if not self.completedRight:
            self.rightComboBox.setCompleter(self.completer)
            self.completedRight = True


    def on_rightComboBox_editTextChanged(self):
        if not self.filled:
            self.fillComboBoxes()
            self.completer = QCompleter(self.clientModel)
            self.completer.setCompletionMode(QCompleter.PopupCompletion)
        if not self.completedRight:
            self.rightComboBox.setCompleter(self.completer)
            self.completedRight = True


# ---------------LEFT--------------
    def on_leftComboBox_highlighted(self, text):
        if not self.filled:
            self.fillComboBoxes()
            self.completer = QCompleter(self.clientModel)
            self.completer.setCompletionMode(QCompleter.PopupCompletion)
        if not self.completedLeft:
            self.leftComboBox.setCompleter(self.completer)
            self.completedLeft = True

    def on_leftComboBox_editTextChanged(self):
        if not self.filled:
            self.fillComboBoxes()
            self.completer = QCompleter(self.clientModel)
            self.completer.setCompletionMode(QCompleter.PopupCompletion)
        if not self.completedLeft:
            self.leftComboBox.setCompleter(self.completer)
            self.completedLeft = True



## ------------- FILL COMBOBOXES ----------------
    def fillComboBoxes(self):
        ### Add the hostnames that we get from browsing _workstation._tcp to the comboBoxes
        for domain in self.connectingWorkstation.getDomains():
            print domain
            self.clientModel.append(domain)
            self.topComboBox.addItem(domain)
            self.bottomComboBox.addItem(domain)
            self.rightComboBox.addItem(domain)
            self.leftComboBox.addItem(domain)
        self.filled = True
        self.topComboBox.removeItem(self.topComboBox.findText(gethostname()))
        self.bottomComboBox.removeItem(self.bottomComboBox.findText(gethostname()))
        self.rightComboBox.removeItem(self.rightComboBox.findText(gethostname()))
        self.leftComboBox.removeItem(self.leftComboBox.findText(gethostname()))

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
                self.txtData.append(("up", self.topComboBox.currentText()))
            if self.bottomComboBox.currentText(): 
                self.txtData.append(("down", self.bottomComboBox.currentText()))
            if self.rightComboBox.currentText(): 
                self.txtData.append(("right", self.rightComboBox.currentText()))
            if self.leftComboBox.currentText(): 
                self.txtData.append(("left", self.leftComboBox.currentText()))

            self.connectingWorkstation.giveData(self.txtData)
            self.connectingWorkstation.announce()


            ### Creating the synergy.conf file
            if self.topComboBox.currentText() != '': 
                self.confdomain.append("up_down_%s" % self.topComboBox.currentText())
            if self.bottomComboBox.currentText() != '': 
                self.confdomain.append("down_up_%s" % self.bottomComboBox.currentText())
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

            self.cmdList = QStringList()
            self.cmdList.append("-f")
            self.cmdList.append("--config")
            self.cmdList.append(self.synergyConf)
            self.process.start('synergys', self.cmdList)
            self.serverState = True
            self.hide()
            time.sleep(0.5)
            self.notifier.show(self.iconNotify, "Sinerji", _("Synergy server started successfull"))
            self.trayIcon.setToolTip(_("Synergy server is running"))
            self.trayMenu.insertAction(self.actionAbout, self.actionDisconnect) ## Add actionDisconnect before self.actionAbout
            self.trayMenu.removeAction(self.actionManage)
            self.trayMenu.removeAction(self.actionSearch)

            self.clientDisconnect.setText(_("Synergy server has started and waiting response from %s") % self.rightComboBox.currentText())

        elif self.clientState:
            QMessageBox.warning(self, _("Warning"), _("Somebody is using your computer. To use other computers please restart"))

        else:
            pass

    def killSynergys(self):
        if self.serverState:
            self.process.kill()
        self.reject()

    def readData(self):
        self.processOutput = self.process.readAllStandardOutput()
        self.text = QString.fromLocal8Bit(str(self.processOutput))
        self.parseReadData(self.text)

    def parseReadData(self, data):
        self.patternFound = 'NOTE:.*client "(.*)" has connected'
        self.patternRemoved = 'NOTE:.*client "(.*)" has disconnected'
        self.patternFoundClient = 'NOTE:.*connected to server'
        self.patternRemovedClient = 'NOTE:.*disconnected from server'
        n = re.match(self.patternFound, str(data), re.I)
        m = re.match(self.patternRemoved, str(data), re.I)
        p = re.match(self.patternFoundClient, str(data), re.I)
        o = re.match(self.patternRemovedClient, str(data), re.I)

        if n:
            clientFound = n.groups()[0]
            self.notifier.show(self.iconNotify, "Sinerji", _("Computer %s is sharing its screen") % clientFound)
            self.trayIcon.setToolTip(_("Synergy server is connected"))
            self.serverState = True

            self.clientDisconnect.setText(_("Your are connected to %s") % clientFound)

        if m:
            clientRemoved = m.groups()[0]
            self.notifier.show(self.iconNotify, "Sinerji", _("Computer %s is no longer sharing its screen") % clientRemoved)
            self.trayMenu.insertAction(self.actionAbout, self.actionManage) ## Add actionDisconnect before self.actionAbout
            self.trayMenu.insertAction(self.actionAbout, self.actionSearch) ## Add actionDisconnect before self.actionAbout
            self.trayMenu.removeAction(self.actionDisconnect)
            self.serverState = None
            self.process.kill()
        if p:
            self.trayMenu.insertAction(self.actionAbout, self.actionDisconnect) ## Add actionDisconnect before self.actionAbout
            self.trayMenu.removeAction(self.actionManage)
            self.trayMenu.removeAction(self.actionSearch)
            self.clientState = True
            self.notifier.show(self.iconNotify, "Sinerji", _("%s is connected to you") % self.hostname, 1500)
            self.clientDisconnect.setText(_("%s is connected to you") % self.hostname)
            self.trayIcon.setToolTip(_("%s is connected to you.") % self.hostname)
            self.timer.stop()
        if o:
            self.trayMenu.insertAction(self.actionAbout, self.actionManage) ## Add actionDisconnect before self.actionAbout
            self.trayMenu.insertAction(self.actionAbout, self.actionSearch) ## Add actionDisconnect before self.actionAbout
            self.trayMenu.removeAction(self.actionDisconnect)
            self.clientState = None
            self.process.kill()
            time.sleep(0.5)
            self.notifier.show(self.iconNotify, "Sinerji", (_("Disconnected from %s") % self.clientData[self.hostname][0]))

    @pyqtSignature("")
    def on_closeButton_clicked(self):
        self.hide()

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
        
        QTimer.singleShot(500, self.searchClient)
        self.searched = True
        self.searchInterval()



    def searchInterval(self):
        self.timer = QTimer()
        self.connect(self.timer, SIGNAL("timeout()"), self.searchClient)
        self.timer.start(30000)



    def updateUi(self):
        ### Look for synergy.conf, if exists parse it and fill the comboBoxes
        print "UpdateUi"
        if os.path.exists(self.synergyConf):
            self.parser = parsesynergyconf.parseSynergyConf(self.synergyConf)
            for position in self.parser.getClients():
                if position[0] == "up":
                    self.topComboBox.insertItem(0, position[1])
                elif position[0] == "down":
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


