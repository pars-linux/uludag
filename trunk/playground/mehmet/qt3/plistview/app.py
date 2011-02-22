#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from qt import *

from temp import PListView
from temp import PListViewItem

class MainWindow(QMainWindow):
    def __init__(self, *args):
        apply(QMainWindow.__init__, (self, ) + args)

        mainwidget = QWidget(self, "mainwidget")

        layout = QVBoxLayout(mainwidget, 1, 1, "layout")

        self.lv = PListView(mainwidget)
        layout.addWidget(self.lv)

        lvi = PListViewItem(self.lv, "name", "mesajjjjjjj")
        self.lv.add(lvi)

        b1 = QPushButton("button1", lvi, "button1")
        lvi.widget = b1
        #layout.addWidget(b1)

        self.setCentralWidget(mainwidget)

def main(args):
    app = QApplication(args)
    win = MainWindow()
    win.show()
    app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))
    app.exec_loop()

if __name__=="__main__":
        main(sys.argv)


