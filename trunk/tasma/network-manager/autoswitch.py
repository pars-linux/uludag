#!/usr/bin/python
# -*- coding: utf-8 -*-

import comar

def parseReply(reply):
    _dict = {}
    for node in reply:
        key,value = node.split('=',1)
        _dict[key] = value
    return _dict

def scanAndConnect(link=None,force=False):
    if not link:
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
            print 'No scan result'
            return

    # Get profiles
    profiles = []
    temp = None

    link.Net.Link['wireless-tools'].connections()
    res = link.read_cmd()
    _profiles = res.data.split('\n')
    for profile in _profiles:
        
        # Get profile details
        link.Net.Link['wireless-tools'].connectionInfo(name=profile)
        res = link.read_cmd()
        temp = parseReply(res.data.split('\n'))

        # Add to list if in scanResults
        if temp['remote'] in justEssIds:
            profiles.append(temp)

    # If there is one result let switch to it
    if len(profiles)==1:
        profile = profiles[0]['name']
        print "Profile '%s' matched." % profile
        connect(link,profiles[0],force)
    else:
        print "There is a lot of matched profile.."

def connect(comLink,profile,force=False):
    name = profile['name']
    if profile['state']=='down' or force:
        print "Connecting to '%s'..." % name
        comLink.Net.Link['wireless-tools'].setState(name=name,state='up')
    else:
        print "Already connected to %s." % name

if __name__=="__main__":
    scanAndConnect()

