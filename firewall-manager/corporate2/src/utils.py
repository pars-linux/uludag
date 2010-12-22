#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import locale

from qt import *
from kdecore import *
from kdeui import *
import kdedesigner
from khtml import *

import dialog

class IconButton(QPushButton):
    def __init__(self, parent, icon_name):
        QPushButton.__init__(self, parent)
        self.setFlat(True)
        self.myset = getIconSet(icon_name, KIcon.Small)
        self.setIconSet(self.myset)
        size = self.myset.iconSize(QIconSet.Small)
        self.myWidth = size.width() + 4
        self.myHeight = size.height() + 4
        self.resize(self.myWidth, self.myHeight)
        self.hide()

def getIconSet(name, group=KIcon.Toolbar):
    return KGlobal.iconLoader().loadIconSet(name, group)

class AdvancedRuleCheckBox(QCheckBox):
    def __init__(self, parent=None, name=None, ports='', index=0, isDefault=False, isRunning=False, isIncoming=False, message=None):
        QCheckBox.__init__(self, parent.viewport(), name)
        self.index = index
        self.ports = ports
        self.isDefault = isDefault
        self.isRunning = isRunning
        self.isIncoming = isIncoming
        self.fwconfig = parent.parentWidget()
        self.entryView = parent
        self.serviceName = ""
        if isDefault:
            self.serviceName = message

        self.updateMessage(message)
        self.isDragging = False

        self.pushEdit = IconButton(self, "configure")
        QToolTip.add(self.pushEdit, i18n("Edit Rule"))
        self.connect(self.pushEdit, SIGNAL("clicked()"), self.slotEdit)

        self.pushDelete = IconButton(self, "cancel")
        QToolTip.add(self.pushDelete, i18n("Delete Rule"))
        self.connect(self.pushDelete, SIGNAL("clicked()"), self.slotDelete)

        self.pushStart = IconButton(self, self.getStartIcon())
        QToolTip.add(self.pushStart, i18n("Start/Stop Rule"))
        self.connect(self.pushStart, SIGNAL("clicked()"), self.slotStart)

        if self.isDefault:
            self.icon = QImage(locate("data", "firewall-config/default.png"))
            self.pushDelete.hide()
            self.pushEdit.hide()
        else:
            self.icon = QImage(locate("data", "firewall-config/user-defined.png"))
            self.pushStart.hide()
        self.iconState = QImage(locate("data", "firewall-config/apply.png"))
        self.icon.smoothScale(32, 32)
        self.icon = QPixmap(self.icon)
        self.iconState.smoothScale(16, 16)
        self.iconState = QPixmap(self.iconState)

        self.fillColor = KGlobalSettings.baseColor()
        self.installEventFilter(self)
        self.show()

    def updateMessage(self, message=""):
        if self.isDefault:
            message = unicode(i18n(message))
            if self.isRunning:
                if self.isIncoming:
                    self.msg = unicode(i18n("Allow all incoming connections to %s.")) % message
                else:
                    self.msg = unicode(i18n("Reject all outgoing connections to %s.")) % message
            else:
                if self.isIncoming:
                    self.msg = unicode(i18n("Rejecting all incoming connections to %s.")) % message
                else:
                    self.msg = unicode(i18n("Allowing all outgoing connections to %s.")) % message
            self.msg2 = unicode(i18n("Ports: %s")) % self.ports.replace(' ', ', ').replace(':', '-')
        elif self.isIncoming:
            self.msg = unicode(i18n('Allow all incoming connection through ports %s.')) % self.ports.replace(':', '-')
        else:
            self.msg = unicode(i18n('Reject all outgoing connection through ports %s.')) % self.ports.replace(':', '-')


    def setIsRunning(self, run):
        self.isRunning = run
        self.pushStart.setIconSet(getIconSet(self.getStartIcon(), KIcon.Small))
        self.updateMessage(self.serviceName)
        self.show()

    def eventFilter(self, target, event):
        if(event.type()==QEvent.MouseMove):
            self.isDragging = True
        elif(event.type()==QEvent.MouseButtonPress):
            self.fillColor = KGlobalSettings.buttonBackground()
            self.showButtons(True)
            self.entryView.setCurrentItem(self)
        elif(event.type()==QEvent.MouseButtonRelease):
            if self.isDragging:
                self.isDragging = False
                if self.entryView.getCurrentItem():
                    self.fillColor = KGlobalSettings.baseColor()
                    self.entryView.getCurrentItem().showButtons(False)
        elif(event.type()==QEvent.Enter):
            if not self.isDragging:
                self.fillColor = KGlobalSettings.buttonBackground()
                self.showButtons(True)
                self.entryView.setCurrentItem(self)
        elif(event.type()==QEvent.Leave):
            if not (self.entryView.getCurrentItem() and self.isDragging):
                self.fillColor = KGlobalSettings.baseColor()
                self.showButtons(False)
        return False

    def showButtons(self, b):
        if not self.isEnabled():
            return
        if b:
            if self.isDefault:
                self.pushStart.show()
            else:
                self.pushEdit.show()
                self.pushDelete.show()
            self.repaint()
        else:
            self.pushEdit.hide()
            self.pushStart.hide()
            self.pushDelete.hide()
            self.repaint()

    def slotEdit(self):
        if self.isIncoming:
            desc = unicode(i18n("Write ports or port ranges that you want to ALLOW for incoming connections."))
        else:
            desc = unicode(i18n("Write ports or port ranges that you want to BLOCK for outgoing connections."))
        dialog = dialogRule(self, title=i18n("Edit Rule"), ports=self.ports, description=desc)
        ports = dialog.exec_loop()
        oldPorts = self.ports
        if ports:
            ports = str(ports)
            self.ports = ports
            try:
                self.fwconfig.saveAll()
                self.updateMessage()
                self.update()
            except:
                self.ports = oldPorts

    def slotStart(self):
        self.isRunning = not self.isRunning
        self.pushStart.setIconSet(getIconSet(self.getStartIcon(), KIcon.Small))
        self.update()
        try:
            self.fwconfig.saveAll()
            self.updateMessage(self.serviceName)
        except:
            self.isRunning = not self.isRunning
            self.pushStart.setIconSet(getIconSet(self.getStartIcon(), KIcon.Small))
            self.update()

    def getStartIcon(self):
        if self.isRunning:
            return "player_stop.png"
        else:
            return "player_play.png"

    def slotDelete(self):
        # fixme: store index and put the same old place
        self.hide()
        self.entryView.entries.remove(self)
        try:
            self.fwconfig.saveAll()
            self.fwconfig.refreshView()
        except:
            self.entryView.entries.append(self)
            self.show()

    def paintEvent(self, event):

        paint = QPainter(self)
        col = KGlobalSettings.baseColor()
        paint.fillRect(event.rect(), QBrush(self.fillColor))
        self.pushEdit.setPaletteBackgroundColor(col)
        self.pushStart.setPaletteBackgroundColor(col)
        self.pushDelete.setPaletteBackgroundColor(col)

        dip = (self.height() - self.icon.height()) / 2
        paint.drawPixmap(6, dip, self.icon)

        if self.isRunning:
            dip = dip + self.icon.height() - self.iconState.height()
            paint.drawPixmap(30, dip, self.iconState)

        oldFont = paint.font()
        font = QFont(oldFont)
        font.setItalic(True)
        font.setPointSize(10)

        paint.setFont(oldFont)
        fm = QFontMetrics(oldFont)
        if self.isDefault:
            paint.drawText(12 + self.icon.width() + 6, fm.ascent() + 2, unicode(self.msg))
            paint.setFont(font)
            paint.drawText(12 + self.icon.width() + 6, fm.ascent() + 18, unicode(self.msg2))
            paint.setFont(oldFont)
        else:
            paint.drawText(12 + self.icon.width() + 6, fm.ascent() + 9, unicode(self.msg))

    def resizeEvent(self, event):
        w = event.size().width()
        h = event.size().height()
        if self.isDefault:
            self.pushStart.setGeometry(w - self.pushStart.myWidth - 6 - 6, 5, self.pushStart.myWidth, self.pushStart.myHeight)
        else:
            self.pushEdit.setGeometry(w - self.pushEdit.myWidth - 6 - 6 - self.pushEdit.myWidth - 3, 5, self.pushEdit.myWidth, self.pushEdit.myHeight)
            self.pushDelete.setGeometry(w - self.pushDelete.myWidth - 6 - 6, 5, self.pushDelete.myWidth, self.pushDelete.myHeight)
        return QWidget.resizeEvent(self, event)

    def sizeHint(self):
        f = QFont(self.font())
        f.setPointSize(f.pointSize() + 1)
        f.setBold(True)
        fm = QFontMetrics(f)
        rect = fm.boundingRect(unicode(self.ports))
        w = 6 + self.icon.width() + 6 + rect.width() + 30 + self.pushStart.myWidth + 3 + self.pushEdit.myWidth + 3 + self.pushDelete.myWidth + 6

        f.setPointSize(f.pointSize() - 2)
        fm2 = self.fontMetrics()
        rect2 = fm2.boundingRect(unicode(self.ports))
        w2 = 6 + self.icon.width() + 6 + rect2.width() + 30 + self.pushStart.myWidth + 3 + self.pushEdit.myWidth + 3 + self.pushDelete.myWidth + 6

        w = max(w, w2)
        #h = max(fm.height() + 3 + fm2.height(), 32) + 10
        h = max(fm.height() + 10, 24) + 10
        return QSize(w, h)

