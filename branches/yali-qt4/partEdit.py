# -*- coding: utf-8 -*-
# Copyleft 2007 Pardus

from PyQt4 import QtCore, QtGui

class DiskList(QtGui.QWidget):
     def __init__(self, name):
        QtGui.QWidget.__init__(self,None)
        self.resize(QtCore.QSize(QtCore.QRect(0,0,778,80).size()).expandedTo(self.minimumSizeHint()))
        self.setStyleSheet("""
            QRadioButton::indicator { width:1px;height:1px;border-color:white; }
            QRadioButton:checked { border:3px solid #777 }
            QSplitter::handle { background-color:white; }
        """)
        self.gridlayout = QtGui.QGridLayout(self)
        self.toolBox = QtGui.QToolBox(self)
        self.gridlayout.addWidget(self.toolBox,0,0,1,1)

    def addDisk(self,dw):
        pass

class DiskWidget(QtGui.QWidget):
    def __init__(self, name):
        QtGui.QWidget.__init__(self,None)
        self.resize(QtCore.QSize(QtCore.QRect(0,0,778,80).size()).expandedTo(self.minimumSizeHint()))
        self.layout = QtGui.QGridLayout(self)
        self.diskGroup = QtGui.QGroupBox(self)
        self.diskGroup.setMinimumSize(QtCore.QSize(0,80))
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
    partList = DiskWidget("/dev/sda")
    partList.addPartition("/dev/sda1",{"size":"50GB"})
    partList.addPartition("/dev/sda1",{"size":"50GB"})
    partList.show()
    sys.exit(app.exec_())

