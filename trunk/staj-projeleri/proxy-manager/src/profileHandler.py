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
        profileDialog.__init__(self,parent)
        self.name = name
        self.updated = False
        if not name:
            self.new = True
            self.name_edit.setText(i18n("new_proxy"))
            self.rd1.setChecked(True)
        else:
            self.new = False
            self.name_edit.setText(self.name)
            type = config.getint(self.name, "type")
            if type == 0:
                self.rd1.setChecked(True)
            elif type == 1:
                self.chooseType1()
            elif type == 2:
                self.chooseType2()
            # FIXME: Bu tip için verilen adresi oku ve değerleri ona göre ata.
            #            Ayrıca ne aralıkla bu adresi kontrol edeceğine karar ver; login?
            elif type == 3:
                self.rd3.setChecked(True)
                self.auto_url.setEnabled(True)
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
        self.connect(self.ch0,SIGNAL('toggled(bool)'), self.slotToggleEnableGlobal)
        self.connect(self.ch1,SIGNAL('toggled(bool)'), self.slotToggleEnableHTTP)
        self.connect(self.ch2,SIGNAL('toggled(bool)'), self.slotToggleEnableFTP)
        self.connect(self.ch3,SIGNAL('toggled(bool)'), self.slotToggleEnableGopher)
        self.connect(self.ch4,SIGNAL('toggled(bool)'), self.slotToggleEnableSSL)
        self.connect(self.ch5,SIGNAL('toggled(bool)'), self.slotToggleEnableSOCKS)
        self.connect(self.rd1,SIGNAL('toggled(bool)'), self.slotToggleEnableType)
        self.connect(self.rd3,SIGNAL('toggled(bool)'), self.slotToggleEnableType)
        self.connect(self.rd3,SIGNAL('toggled(bool)'), self.slotToggleEnableType)
        
        self.show()
    
    def slotUpdated(self,content):
        self.updated = True
    
    def slotToggleEnableType(self, on):
        if self.rd1.isChecked():
            self.ch0.setEnabled(False)
            self.ch1.setEnabled(False)
            self.slotToggleEnableHTTP(False)
            self.slotToggleEnableGlobal(True)
            self.slotToggleEnableAuto(False)
        elif self.rd2.isChecked():
            self.ch0.setEnabled(True)
            self.ch1.setEnabled(True)
            self.slotToggleEnableHTTP(self.ch1.isChecked())
            self.slotToggleEnableGlobal(self.ch0.isChecked())
            self.slotToggleEnableAuto(False)
        elif self.rd3.isChecked():
            self.ch0.setEnabled(False)
            self.ch1.setEnabled(False)
            self.slotToggleEnableHTTP(False)
            self.slotToggleEnableGlobal(True)
            self.slotToggleEnableAuto(True)
    
    def slotToggleEnableGlobal(self, on):
        if on == self.ch2.isEnabled():
            self.ch2.setEnabled(not on)
            self.ch3.setEnabled(not on)
            self.ch4.setEnabled(not on)
            self.ch5.setEnabled(not on)
            if on:
                self.ch1.setText(i18n("Global"))
                self.slotToggleEnableFTP(False)
                self.slotToggleEnableGopher(False)
                self.slotToggleEnableSSL(False)
                self.slotToggleEnableSOCKS(False)
            else:
                self.ch1.setText(i18n("Http"))
                self.slotToggleEnableFTP(self.ch2.isChecked())
                self.slotToggleEnableGopher(self.ch3.isChecked())
                self.slotToggleEnableSSL(self.ch4.isChecked())
                self.slotToggleEnableSOCKS(self.ch5.isChecked())
    def slotToggleEnableHTTP(self, on):
            self.http_host.setEnabled(on)
            self.http_port.setEnabled(on)
    def slotToggleEnableFTP(self, on):
            self.ftp_host.setEnabled(on)
            self.ftp_port.setEnabled(on)
    def slotToggleEnableGopher(self, on):
            self.gopher_host.setEnabled(on)
            self.gopher_port.setEnabled(on)
    def slotToggleEnableSSL(self, on):
            self.ssl_host.setEnabled(on)
            self.ssl_port.setEnabled(on)
    def slotToggleEnableSOCKS(self, on):
            self.socks_host.setEnabled(on)
            self.socks_port.setEnabled(on)
    def slotToggleEnableAuto(self,on):
            self.auto_url.setEnabled(on)

    def chooseType1(self):
        self.rd2.setChecked(True)
        self.ch0.setChecked(True)
        self.ch1.setEnabled(True)
        self.ch1.setChecked(True)
        self.ch1.setText(i18n("Global"))
        self.http_host.setText(config.get(self.name, "http_host"))
        self.http_port.setText(config.get(self.name, "http_port"))
        self.slotToggleEnableHTTP(True)
    
    def chooseType2(self):
        self.rd2.setChecked(True)
        if config.has_option(self.name, "http_host"):
            self.ch1.setChecked(True)
            self.http_host.setText(config.get(self.name, "http_host"))
            self.http_port.setText(config.get(self.name, "http_port"))
            self.slotToggleEnableHTTP(True)
        if config.has_option(self.name, "ftp_host"):
            self.ch2.setChecked(True)
            self.ftp_host.setText(config.get(self.name, "ftp_host"))
            self.ftp_port.setText(config.get(self.name, "ftp_port"))
        if config.has_option(self.name, "gopher_host"):
            self.ch3.setChecked(True)
            self.gopher_host.setText(config.get(self.name, "gopher_host"))
            self.gopher_port.setText(config.get(self.name, "gopher_port"))
        if config.has_option(self.name, "ssl_host"):
            self.ch4.setChecked(True)
            self.ssl_host.setText(config.get(self.name, "ssl_host"))
            self.ssl_port.setText(config.get(self.name, "ssl_port"))
        if config.has_option(self.name, "socks_host"):
            self.ch5.setChecked(True)
            self.socks_host.setText(config.get(self.name, "socks_host"))
            self.socks_port.setText(config.get(self.name, "socks_port"))
        self.slotToggleEnableGlobal(False)
        self.ch1.setEnabled(True)

    def slotApply(self):
        # FIXME: consider if "name" of the profile changes
        name = unicode(self.name_edit.text())
        ok = self.validate()
        old_isActive = "0"
        if not ok:
            return
        if not self.new:
            old_isActive = config.get(self.name,"isActive")
            config.remove_section(self.name)
        # Set the configurations to "config"
        config.add_section(name)
        config.set(name,"isActive",old_isActive)
        if self.rd1.isChecked():
            config.set(name,"type","0")
        elif self.rd2.isChecked():
            if self.ch0.isChecked():
                config.set(name,"type","1")
                config.set(name,"http_host",unicode(self.http_host.text()))
                config.set(name,"http_port",unicode(self.http_port.text()))
            else:
                config.set(name,"type","2")
                if self.ch1.isChecked():
                    config.set(name,"http_host",unicode(self.http_host.text()))
                    config.set(name,"http_port",unicode(self.http_port.text()))
                if self.ch2.isChecked():
                    config.set(name,"ftp_host",unicode(self.ftp_host.text()))
                    config.set(name,"ftp_port",unicode(self.ftp_port.text()))
                if self.ch3.isChecked():
                    config.set(name,"gopher_host",unicode(self.gopher_host.text()))
                    config.set(name,"gopher_port",unicode(self.gopher_port.text()))
                if self.ch4.isChecked():
                    config.set(name,"ssl_host",unicode(self.ssl_host.text()))
                    config.set(name,"ssl_port",unicode(self.ssl_port.text()))
                if self.ch5.isChecked():
                    config.set(name,"socks_host",unicode(self.socks_host.text()))
                    config.set(name,"socks_port",unicode(self.socks_port.text()))
        else:
            config.set(name,"type","3")
            config.set(name,"auto_url",unicode(self.auto_url.text()))
        f = open(configPath,"w")
        config.write(f)
        f.close()
        if self.new:
            self.parent().add(name)
        self.close()
    
    def validate(self):
        name = unicode(self.name_edit.text())
        if name == "":
            self.warning.setText(i18n("Enter a name."))
            return
        if (self.new or (self.updated and self.name != name)) and config.has_section(name):
            self.warning.setText(i18n("This name is in use. Pick another."))
            return False
        if self.rd2.isChecked():
            if self.ch0.isChecked() and len(self.http_host.text()) == 0:
                self.warning.setText(i18n("Please specify a host."))
                return False
            if self.ch1.isChecked() and len(self.http_host.text()) == 0:
                self.warning.setText(i18n("Please specify a host for http."))
                return False
            if self.ch2.isChecked() and len(self.ftp_host.text()) == 0:
                self.warning.setText(i18n("Please specify a host for ftp."))
                return False
            if self.ch3.isChecked() and len(self.gopher_host.text()) == 0:
                self.warning.setText(i18n("Please specify a host for gopher."))
                return False
            if self.ch4.isChecked() and len(self.ssl_host.text()) == 0:
                self.warning.setText(i18n("Please specify a host for ssl."))
                return False
            if self.ch5.isChecked() and len(self.socks_host.text()) == 0:
                self.warning.setText(i18n("Please specify a host for socks."))
                return False
        elif self.rd3.isChecked() and len(self.auto_url.text()) == 0:
            self.warning.setText(i18n("Please specify a url."))
            return False
        
        return True

