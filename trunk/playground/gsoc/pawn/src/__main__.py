import sys,time
from PyQt4 import QtGui
from PyQt4 import QtCore
from ftpdownloader import FTPDownloader

app = QtGui.QApplication(sys.argv)
from versionmanager import Mirror
m = Mirror()
m.hostname='ftp.pardus.org.tr'
m.login='true'
m.username='anonymous'
m.password='anonymous'
m.port='21'
m.path='/pub'
m.filename='md5summer.exe' #'Pardus_2009.1_Anthropoides_virgo.iso'

widget = QtGui.QWidget()
widget.resize(500,500)
d = FTPDownloader(m, 'a.txt')

pb = QtGui.QPushButton('click', widget)
widget.connect(pb, QtCore.SIGNAL('clicked()'), d.startTransfer)
#QtCore.QObject.connect(d, QtCore.SIGNAL('commandStarted(int)'), d.starts)
QtCore.QObject.connect(d, QtCore.SIGNAL('commandFinished(int,bool)'), d.logCommandFinished)
QtCore.QObject.connect(d, QtCore.SIGNAL('stateChanged(int)'), d.logChangeState)
QtCore.QObject.connect(d, QtCore.SIGNAL('done(bool)'), d.processDone)
#QtCore.QObject.connect(d, QtCore.SIGNAL('rawCommandReply(int, const QString)'), d.cmd) #TODO: Does not work!
QtCore.QObject.connect(d, QtCore.SIGNAL('dataTransferProgress(qint64,qint64)'), d.traceTransferProgress)
QtCore.QObject.connect(d, QtCore.SIGNAL('readyRead()'), d.writeBack)

widget.show()
sys.exit(app.exec_())
