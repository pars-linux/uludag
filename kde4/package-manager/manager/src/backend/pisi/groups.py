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

(GROUP_ALL, GROUP_UNKNOWN, GROUP_ACCESSIBILITIY, GROUP_ACCESSORIES, GROUP_EDUCATION, GROUP_GAMES, GROUP_GRAPHICS,
 GROUP_INTERNET, GROUP_OFFICE, GROUP_OTHER, GROUP_PROGRAMMING, GROUP_MULTIMEDIA, GROUP_SYSTEM,
 GROUP_DESKTOP_KDE, GROUP_DESKTOP_GNOME, GROUP_DESKTOP_XFCE, GROUP_DESKTOP_OTHER, GROUP_PUBLISHING,
 GROUP_SERVERS, GROUP_FONTS, GROUP_ADMIN_TOOLS, GROUP_LEGACY, GROUP_LOCALIZATION, GROUP_VIRTUALIZATION,
 GROUP_POWER_MANAGEMENT, GROUP_SECURITY, GROUP_COMMUNICATION, GROUP_NETWORK, GROUP_SCIENCE,
 GROUP_ELECTRONICS, GROUP_DOCUMENTATION) = range(31)

groups = { GROUP_ALL : {
             "name": "All",
             "icon": "unknown"
             },
           GROUP_UNKNOWN : {
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
    "desktop" : GROUP_DESKTOP_OTHER,
    "desktop.font" : GROUP_FONTS,
    "desktop.gnome" : GROUP_DESKTOP_GNOME,
    "desktop.kde" : GROUP_DESKTOP_KDE,
    "desktop.kde.addon" : GROUP_DESKTOP_KDE,
    "desktop.kde.admin" : GROUP_DESKTOP_KDE,
    "desktop.kde.base" : GROUP_DESKTOP_KDE,
    "desktop.kde.l10n" : GROUP_LOCALIZATION,
    "desktop.kde3" : GROUP_DESKTOP_KDE,
    "desktop.kde3.addon" : GROUP_DESKTOP_KDE,
    "desktop.kde3.admin" : GROUP_DESKTOP_KDE,
    "desktop.kde3.base" : GROUP_DESKTOP_KDE,
    "desktop.kde3.l10n" : GROUP_LOCALIZATION,
    "desktop.lookandfeel" : GROUP_DESKTOP_OTHER,
    "desktop.misc" : GROUP_DESKTOP_OTHER,
    "desktop.toolkit" : GROUP_PROGRAMMING,
    "desktop.toolkit.gtk" : GROUP_PROGRAMMING,
    "desktop.toolkit.motif" : GROUP_PROGRAMMING,
    "desktop.toolkit.qt" : GROUP_PROGRAMMING,
    "desktop.toolkit.qt3" : GROUP_PROGRAMMING,
    "desktop.toolkit.qwt" : GROUP_PROGRAMMING,
    "editor" : GROUP_ACCESSORIES,
    "editor.emacs" : GROUP_ACCESSORIES,
    "editor.vi" : GROUP_ACCESSORIES,
    "editor.web" : GROUP_ACCESSORIES,
    "game" : GROUP_GAMES,
    "game.action" : GROUP_GAMES,
    "game.adventure" : GROUP_GAMES,
    "game.arcade" : GROUP_GAMES,
    "game.board" : GROUP_GAMES,
    "game.engine" : GROUP_GAMES,
    "game.fps" : GROUP_GAMES,
    "game.library" : GROUP_PROGRAMMING,
    "game.puzzle" : GROUP_GAMES,
    "game.rpg" : GROUP_GAMES,
    "game.simulation" : GROUP_GAMES,
    "game.sports" : GROUP_GAMES,
    "game.strategy" : GROUP_GAMES,
    "hardware" : GROUP_SYSTEM,
    "hardware.bluetooth" : GROUP_SYSTEM,
    "hardware.cpu" : GROUP_SYSTEM,
    "hardware.disk" : GROUP_SYSTEM,
    "hardware.emulator" : GROUP_SYSTEM,
    "hardware.firmware" : GROUP_SYSTEM,
    "hardware.graphics" : GROUP_SYSTEM,
    "hardware.info" : GROUP_SYSTEM,
    "hardware.irda" : GROUP_SYSTEM,
    "hardware.library" : GROUP_PROGRAMMING,
    "hardware.misc" : GROUP_SYSTEM,
    "hardware.mobile" : GROUP_SYSTEM,
    "hardware.optical" : GROUP_SYSTEM,
    "hardware.powermanagement" : GROUP_POWER_MANAGEMENT,
    "hardware.printer" : GROUP_SYSTEM,
    "hardware.scanner" : GROUP_SYSTEM,
    "hardware.security" : GROUP_SYSTEM,
    "hardware.smartcard" : GROUP_SYSTEM,
    "hardware.sound" : GROUP_SYSTEM,
    "hardware.virtualization" : GROUP_VIRTUALIZATION,
    "kernel" : GROUP_SYSTEM,
    "kernel.default" : GROUP_SYSTEM,
    "kernel.default.drivers" : GROUP_SYSTEM,
    "kernel.pae" : GROUP_SYSTEM,
    "kernel.pae.drivers" : GROUP_SYSTEM,
    "kernel.xen" : GROUP_SYSTEM,
    "multimedia" : GROUP_MULTIMEDIA,
    "multimedia.converter" : GROUP_MULTIMEDIA,
    "multimedia.editor" : GROUP_MULTIMEDIA,
    "multimedia.graphics" : GROUP_MULTIMEDIA,
    "multimedia.library" : GROUP_PROGRAMMING,
    "multimedia.plugin" : GROUP_MULTIMEDIA,
    "multimedia.radio" : GROUP_MULTIMEDIA,
    "multimedia.sound" : GROUP_MULTIMEDIA,
    "multimedia.stream" : GROUP_MULTIMEDIA,
    "multimedia.tv" : GROUP_MULTIMEDIA,
    "multimedia.video" : GROUP_MULTIMEDIA,
    "network" : GROUP_NETWORK,
    "network.analyzer" : GROUP_NETWORK,
    "network.chat" : GROUP_COMMUNICATION,
    "network.connection" : GROUP_NETWORK,
    "network.download" : GROUP_NETWORK,
    "network.fax" : GROUP_NETWORK,
    "network.filter" : GROUP_NETWORK,
    "network.ftp" : GROUP_NETWORK,
    "network.library" : GROUP_PROGRAMMING,
    "network.mail" : GROUP_NETWORK,
    "network.monitor" : GROUP_NETWORK,
    "network.p2p" : GROUP_NETWORK,
    "network.plugin" : GROUP_NETWORK,
    "network.remoteshell" : GROUP_NETWORK,
    "network.rss" : GROUP_NETWORK,
    "network.share" : GROUP_NETWORK,
    "network.voip" : GROUP_NETWORK,
    "network.web" : GROUP_NETWORK,
    "office" : GROUP_OFFICE,
    "office.dictionary" : GROUP_OFFICE,
    "office.docbook" : GROUP_OFFICE,
    "office.koffice" : GROUP_OFFICE,
    "office.library" : GROUP_PROGRAMMING,
    "office.misc" : GROUP_OFFICE,
    "office.openoffice" : GROUP_OFFICE,
    "office.postscript" : GROUP_OFFICE,
    "office.spellcheck" : GROUP_OFFICE,
    "office.tex" : GROUP_OFFICE,
    "programming" : GROUP_PROGRAMMING,
    "programming.build" : GROUP_PROGRAMMING,
    "programming.debug" : GROUP_PROGRAMMING,
    "programming.environment" : GROUP_PROGRAMMING,
    "programming.environment.eclipse" : GROUP_PROGRAMMING,
    "programming.environment.eric" : GROUP_PROGRAMMING,
    "programming.language" : GROUP_PROGRAMMING,
    "programming.language.dotnet" : GROUP_PROGRAMMING,
    "programming.language.gambas" : GROUP_PROGRAMMING,
    "programming.language.haskell" : GROUP_PROGRAMMING,
    "programming.language.java" : GROUP_PROGRAMMING,
    "programming.language.lisp" : GROUP_PROGRAMMING,
    "programming.language.pascal" : GROUP_PROGRAMMING,
    "programming.language.perl" : GROUP_PROGRAMMING,
    "programming.language.php" : GROUP_PROGRAMMING,
    "programming.language.python" : GROUP_PROGRAMMING,
    "programming.language.ruby" : GROUP_PROGRAMMING,
    "programming.language.tcl" : GROUP_PROGRAMMING,
    "programming.library" : GROUP_PROGRAMMING,
    "programming.microcontroller" : GROUP_PROGRAMMING,
    "programming.profiler" : GROUP_PROGRAMMING,
    "programming.tool" : GROUP_PROGRAMMING,
    "programming.vcs" : GROUP_PROGRAMMING,
    "science" : GROUP_SCIENCE,
    "science.astronomy" : GROUP_SCIENCE,
    "science.chemistry" : GROUP_SCIENCE,
    "science.electronics" : GROUP_SCIENCE,
    "science.library" : GROUP_PROGRAMMING,
    "science.mathematics" : GROUP_SCIENCE,
    "science.medical" : GROUP_SCIENCE,
    "science.robotics" : GROUP_SCIENCE,
    "server" : GROUP_SERVERS,
    "server.auth" : GROUP_SERVERS,
    "server.database" : GROUP_SERVERS,
    "server.ftp" : GROUP_SERVERS,
    "server.library" : GROUP_PROGRAMMING,
    "server.mta" : GROUP_SERVERS,
    "server.proxy" : GROUP_SERVERS,
    "server.ptsp" : GROUP_SERVERS,
    "server.web" : GROUP_SERVERS,
    "system" : GROUP_SYSTEM,
    "system.auth" : GROUP_SECURITY,
    "system.base" : GROUP_SYSTEM,
    "system.boot" : GROUP_SYSTEM,
    "system.devel" : GROUP_PROGRAMMING,
    "system.doc" : GROUP_UNKNOWN,
    "system.installer" : GROUP_SYSTEM,
    "util" : GROUP_ACCESSORIES,
    "util.admin" : GROUP_ACCESSORIES,
    "util.antivirus" : GROUP_ACCESSORIES,
    "util.apparmor" : GROUP_ACCESSORIES,
    "util.archive" : GROUP_ACCESSORIES,
    "util.crypt" : GROUP_ACCESSORIES,
    "util.misc" : GROUP_ACCESSORIES,
    "util.shell" : GROUP_ACCESSORIES,
    "x11" : GROUP_SYSTEM,
    "x11.driver" : GROUP_SYSTEM,
    "x11.im" : GROUP_SYSTEM,
    "x11.library" : GROUP_PROGRAMMING,
    "x11.misc" : GROUP_SYSTEM,
    "x11.server" : GROUP_SYSTEM,
    "x11.terminal" : GROUP_ACCESSORIES,
    "x11.util" : GROUP_ACCESSORIES
}

def groupNameToID(name):
    for gid in groups.keys():
        if groups[gid]["name"] == name:
            return gid
    return None

def getGroups():
    return list(set(groups.keys()))

def getGroupComponents(name):
    group = groupNameToID(name)
    components = []
    for name in component_group_mappings.keys():
        if component_group_mappings[name] == group:
            components.append(name)
    return components
