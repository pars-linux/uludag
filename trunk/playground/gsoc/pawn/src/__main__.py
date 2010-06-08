import sys,time
from PyQt4 import QtGui
from PyQt4 import QtCore
from ftpdownloader import FTPDownloader

app = QtGui.QApplication(sys.argv)
from versionmanager import Mirror
m = Mirror()
m.hostname='ftp.linux.org.tr'
m.login='true'
m.username='anonymous'
m.password='anonymous'
m.port='21'
m.path='/'
m.filename='ls-lR.gz' #'Pardus_2009.1_Anthropoides_virgo.iso'

widget = QtGui.QWidget()
widget.resize(500,500)
d = FTPDownloader(m, m.filename)

pb = QtGui.QPushButton('Download it!', widget)
widget.connect(pb, QtCore.SIGNAL('clicked()'), d.startTransfer)
pb.resize(300,300)
widget.show()
sys.exit(app.exec_())
