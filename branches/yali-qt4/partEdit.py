# -*- coding: utf-8 -*-
# Copyleft 2007 Pardus

from PyQt4 import QtCore, QtGui

class DiskList(QtGui.QWidget):
    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.resize(QtCore.QSize(QtCore.QRect(0,0,778,100).size()).expandedTo(self.minimumSizeHint()))
        self.setStyleSheet("""
            QToolBox::tab { background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                        stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                                        stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
                            border-radius: 5px; }
            QRadioButton::indicator { width:1px;height:1px;border-color:white; }
            QRadioButton:checked { border:3px solid #777 }
            QSplitter::handle { background-color:white; }
        """)
        self.gridlayout = QtGui.QGridLayout(self)
        self.toolBox = QtGui.QToolBox(self)
        self.gridlayout.addWidget(self.toolBox,0,0,1,1)

    def addDisk(self,dw):
        self.toolBox.addItem(dw,dw.name)

class DiskWidget(QtGui.QWidget):
    def __init__(self, name):
        QtGui.QWidget.__init__(self,None)
        self.resize(QtCore.QSize(QtCore.QRect(0,0,778,80).size()).expandedTo(self.minimumSizeHint()))
        self.layout = QtGui.QGridLayout(self)
        self.diskGroup = QtGui.QGroupBox(self)
        self.diskGroup.setMinimumSize(QtCore.QSize(0,50))
        self.gridlayout = QtGui.QGridLayout(self.diskGroup)
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(0)
        self.splinter = QtGui.QSplitter(QtCore.Qt.Horizontal,self.diskGroup)
        self.gridlayout.addWidget(self.splinter,0,0,1,1)
        self.layout.addWidget(self.diskGroup)
        self.partitions = []
        self.name = name

    def addPartition(self,name=None,data=None):
        partition = QtGui.QRadioButton("%s\n55.3 GB" % name,self.diskGroup)
        partition.setStyleSheet("background-color:lightblue")
        partition.setFocusPolicy(QtCore.Qt.NoFocus)
        self.splinter.addWidget(partition)
        self.partitions.append({"name":name,"data":data})

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    diskList = DiskList()

    disk1 = DiskWidget("/dev/sda")
    disk1.addPartition("/dev/sda1",{"size":"50GB"})
    disk1.addPartition("/dev/sda2",{"size":"50GB"})
    diskList.addDisk(disk1)

    disk2 = DiskWidget("/dev/sdb")
    disk2.addPartition("/dev/sdb1",{"size":"10GB"})
    disk2.addPartition("/dev/sdb2",{"size":"50GB"})
    disk2.addPartition("/dev/sdb3",{"size":"10GB"})
    diskList.addDisk(disk2)

    diskList.show()
    sys.exit(app.exec_())