class EntryView(QScrollView):
    def __init__(self, parent):
        QScrollView.__init__(self, parent)
        self.viewport().setPaletteBackgroundColor(KGlobalSettings.baseColor())
        self.entries = []
        self.fwconfig = parent
        self.currentItem = None

    def setCurrentItem(self, item):
        self.currentItem = item

    def getCurrentItem(self):
        return self.currentItem

    def clear(self):
        for e in self.entries:
            e.hide()
        self.entries = []

    def getPorts(self):
        ports = []
        for e in self.entries:
            if e.isDefault:
                if e.isRunning:
                    ports.append(e.ports)
            else:
                ports.append(e.ports)
        return ports

    def add(self, name="", ports="", index=0, isDefault=False, isRunning=False, isIncoming=False, message=None):
        if index == -1:
            index = len(self.entries)
        e = AdvancedRuleCheckBox(self, name, ports, index, isDefault, isRunning, isIncoming, message)
        self.entries.append(e)
        size = QSize(self.width(), self.height())
        self.resizeEvent(QResizeEvent(size , QSize(0, 0)))
        return e

    def delete(self, item):
        self.entries.remove(item)
        self.fwconfig.refreshView()

    def resizeEvent(self, event):
        QScrollView.resizeEvent(self, event)
        self.myResize(self.visibleWidth())

    def myResize(self, width):
        mw = 0
        th = 0
        for e in self.entries:
            h = e.sizeHint().height()
            mw = max(mw, e.sizeHint().width())
            e.setGeometry(0, th, width, h)
            th += h
        self.setMinimumSize(QSize(mw, 0))
        if th > self.height():
            self.resizeContents(width - 12, th)
        else:
            self.resizeContents(width, th)

    def checkItem(self, ports):
        for x in self.entries:
            if x.ports == ports:
                return True
        return False

