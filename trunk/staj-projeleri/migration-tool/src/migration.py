#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

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
