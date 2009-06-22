#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore

from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

from mainwindow import Ui_MainManager
from uiitem import Ui_HistoryItemWidget

from interface import *

SHOW, HIDE     = range(2)
TARGET_HEIGHT  = 0
ANIMATION_TIME = 200
DEFAULT_HEIGHT = 16777215

class MainManager(QtGui.QWidget):
    def __init__(self, parent, standAlone=True, app=None):
        super(MainManager, self).__init__(parent)

        self.ui = Ui_MainManager()
        self.app = app

        if standAlone:
            self.ui.setupUi(self)
            self.parent = self
        else:
            self.ui.setupUi(parent)
            self.parent = parent

        self.settings = QtCore.QSettings()

        self.animator = QTimeLine(ANIMATION_TIME, self)
        self.lastAnimation = SHOW

        self.tweakUi()

        self.last_item = None

        self.cface = ComarIface()
        self.pface = PisiIface(self)
        self.loaded = 0

        self.connectSignals()

        self.ui.textEdit.installEventFilter(self)
        self.ui.lw.installEventFilter(self)

        self.cface.listen(self.handler)
        self.pface.start()

    def connectSignals(self):
        # self.connect(self.pface, SIGNAL("finished()"), self.loadHistory)
        self.connect(self.pface, SIGNAL("loadFetched(PyQt_PyObject)"), self.loadHistory)

        self.connect(self.animator, SIGNAL("frameChanged(int)"), self.animate)
        self.connect(self.animator, SIGNAL("finished()"), self.animateFinished)
        self.connect(self.ui.newSnapshotPB, SIGNAL("clicked()"), self.takeSnapshot)
        self.connect(self.ui.buttonCancelMini, SIGNAL("clicked()"), self.hideEditBox)
        self.connect(self.ui.aliasLE, SIGNAL("textEdited(const QString &)"), self.setAlias)

    def loadHistory(self, num):
        map(self.addNewOperation, self.pface.ops.values()[self.loaded:num])

        self.loaded = num
        self.status(i18n("%d Operations Loaded" % self.loaded))

    def setAlias(self, txt):
        if self.last_item:
            self.last_item.setAlias(txt)

    def tweakUi(self):
        self.ui.lw.clear()
        self.ui.editBox.setMaximumHeight(TARGET_HEIGHT)
        self.ui.progressBar.hide()

    def animate(self, height):
        self.ui.editBox.setMaximumHeight(height)
        self.ui.lw.setMaximumHeight(self.parent.height()-height)
        self.update()

    def animateFinished(self):
        if self.lastAnimation == SHOW:
            self.ui.editBox.setMaximumHeight(DEFAULT_HEIGHT)
            self.ui.lw.setMaximumHeight(TARGET_HEIGHT)
            self.ui.editBox.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        elif self.lastAnimation == HIDE:
            self.ui.lw.setFocus()
            self.ui.lw.setMaximumHeight(DEFAULT_HEIGHT)
            self.ui.editBox.setMaximumHeight(TARGET_HEIGHT)
            self.ui.lw.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def hideEditBox(self):
        if self.lastAnimation == SHOW:
            self.lastAnimation = HIDE
            self.hideScrollBars()
            self.animator.setFrameRange(self.ui.editBox.height(), TARGET_HEIGHT)
            self.animator.start()
            self.ui.textEdit.clear()
            self.ui.editGroup.setTitle("")

    def hideScrollBars(self):
        self.ui.editBox.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.lw.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def loadDetails(self):
        self.status(i18n("Loading operation details.."))

        self.ui.textEdit.clear()
        item = self.sender().parent()
        self.last_item = item

        self.ui.editGroup.setTitle("Details for operation on %s at %s" % (item.op_date, item.op_time))

        self.ui.aliasLE.setText(unicode(item.ui.labelLabel.text()))

        message = ""
        if item.op_type == "snapshot":
            message += i18n("There are %1 packages in this snapshot", item.op_pack_len)
        else:
            for val in item.op_pack:
                message += "- %s\n" % val

        self.ui.textEdit.setText(message)

        self.lastAnimation = SHOW
        self.hideScrollBars()

        self.animator.setFrameRange(TARGET_HEIGHT, self.parent.height() - TARGET_HEIGHT)
        self.animator.start()

        self.status(i18n("Ready .."))

    def addNewOperation(self, op):
        item = HistoryItem(self.ui.lw, op[0])
        item.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
        item.setSizeHint(QSize(38,48))
        self.ui.lw.setItemWidget(item, NewOperation(op, self))
        self.ui.lw.sortItems(Qt.DescendingOrder)

    def loadPlan(self):
        self.status(i18n("Loading Operation Plan"))

        self.ui.textEdit.clear()
        self.lastAnimation = SHOW
        self.hideScrollBars()

        item = self.sender().parent()
        self.last_item = item

        self.app.processEvents()

        willbeinstalled, willberemoved = self.pface.historyPlan(item.op_no)

        information = ""
        if item.op_type == "snapshot":
            configs = self.pface.historyConfigs(item.op_no)
            if configs and len(configs) != 0:
                information += i18n("Configuration files in snapshot:")
                for i in configs.keys():
                    information += "<br><br><b> %s </b><br>" % i
                    for j in configs.get(i):
                        information += "%s \n" % ("/".join(j.split(str(item.op_no),1)[1].split(i,1)[1:]))
        message = ""

        if willbeinstalled and len(willbeinstalled) != 0:
            message += i18n("<br> These package(s) will be <b>installed</b> :<br>")
            for i in range(len(willbeinstalled)):
                message += "%s <br>" % willbeinstalled[i]

        if willberemoved and len(willberemoved) != 0:
            message += i18n("<br> These package(s) will be <b>removed</b> :<br>")
            for i in range(len(willberemoved)):
                message += "%s <br>" % willberemoved[i]

        message += "<br>"

        self.ui.editGroup.setTitle("Takeback plan for Operation on %s at %s" % (item.op_date, item.op_time))
        self.ui.textEdit.setText(message+information)

        self.animator.setFrameRange(TARGET_HEIGHT, self.parent.height() - TARGET_HEIGHT)
        self.animator.start()

        self.status(i18n("Ready .."))

    def status(self, txt):
        if self.ui.progressBar.isVisible():
            self.ui.progressBar.setFormat(txt)
            self.ui.opTypeLabel.hide()
        else:
            self.ui.opTypeLabel.setText(txt)
            self.ui.opTypeLabel.show()

    def takeLastOperation(self):
        self.pface.initDb()
        return self.pface.getLastOperation()

    def takeBack(self):
        willbeinstalled, willberemoved = None, None

        item = self.sender().parent()

        try:
            willbeinstalled, willberemoved = self.pface.historyPlan(item.op_no)
        except ValueError:
            return

        reply = QtGui.QMessageBox.warning(self, i18n("Takeback operation verification"),
            i18n("<center>This will restore your system back to : <b>%1</b> - <b>%2</b><br>", item.op_date, item.op_time) + \
            i18n("If you're unsure, click Cancel and see TakeBack Plan.</center>"),
             QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)

        if reply == QtGui.QMessageBox.Ok:
            self.status(i18n("Taking back to : %1", item.op_date))
            self.enableButtons(False)

            self.app.processEvents()
            self.cface.takeBack(item.op_no)

    def takeSnapshot(self):
        reply = QtGui.QMessageBox.question(self, i18n("Start new snapshot"),
            i18n("<center>This will take a snapshot of your system.<br>Click Ok when you're ready.</center>"),
             QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)

        if reply == QtGui.QMessageBox.Cancel:
            return

        self.status(i18n("Taking New Snapshot"))
        self.enableButtons(False)

        try:
            self.app.processEvents()
            self.cface.takeSnap()
        except:
            self.status(i18n("Authentication Failed"))
            self.enableButtons(True)

    def handler(self, package, signal, args):
        # print "Package:",package, "Signal:", signal, "Arguments:", args

        if signal == "status":
            self.status(" ".join(args))
        elif signal == "finished":
            self.status(i18n("Finished succesfully"))
            self.addNewOperation( self.takeLastOperation() )
            self.enableButtons(True)
        elif signal == "progress":
            self.status(i18n("Taking Snapshot : <b>%s</b>/100" % args[1]))
            self.enableButtons(False)

    def closeEvent(self, event=None):
        self.settings.setValue("pos", QtCore.QVariant(self.mapToGlobal(self.parent.pos())))
        self.settings.setValue("size", QtCore.QVariant(self.parent.size()))
        self.settings.sync()

        if self.pface.isRunning():
            self.pface.quit()
            # self.pface.wait()

        if event != None:
            event.accept()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Hide:
            self.closeEvent()
            return True

        return QtCore.QObject.eventFilter(self, obj, event)

    def enableButtons(self, true):
        self.ui.newSnapshotPB.setEnabled(true)

