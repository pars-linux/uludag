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
import profile

class profileHandler(profileDialog):
    def __init__(self,parent = None,prfl = None,prfl_item = None, modal = 0,fl = 0):
        profileDialog.__init__(self,parent)
        self.prfl = prfl
        self.prfl_item = prfl_item
        self.updated = False
        if not prfl:
            self.new = True
            self.name_edit.setText(i18n("new_proxy"))
            self.rd1.setChecked(True)
            self.slotToggleEnableGlobal(True)
        else:
            self.new = False
            self.name_edit.setText(self.prfl.name)
            if self.prfl.type == profile.globl:
                self.rd1.setChecked(True)
                self.globl_host.setText(self.prfl.globl_host)
                self.globl_port.setText(self.prfl.globl_port)
                self.globl_host.setEnabled(True)
                self.globl_port.setEnabled(True)
            elif self.prfl.type == profile.indiv:
                self.chooseIndivType()
            elif self.prfl.type == profile.auto:
                self.rd3.setChecked(True)
                self.auto_url.setEnabled(True)
                self.auto_url.setText(self.prfl.auto_url)
            
        # Configure UI
        self.apply_but.setIconSet(loadIconSet("apply", KIcon.Small))
        self.apply_but.setText(i18n("Apply"))
        self.cancel_but.setIconSet(loadIconSet("cancel", KIcon.Small))
        self.cancel_but.setText(i18n("Cancel"))
        
        # Connections
        self.connect(self.apply_but, SIGNAL('clicked()'), self.slotApply)
        self.connect(self.cancel_but, SIGNAL('clicked()'), SLOT('close()'))
        self.connect(self.name_edit, SIGNAL('textChanged(const QString &)'), self.slotUpdated)
        self.connect(self.ch1,SIGNAL('toggled(bool)'), self.slotToggleEnableHTTP)
        self.connect(self.ch2,SIGNAL('toggled(bool)'), self.slotToggleEnableFTP)
        self.connect(self.ch4,SIGNAL('toggled(bool)'), self.slotToggleEnableSSL)
        self.connect(self.ch5,SIGNAL('toggled(bool)'), self.slotToggleEnableSOCKS)
        self.connect(self.rd1,SIGNAL('toggled(bool)'), self.slotToggleEnableType)
        self.connect(self.rd2,SIGNAL('toggled(bool)'), self.slotToggleEnableType)
        self.connect(self.rd3,SIGNAL('toggled(bool)'), self.slotToggleEnableType)
        
        self.show()
        

    def chooseIndivType(self):
        self.rd2.setChecked(True)
        self.ch1.setChecked(True)
        if self.prfl.http_host:
            self.http_host.setText(self.prfl.http_host)
            self.http_port.setText(self.prfl.http_port)
        if self.prfl.ftp_host:
            self.ch2.setChecked(True)
            self.ftp_host.setText(self.prfl.ftp_host)
            self.ftp_port.setText(self.prfl.ftp_port)
        if self.prfl.ssl_host:
            self.ch4.setChecked(True)
            self.ssl_host.setText(self.prfl.ssl_host)
            self.ssl_port.setText(self.prfl.ssl_port)
        if self.prfl.socks_host:
            self.ch5.setChecked(True)
            self.socks_host.setText(self.prfl.socks_host)
            self.socks_port.setText(self.prfl.socks_port)
        self.slotToggleEnableIndiv(True)
        

    def slotUpdated(self,content):
        self.updated = True
    
    def slotToggleEnableType(self, on):
        if self.rd1.isChecked():
            self.slotToggleEnableGlobal(True)
            self.slotToggleEnableIndiv(False)
            self.slotToggleEnableAuto(False)
        elif self.rd2.isChecked():
            self.slotToggleEnableGlobal(False)
            self.slotToggleEnableIndiv(True)
            self.slotToggleEnableAuto(False)
        elif self.rd3.isChecked():
            self.slotToggleEnableGlobal(False)
            self.slotToggleEnableIndiv(False)
            self.slotToggleEnableAuto(True)
    
    def slotToggleEnableGlobal(self, on):
        self.globl_host.setEnabled(on)
        self.globl_port.setEnabled(on)
    
    def slotToggleEnableIndiv(self, on):
        self.ch1.setEnabled(on)
        self.ch2.setEnabled(on)
        self.ch4.setEnabled(on)
        self.ch5.setEnabled(on)
        if not on:
            self.slotToggleEnableHTTP(False)
            self.slotToggleEnableFTP(False)
            self.slotToggleEnableSSL(False)
            self.slotToggleEnableSOCKS(False)
        else:
            self.slotToggleEnableHTTP(self.ch1.isChecked())
            self.slotToggleEnableFTP(self.ch2.isChecked())
            self.slotToggleEnableSSL(self.ch4.isChecked())
            self.slotToggleEnableSOCKS(self.ch5.isChecked())
    
    def slotToggleEnableHTTP(self, on):
            self.http_host.setEnabled(on)
            self.http_port.setEnabled(on)
    def slotToggleEnableFTP(self, on):
            self.ftp_host.setEnabled(on)
            self.ftp_port.setEnabled(on)
    def slotToggleEnableSSL(self, on):
            self.ssl_host.setEnabled(on)
            self.ssl_port.setEnabled(on)
    def slotToggleEnableSOCKS(self, on):
            self.socks_host.setEnabled(on)
            self.socks_port.setEnabled(on)
    def slotToggleEnableAuto(self,on):
            self.auto_url.setEnabled(on)

    def validate(self):
        name = unicode(self.name_edit.text())
        if name == "":
            self.warning.setText(i18n("Enter a name."))
            return
        if (self.new or (self.updated and self.name != name)) and profile.exists(name):
            self.warning.setText(i18n("This name is in use. Pick another."))
            return False
        if self.rd1.isChecked() and len(self.globl_host.text()) == 0:
            self.warning.setText(i18n("Please specify a host."))
            return False
        elif self.rd2.isChecked():
            if not self.ch1.isChecked() and not self.ch2.isChecked() and not self.ch4.isChecked() and not self.ch5.isChecked():
                self.warning.setText(i18n("Please specify at least one protocol."))
                return False
            if self.ch1.isChecked() and len(self.http_host.text()) == 0:
                self.warning.setText(i18n("Please specify a host for http."))
                return False
            if self.ch2.isChecked() and len(self.ftp_host.text()) == 0:
                self.warning.setText(i18n("Please specify a host for ftp."))
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

    def slotApply(self):
        name = unicode(self.name_edit.text())
        ok = self.validate()
        if not ok:
            return
        if self.new:
            self.prfl = profile.Profile(name)
        else:
            self.prfl.changeName(name)
        if self.rd1.isChecked():
            self.prfl.type = profile.globl
            self.prfl.globl_host = unicode(self.globl_host.text())
            self.prfl.globl_port = unicode(self.globl_port.text())
            self.prfl.comment = profile.comment_globl + " " + self.prfl.globl_host
        elif self.rd2.isChecked():
            self.prfl.type = profile.indiv
            self.prfl.comment = i18n("Protocols: ")
            if self.ch1.isChecked():
                self.has_http = True
                self.prfl.http_host = unicode(self.http_host.text())
                self.prfl.http_port = unicode(self.http_port.text())
                self.prfl.comment += " " + profile.comment_http + ":" + self.prfl.http_host
            if self.ch2.isChecked():
                self.has_ftp = True
                self.prfl.ftp_host = unicode(self.ftp_host.text())
                self.prfl.ftp_port = unicode(self.ftp_port.text())
                self.prfl.comment += " " + profile.comment_ftp + ":" + self.prfl.ftp_host
            if self.ch4.isChecked():
                self.has_ssl = True
                self.prfl.ssl_host = unicode(self.ssl_host.text())
                self.prfl.ssl_port = unicode(self.ssl_port.text())
                self.prfl.comment += " " + profile.comment_ssl + ":" + self.prfl.ssl_host
            if self.ch5.isChecked():
                self.has_socks = True
                self.prfl.socks_host = unicode(self.socks_host.text())
                self.prfl.socks_port = unicode(self.socks_port.text())
                self.prfl.comment += " " + profile.comment_socks + ":" + self.prfl.socks_host
        else:
            self.prfl.type = profile.auto
            self.prfl.auto_url = unicode(self.auto_url.text())
            self.prfl.comment = profile.comment_auto
        self.prfl.save()
        if self.new:
            self.parent().add(self.prfl)
        profile.save()
        self.prfl_item.repaint()
        self.close()
        
