#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#
#

import os

packageList = []

for dirname, dirnames, filenames in os.walk('.'):
    for filename in filenames:
        if filename.split(".")[-1] == "pisi":
            packageList.append(filename)

command = "pm-install "
for i in packageList:
    command+= i+" " 
    
print command 
os.system(command)
    
