#!/usr/bin/python
from tabbed import Ui_MainWindow
import sys,os,threading
from PyQt4.QtGui import *
from PyQt4  import QtCore
import test

class app(QMainWindow):
  def __init__(self, parent = None):
    QMainWindow.__init__(self, parent)
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.connect(self.ui.pushButton, QtCore.SIGNAL("clicked()"), self.quit_all)

    """
    pushButton2 -> addtab
    pushButton3 -> removeTab
    """
    self.connect(self.ui.pushButton_2, QtCore.SIGNAL("clicked()"), self.addTab)
    self.connect(self.ui.pushButton_3, QtCore.SIGNAL("clicked()"), self.removeTab);


  def action(self):
    print "hammering"
  
  def addTab(self):
    try:
      self.newTab = QWidget()
      self.newTab.setObjectName("newTab")
      tabName = QtCore.QString("hede")
      self.ui.tabWidget.addTab(self.newTab, tabName)
    except Exception, e:
      print "ERR: ",e
      self.quit_all()
    
  
  def removeTab(self):
    try:
      tabNumber = self.ui.tabWidget.currentIndex()
      if tabNumber!= -1:
        self.ui.tabWidget.removeTab(tabNumber)
      else:
        print "WAR: no tab active"
    except Exception, e:
      print "ERR: ",e
      self.quit_all()


  def quit_all(self):
    quit()

class Mein(QApplication):
  def __init__(self):
    QApplication.__init__(self, sys.argv)

  def go(self):
    ret = test.connect()
    if ret == 0:
      print "py: initialize OK"
      print "py: entering loop"
      test.loop()
    else:
      print "py: initialize& event failed"



def main():
  main_app = Mein()
  guiPart = app()
  guiPart.show()
  main_app.go()


if __name__ == "__main__":
  main()
