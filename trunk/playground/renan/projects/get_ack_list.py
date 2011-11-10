#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
USAGE: ./get_ack_list.py packs_file awaiting_file Renan

Just copy and paste the contents from the email to a file

pack_file contains a list that has the "Source" key
    Ex: Source: kaptan (·
        http://packages.pardus.org.tr/info/2011/testing/source/kaptan.html )
        Version: 5.0.5
        Release: 89 (Fix Package Manager update interval. (Pa...)
        Owner: Renan Çakırerk

awaiting_file contains a list of package names and statuses
    Ex: U  kaptan-5.0.5-89-p11-x86_64.pisi
        U  kdebase-workspace-4.6.5-174-p11-x86_64.pisi
        U  kdebase-workspace-devel-4.6.5-174-p11-x86_64.pisi

Ten minutes coding challange wohoo!

"""
import sys

packs_file = sys.argv[1]
awaiting_file = sys.argv[2]
username = sys.argv[3]

pf = open(packs_file, "r")
packs = pf.read()

af = open(awaiting_file, "r")
awaiting = af.read()

flag = 0
pack_list = []

for pack in packs.split('\n\n\n'):
    if len(pack.split('\n')) == 6:
        if flag == 1 and len(pack.split('\n')) == 6 and not pack.split('\n')[0].__contains__('Source'):
            flag = 0
        if pack.split('\n')[0].startswith(username):
            flag = 1

    if flag == 1:
        det = pack.split('\n')

        for d in det:
            if d.__contains__('Source'):
                pack_list.append( d.split(' ')[-3] )

print pack_list


for a in awaiting.split('\n'):
    for p in pack_list:
        if a.__contains__(p):
            print a

