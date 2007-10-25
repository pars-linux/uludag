#!/usr/bin/python
# -*- coding: utf-8 -*-

import comar
import pynotify

import gettext
gettext.bindtextdomain('network-manager', '/usr/kde/3.5/share/locale/')
gettext.textdomain('network-manager')
i18n = gettext.gettext

pynotify.init('Network-Manager')

FAIL,SUCCESS = pynotify.URGENCY_CRITICAL,pynotify.URGENCY_NORMAL

def parseReply(reply):
    _dict = {}
    for node in reply:
        key,value = node.split('=',1)
        _dict[key] = value
    return _dict

def notify(message,type=None):
    _notify = pynotify.Notification(message)
    if type:
        _notify.set_urgency(type)
    _notify.show()

def scanAndConnect(link=None,force=False):
    if not link:
        # If no Comar link given, create one
        link = comar.Link()

    # Get Wireless Devices
    link.Net.Link['wireless-tools'].deviceList()
    res = link.read_cmd()
    devices = res.data.split('\n')

    # If there is no device, go on
    if not len(devices):
        return

    # Get current APs
    justEssIds = []
    justMacAddr= []
    temp = None
    for dev in devices:
        # Some times we need to scan twice to get all access points
        for x in range(2):
            link.Net.Link['wireless-tools'].scanRemote(device=dev)
            temp = link.read_cmd()
        if temp.data:
            scanResults = map(lambda x: parseReply(x.split('\t')),temp.data.split('\n'))
            map(lambda x: justEssIds.append(x['remote']),scanResults)
            map(lambda x: justMacAddr.append(x['mac']),scanResults)
        else:
            notify('No scan result',FAIL)
            return

    # Get profiles
    profiles = []
    temp = None

    link.Net.Link['wireless-tools'].connections()
    res = link.read_cmd()
    _profiles = res.data.split('\n')
    for profile in _profiles:
        try:
            # Get profile details
            link.Net.Link['wireless-tools'].connectionInfo(name=profile)
            res = link.read_cmd()
            temp = parseReply(res.data.split('\n'))
        except:
            pass

        # Add to list if in scanResults
        if temp:
            if temp['remote'] in justEssIds\
                    or temp.get('apmac','') in justMacAddr:
                profiles.append(temp)

    possibleProfile = None
    # If there is one result let switch to it
    if len(profiles)==1:
        possibleProfile = profiles[0]
    else:
        for result in scanResults:
            for profile in profiles:
                    if profile.get('apmac','')==result['mac'] and not possibleProfile:
                        possibleProfile = profile

    if possibleProfile:
        m = i18n("Profile '%s' matched.")
        notify(m % possibleProfile['name'])
        connect(link,possibleProfile,force)
    else:
        notify(i18n("There is no matched profile"),FAIL)

def connect(comLink,profile,force=False):
    profileName = profile['name']
    if not profile['state'].startswith('up') or force:
        comLink.Net.Link['wireless-tools'].setState(name=profileName,state='up')
        m = i18n("Connecting to '%s' ...")
        notify(m % profileName)
    else:
        m = i18n("Already connected to '%s'")
        notify(m % profileName)

if __name__=="__main__":
    scanAndConnect()

