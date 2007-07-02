# -*- coding: utf-8 -*-

import sys

from qt import *

from wizard import Wizard

def main():
    app = QApplication(sys.argv)
    wizard = Wizard()
    
    app.setMainWidget(wizard)
    wizard.show()
    app.exec_loop()

if __name__ == "__main__":
    main()
