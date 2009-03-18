#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# A temporary module for mapping components and groups until pisi components provide them

(GROUP_UNKNOWN, GROUP_ACCESSIBILITIY, GROUP_ACCESSORIES, GROUP_EDUCATION, GROUP_GAMES, GROUP_GRAPHICS,
 GROUP_INTERNET, GROUP_OFFICE, GROUP_OTHER, GROUP_PROGRAMMING, GROUP_MULTIMEDIA, GROUP_SYSTEM,
 GROUP_DESKTOP_KDE, GROUP_DESKTOP_GNOME, GROUP_DESKTOP_XFCE, GROUP_DESKTOP_OTHER, GROUP_PUBLISHING,
 GROUP_SERVERS, GROUP_FONTS, GROUP_ADMIN_TOOLS, GROUP_LEGACY, GROUP_LOCALIZATION, GROUP_VIRTUALIZATION,
 GROUP_POWER_MANAGEMENT, GROUP_SECURITY, GROUP_COMMUNICATION, GROUP_NETWORK, GROUP_SCIENCE,
 GROUP_ELECTRONICS, GROUP_DOCUMENTATION) = range(30)

groups = { GROUP_UNKNOWN : {
             "name": "Unknown",
             "icon": "unknown"
             },
           GROUP_ACCESSIBILITIY: {
             "name": "Accessibility",
             "icon": "preferences-desktop-accessibility"
             },
           GROUP_ACCESSORIES: {
             "name": "Accessories",
             "icon": "applications-accessories"
             },
           GROUP_EDUCATION: {
             "name": "Education",
             "icon": "applications-education"
             },
           GROUP_GAMES: {
             "name": "Games",
             "icon": "applications-games"
             },
           GROUP_GRAPHICS: {
             "name": "Graphics",
             "icon": "applications-graphics"
             },
           GROUP_INTERNET: {
             "name": "Internet",
             "icon": "applications-internet"
             },
           GROUP_OFFICE: {
             "name": "Office",
             "icon": "applications-office"
             },
           GROUP_OTHER: {
             "name": "Other",
             "icon": "applications-other" },
           GROUP_PROGRAMMING: {
             "name": "Programming",
             "icon": "applications-development"
             },
           GROUP_MULTIMEDIA: {
             "name": "Multimedia",
             "icon": "applications-multimedia"
             },
           GROUP_SYSTEM: {
             "name": "System",
             "icon": "applications-system"
             },
           GROUP_DESKTOP_KDE: {
             "name": "KDE Desktop",
             "icon": "kde"
             },
           GROUP_DESKTOP_GNOME: {
             "name": "Gnome Desktop",
             "icon": "preferences-desktop"
             },
           GROUP_DESKTOP_XFCE: {
             "name": "Xfce Desktop",
             "icon": "preferences-desktop"
             },
           GROUP_DESKTOP_OTHER: {
             "name": "Other Desktops",
             "icon": "preferences-desktop"
             },
           GROUP_PUBLISHING: {
             "name": "Publishing",
             "icon": "accessories-dictionary"
             },
           GROUP_SERVERS: {
             "name": "Servers",
             "icon": "network-server"
             },
           GROUP_FONTS: {
             "name": "Fonts",
             "icon": "preferences-desktop-font"
             },
           GROUP_ADMIN_TOOLS: {
             "name": "Admin Tools",
             "icon": "application-x-shellscript"
             },
           GROUP_LEGACY: {
             "name": "Legacy",
             "icon": "media-floppy"
             },
           GROUP_LOCALIZATION: {
             "name": "Localization",
             "icon": "preferences-desktop-locale"
             },
           GROUP_VIRTUALIZATION: {
             "name": "Virtualization",
             "icon": "video-display"
             },
           GROUP_POWER_MANAGEMENT: {
             "name": "Power Management",
             "icon": "preferences-system-power-management"
             },
           GROUP_SECURITY: {
             "name": "Security",
             "icon": "preferences-desktop-cryptography"
             },
           GROUP_COMMUNICATION: {
             "name": "Communication",
             "icon": "internet-telephony"
             },
           GROUP_NETWORK: {
             "name": "Network",
             "icon": "network-workgroup"
             },
           GROUP_SCIENCE: {
             "name": "Science",
             "icon": "applications-science"
             },
           GROUP_ELECTRONICS: {
             "name": "Electronics",
             "icon": "utilities-system-monitor"
             },
           GROUP_DOCUMENTATION: {
             "name": "Documentation",
             "icon": "graphics-viewer-document"
             }
}

