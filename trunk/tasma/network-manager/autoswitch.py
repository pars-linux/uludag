#!/usr/bin/python
# -*- coding: utf-8 -*-

import comar

def parseReply(reply):
    _dict = {}
    for node in reply:
        key,value = node.split('=',1)
        _dict[key] = value
    return _dict

def scanAndConnect():
    link = comar.Link()

    # Get Wireless Devices
    link.Net.Link['wireless-tools'].deviceList()
    devices = link.read_cmd().data.split('\n')

    # If there is no device, go on
    if not len(devices):
        return

    # Get current APs
    for dev in devices:
        # Some times we need to scan twice to get all access points
        for x in range(2):
            link.Net.Link['wireless-tools'].scanRemote(device=dev)
        scanResults = map(lambda x: parseReply(x.split('\t')),link.read_cmd().data.split('\n'))

    # Clear the queue
    link.read_cmd()

    # Get profiles
    profiles = []
    link.Net.Link['wireless-tools'].connections()
    _profiles = link.read_cmd().data.split('\n')
    for profile in _profiles:
        # Get profile details
        link.Net.Link['wireless-tools'].connectionInfo(name=profile)
        profiles.append(parseReply(link.read_cmd().data.split('\n')))
        #print link.read_cmd().data.split('\n')

    # Clear the queue
    #link.read_cmd()
    
    print profiles
    print "-----------"
    print scanResults
    print "-----------"

scanAndConnect()
