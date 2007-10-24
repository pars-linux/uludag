#!/usr/bin/python
# -*- coding: utf-8 -*-

import comar
import pynotify

import gettext
gettext.bindtextdomain('network-manager', '/usr/kde/3.5/share/locale/')
gettext.textdomain('network-manager')
i18n = gettext.gettext

pynotify.init('Network-Manager')

def parseReply(reply):
    _dict = {}
    for node in reply:
        key,value = node.split('=',1)
        _dict[key] = value
    return _dict

def scanAndConnect(link=None,force=False):
    if not link:
        # If no Comar link given, create one
        link = comar.Link()

    # Notification Messages
    messages = []

    # Get Wireless Devices
    link.Net.Link['wireless-tools'].deviceList()
    res = link.read_cmd()
    devices = res.data.split('\n')

    # If there is no device, go on
    if not len(devices):
        return

    # Get current APs
    justEssIds = []
    temp = None
    for dev in devices:
        # Some times we need to scan twice to get all access points
        for x in range(2):
            link.Net.Link['wireless-tools'].scanRemote(device=dev)
            temp = link.read_cmd()
        if temp.data:
            scanResults = map(lambda x: parseReply(x.split('\t')),temp.data.split('\n'))
            map(lambda x: justEssIds.append(x['remote']),scanResults)
        else:
            messages.append('No scan result')
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
            if temp['remote'] in justEssIds:
                profiles.append(temp)

    # If there is one result let switch to it
    if len(profiles)==1:
        profile = profiles[0]['name']
        m = i18n("Profile '%s' matched.")
        messages.append(m % profile)
        messages.append(connect(link,profiles[0],force))
    elif not len(profiles):
        messages.append("There is no matched profile")
    else:
        messages.append("There is a lot of matched profile..")

    # Show notification messages if exists
    if len(messages)>0:
        for message in messages:
            _notify = pynotify.Notification(message)
            _notify.show()

def connect(comLink,profile,force=False):
    name = profile['name']
    if not profile['state']=='up' or force:
        comLink.Net.Link['wireless-tools'].setState(name=name,state='up')
        m = i18n("Connecting to '%s' ...")
        return m % name
    else:
        m = i18n("Already connected to '%s'")
        return m % name

if __name__=="__main__":
    scanAndConnect()