component_group_mappings = {
    "applications" : GROUP_OTHER,
    "applications.admin" : GROUP_ADMIN_TOOLS,
    "applications.archive" : GROUP_OTHER,
    "applications.dictionaries" : GROUP_OTHER,
    "applications.dictionaries.aspell" : GROUP_OTHER,
    "applications.doc" : GROUP_PUBLISHING,
    "applications.doc.docbook" : GROUP_PUBLISHING,
    "applications.editors" : GROUP_ACCESSORIES,
    "applications.editors.emacs" : GROUP_ACCESSORIES,
    "applications.emulators" : GROUP_OTHER,
    "applications.filesystems" : GROUP_OTHER,
    "applications.games" : GROUP_GAMES,
    "applications.hardware" : GROUP_OTHER,
    "applications.hardware.smartcard" : GROUP_SECURITY,
    "applications.multimedia" : GROUP_MULTIMEDIA,
    "applications.network" : GROUP_INTERNET,
    "applications.network.amsn" : GROUP_INTERNET,
    "applications.network.mozilla" : GROUP_INTERNET,
    "applications.pda" : GROUP_ACCESSORIES,
    "applications.powermanagement" : GROUP_POWER_MANAGEMENT,
    "applications.printing" : GROUP_PUBLISHING,
    "applications.science" : GROUP_SCIENCE,
    "applications.science.astronomy" : GROUP_SCIENCE,
    "applications.science.electronics" : GROUP_SCIENCE,
    "applications.science.mathematics" : GROUP_EDUCATION,
    "applications.science.robotics" : GROUP_SCIENCE,
    "applications.security" : GROUP_SECURITY,
    "applications.shells" : GROUP_ADMIN_TOOLS,
    "applications.tex" : GROUP_PUBLISHING,
    "applications.util" : GROUP_ACCESSORIES,
    "applications.virtualization" : GROUP_VIRTUALIZATION,
    "desktop.enlightenment" : GROUP_DESKTOP_OTHER,
    "desktop.enlightenment.base" : GROUP_DESKTOP_OTHER,
    "desktop.fluxbox" : GROUP_DESKTOP_OTHER,
    "desktop.fonts" : GROUP_FONTS,
    "desktop.freedesktop" : GROUP_DESKTOP_OTHER,
    "desktop.freedesktop.xorg" : GROUP_DESKTOP_OTHER,
    "desktop.freedesktop.xorg.lib" : GROUP_DESKTOP_OTHER,
    "desktop.gnome" : GROUP_DESKTOP_GNOME,
    "desktop.gnome.base" : GROUP_DESKTOP_GNOME,
    "desktop.kde" : GROUP_DESKTOP_KDE,
    "desktop.kde.base" : GROUP_DESKTOP_KDE,
    "desktop.kde.i18n" : GROUP_LOCALIZATION,
    "desktop.kde4" : GROUP_DESKTOP_KDE,
    "desktop.kde4.base" : GROUP_DESKTOP_KDE,
    "desktop.kde4.i18n" : GROUP_LOCALIZATION,
    "desktop.opencompositing" : GROUP_DESKTOP_OTHER,
    "desktop.opencompositing.cairo" : GROUP_DESKTOP_OTHER,
    "desktop.opencompositing.compiz" : GROUP_DESKTOP_OTHER,
    "desktop.opencompositing.kiba" : GROUP_DESKTOP_OTHER,
    "desktop.xfce4" : GROUP_DESKTOP_XFCE,
    "desktop.xfce4.base" : GROUP_DESKTOP_XFCE,
    "desktop.xfce4.goodies" : GROUP_DESKTOP_XFCE,
    "desktop.xfce4.themes" : GROUP_DESKTOP_XFCE,
    "kernel" : GROUP_SYSTEM,
    "kernel.drivers" : GROUP_SYSTEM,
    "kernel.firmware" : GROUP_SYSTEM,
    "programming" : GROUP_PROGRAMMING,
    "programming.environments" : GROUP_PROGRAMMING,
    "programming.environments.eclipse" : GROUP_PROGRAMMING,
    "programming.environments.eric" : GROUP_PROGRAMMING,
    "programming.languages" : GROUP_PROGRAMMING,
    "programming.languages.dotnet" : GROUP_PROGRAMMING,
    "programming.languages.gambas" : GROUP_PROGRAMMING,
    "programming.languages.haskell" : GROUP_PROGRAMMING,
    "programming.languages.java" : GROUP_PROGRAMMING,
    "programming.languages.lisp" : GROUP_PROGRAMMING,
    "programming.languages.pascal" : GROUP_PROGRAMMING,
    "programming.languages.perl" : GROUP_PROGRAMMING,
    "programming.languages.php" : GROUP_PROGRAMMING,
    "programming.languages.python" : GROUP_PROGRAMMING,
    "programming.languages.python.django" : GROUP_PROGRAMMING,
    "programming.languages.tcl" : GROUP_PROGRAMMING,
    "programming.libs" : GROUP_PROGRAMMING,
    "programming.tools" : GROUP_PROGRAMMING,
    "ptsp" : GROUP_SERVERS,
    "server" : GROUP_SERVERS,
    "server.database" : GROUP_SERVERS,
    "server.mail" : GROUP_SERVERS,
    "server.nis" : GROUP_SERVERS,
    "server.www" : GROUP_SERVERS,
    "system" : GROUP_SYSTEM,
    "system.base" : GROUP_SYSTEM,
    "system.devel" : GROUP_PROGRAMMING,
    "system.doc" : GROUP_SYSTEM,
    "system.locale" : GROUP_LOCALIZATION
}
