#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import pisi

def upgrade_pisi():
    os.system("pisi up -y pisi")

def remove_all_repos_and_add_2009_repository():
    for repo in pisi.api.list_repos():
        pisi.api.remove_repo(repo)
    pisi.api.add_repo("pardus-2009", "http://paketler.pardus.org.tr/pardus-2009/pisi-index.xml.bz2")

def upgrade_and_configure_packages():
    os.system("pisi up --ignore-comar -y")
    os.system("pisi cp -y")

def install_missing_x11_drivers():
    os.system("pisi it -y -c x11.driver")    

def install_display_manager():
    os.unlink('/etc/X11/kdm/kdmrc')
    os.system("pisi it -y kdm xdm")

def install_other_missing_packages():
    os.system("pisi it -y pardus-default-settings")

def migrate_2008_to_2009():
    upgrade_pisi()
    remove_all_repos_and_add_2009_repository()
    upgrade_and_configure_packages()
    install_missing_x11_drivers()
    install_display_manager()
    install_other_missing_packages()

if __name__ == '__main__':
    migrate_2008_to_2009()
