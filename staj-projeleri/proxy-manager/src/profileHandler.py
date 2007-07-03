#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.

from profileDialog import profileDialog
from utility import *

class profileHandler(profileDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
##        self.programs = getPrograms()
        profileDialog.__init__(self,parent)
        self.parent = parent
        self.name = name
        self.updated = False
        if not name:
            self.new = True
            self.name_edit.setText(i18n("new_proxy"))
            self.rd1.setChecked(True)
        else:
            self.new = False
            self.name_edit.setText(self.name)
            if config.getint(self.name, "type") == 0:
                self.rd1.setChecked(True)
            elif config.getint(self.name, "type") == 1:
                self.chooseType1()
            elif config.getint(self.name, "type") == 2:
                self.chooseType2()
            # FIXME: Bu tip için verilen adresi oku ve değerleri ona göre ata.
            #            Ayrıca ne aralıkla bu adresi kontrol edeceğine karar ver; login?
            elif config.getint(self.name, "type") == 3:
                self.rd2.setChecked(True)
                self.auto_url.setText(config.get(self.name, "auto_url"))
            
        # Configure UI
        self.apply_but.setIconSet(loadIconSet("apply", KIcon.Small))
        self.apply_but.setText(i18n("Apply"))
        self.cancel_but.setIconSet(loadIconSet("cancel", KIcon.Small))
        self.cancel_but.setText(i18n("Cancel"))
        
        
        # Connections
        self.connect(self.apply_but, SIGNAL('clicked()'), self.slotApply)
        self.connect(self.cancel_but, SIGNAL('clicked()'), SLOT('close()'))
        self.connect(self.name_edit, SIGNAL('textChanged(const QString &)'), self.slotUpdated)
        
        self.show()
    
    def slotUpdated(self,content):
        self.updated = True
        pass

    def slotApply(self):
        # FIXME: consider if "name" of the profile changes
        lineEdit = unicode(self.name_edit.text())
        if lineEdit == "":
            self.warning.setText(i18n("Enter a name."))
            return
        if self.new or (self.updated and self.name != lineEdit):
            if config.has_section(lineEdit):
                self.warning.setText(i18n("This name is in use. Pick another."))
                return
        if not self.new:
            old_isActive = config.get(self.name,"isActive")
            config.remove_section(self.name)
            config.add_section(lineEdit)
        # Set the configurations to "config"
        config.set(lineEdit,"isActive",old_isActive)
        if self.rd1.isChecked():
            config.set(lineEdit,"type","0")
        elif self.rd2.isChecked():
            if self.ch0.isChecked():
                config.set(lineEdit,"type","1")
                config.set(lineEdit,"http_host",self.http_host.text)
                config.set(lineEdit,"http_port",self.http_port.text)
            else:
                config.set(lineEdit,"type","2")
        else:
            pass
        f = open(configPath,"w")
        config.write(f)
        f.close()
##        config.set(name, "isActive", "0")
##        self.parent.prflview.add(name)
        self.close()
    
    def chooseType1(self):
        self.rd2.setChecked(True)
        self.ch0.setChecked(True)
        self.ch1.setChecked(True)
        self.ch1.setText(i18n("Global"))
        if config.has_option(self.name, "http_host"):
            self.http_host.setText(config.get(self.name, "http_host"))
            self.http_port.setText(config.get(self.name, "http_port"))
            self.http_host.setEnabled(True)
            self.http_port.setEnabled(True)
    
    def chooseType2(self):
        self.rd2.setChecked(True)
        self.ch0.setChecked(True)
        if config.has_option(self.name, "http_host"):
            self.ch1.setChecked(True)
            self.http_host.setText(config.get(self.name, "http_host"))
            self.http_port.setText(config.get(self.name, "http_port"))
            self.http_host.setEnabled(True)
            self.http_port.setEnabled(True)
        if config.has_option(self.name, "ftp_host"):
            self.ch2.setChecked(True)
            self.ftp_host.setText(config.get(self.name, "ftp_host"))
            self.ftp_port.setText(config.get(self.name, "ftp_port"))
            self.ftp_host.setEnabled(True)
            self.ftp_port.setEnabled(True)
        if config.has_option(self.name, "gopher_host"):
            self.ch3.setChecked(True)
            self.gopher_host.setText(config.get(self.name, "gopher_host"))
            self.gopher_port.setText(config.get(self.name, "gopher_port"))
            self.gopher_host.setEnabled(True)
            self.gopher_port.setEnabled(True)
        if config.has_option(self.name, "ssl_host"):
            self.ch4.setChecked(True)
            self.ssl_host.setText(config.get(self.name, "ssl_host"))
            self.ssl_port.setText(config.get(self.name, "ssl_port"))
            self.ssl_host.setEnabled(True)
            self.ssl_port.setEnabled(True)
        if config.has_option(self.name, "socks_host"):
            self.ch5.setChecked(True)
            self.socks_host.setText(config.get(self.name, "socks_host"))
            self.socks_port.setText(config.get(self.name, "socks_port"))
            self.socks_host.setEnabled(True)
            self.socks_port.setEnabled(True)

    
