#!/usr/bin/python
# -*- coding: utf-8 -*-

import pynotify
import gettext

gettext.bindtextdomain('network-manager', '/usr/kde/3.5/share/locale/')
gettext.textdomain('network-manager')
i18n = gettext.gettext

FAIL, SUCCESS = pynotify.URGENCY_CRITICAL,pynotify.URGENCY_NORMAL

class autoSwitch:
    def __init__(self, comlink, notifier=True):
        self.notifier = False
        self.iconPath = ''
        self.comlink = comlink
        if notifier:
            if pynotify.init('autoswitch'):
                self.notifier = pynotify

    def setNotifier(self, notifier, iconPath=None):
        self.notifier = notifier
        self.iconPath = str(iconPath)

    def notify(self, message, mtype=SUCCESS, cancel=None, timeout=None):
        if not self.notifier:
            print message
            return
        if type(self.notifier) == pynotify.Notification:
            _notify = self.notifier
            _notify.clear_actions()
            _notify.update(i18n("Network Manager"), message,self.iconPath)
        else:
            _notify = self.notifier.Notification(i18n("Network Manager"), message)
        if mtype:
            _notify.set_urgency(mtype)
        if cancel:
            _notify.add_action('cancel', i18n("Cancel"), cancel)
        if timeout:
            _notify.set_timeout(timeout)
        _notify.show()

    def scanAndConnect(self, force=True):
        # Get wireless devices & profiles
        devices = []
        profiles = []
        for myhash, conn in self.comlink.connections.iteritems():
            if conn.script == 'wireless_tools':
                if conn.devid not in devices:
                    devices.append(conn.devid)
                profiles.append(conn)

        # If there is no wi-fi device, go on
        if not profiles or not devices:
            return

        # If already connected, go on
        for profile in profiles:
            if profile.state == "up":
                return

        self.notify(i18n("Scanning..."), SUCCESS)

        # Get current APs
        justEssIds = []
        justMacAddr = []

        def handler(remotes):
            if remotes:
                for remote in remotes:
                    justEssIds.append(remote['remote'])
                    justMacAddr.append(remote['mac'])
                # try to connect
                possibleProfile = None
                if len(profiles) == 1:
                    possibleProfile = profiles[0]
                else:
                    for mac in justMacAddr:
                        for profile in profiles:
                            if profile.apmac == mac and not possibleProfile:
                                possibleProfile = profile
                if possibleProfile:
                    m = i18n("Profile <b>%s</b> matched.")
                    self.notify(m % possibleProfile.name)
                    self.connect(possibleProfile, force)
                else:
                    self.notify(i18n("There is no matched profile"),FAIL)
            else:
                self.notify(i18n("No scan result"),FAIL)

        for dev in devices:
            ch = self.comlink.callHandler("wireless_tools", "Net.Link", "scanRemote", "tr.org.pardus.comar.net.link.get")
            ch.registerDone(handler)
            ch.call(dev)

    def connect(self, profile, force=False):
        profileName = profile.name
        if not profile.state.startswith('up') or force:
            m = i18n("Connecting to <b>%s</b> ...")
            self.notify(m % profileName)
            ch = self.comlink.callHandler("wireless_tools", "Net.Link", "setState", "tr.org.pardus.comar.net.link.setstate")
            ch.call(profileName, "up")