class HelpDialog(QDialog):
    def __init__(self, name, title, parent=None):
        QDialog.__init__(self, parent)
        self.setCaption(title)
        self.layout = QGridLayout(self)
        self.htmlPart = KHTMLPart(self)
        self.resize(500, 600)
        self.layout.addWidget(self.htmlPart.view(), 1, 1)

        lang = locale.setlocale(locale.LC_MESSAGES)
        if "_" in lang:
            lang = lang.split("_", 1)[0]
        url = locate("data", "%s/help/%s/main_help.html" % (name, lang))
        if not os.path.exists(url):
            url = locate("data", "%s/help/en/main_help.html" % name)
        self.htmlPart.openURL(KURL(url))

class dialogRule(dialog.dialogRule):
    def __init__(self, parent=None, name=None, title="", ports="", description=""):
        dialog.dialogRule.__init__(self, parent, name)

        self.connect(self.pushCancel, SIGNAL('clicked()'), self, SLOT('reject()'))
        self.connect(self.pushOK, SIGNAL('clicked()'), SLOT('accept()'))

        # Load icons for buttons
        self.pushCancel.setIconSet(getIconSet('cancel', group=KIcon.Small))
        self.pushOK.setIconSet(getIconSet('ok', group=KIcon.Small))

        self.setCaption(title)
        self.linePorts.setText(ports.replace(':', '-'))
        self.infoLabel.setText(description)

    def accept(self):
        if checkPortFormat(str(self.linePorts.text())):
            dialog.dialogRule.accept(self)
        else:
            KMessageBox.sorry(self, i18n('Invalid port range.'), i18n('Error'))

    def exec_loop(self):
        if dialog.dialogRule.exec_loop(self):
            ports = self.linePorts.text().replace('-', ':')
            ports = ports.replace(' ', '')

            return ports
        else:
            return False

def checkPortFormat(ports):
    '''Check multiport format'''
    ports = ports.replace(' ', '')
    if ports.count(',') + ports.count('-') > 15:
        return False
    for port in ports.split(','):
        grp = port.split('-')
        if len(grp) > 2:
            return False
        for p in grp:
            if not p.isdigit() or p.startswith("0") or 0 > int(p) or int(p) > 65535:
                return False
    return True

