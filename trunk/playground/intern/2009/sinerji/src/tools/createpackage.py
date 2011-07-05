#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This script do some helpful automatic tasks in order:

-Get the pspec.xml file and assign to variable
-Create *.tar.gz package from the source
-Upload to my own host
-Get sha1sum from the package
-Write the sha1sum and packagename to pspec.xml
-Build the pisi package, and list the files to be installed
-It will ask you before install pisi package

Note: Thanks Emre Aladağ for inspiration ;)
"""

import os
import sys
import commands


pspec = "/home/fatih/uludag/trunk/staj-projeleri/paketler/fatih/applications/network/sinerji/pspec.xml" 
pspecyedek = pspec + "yedek"

os.system("python setup.py dist")
for file in os.listdir("."):
    if file.endswith("tar.gz"):
        packagename = file

print "Package created: ", packagename

os.system("scp %s farslan@arsln.org:arsln.org/dosya" % packagename)
print "Package sent"

shasum = commands.getoutput("sha1sum %s" % packagename).split()[0]
print "Sha1sum : %s" % shasum

output = ""
os.system("cp %s %s" % (pspec, pspecyedek))
if os.path.exists(pspec):
    for line in open(pspec, "r").readlines():
        if "<Archive sha1sum=" in line:
            toadd = '\t\t<Archive sha1sum="%s" type="targz">http://www.arsln.org/dosya/%s</Archive>\n' % (shasum ,packagename)
        else:
            toadd = line
        output+=toadd
    print "Sha1sum is added to ", pspec
else:
    print "%s doesn't exist" % pspec
f = open(pspec, "w")
f.write(output)
f.close()


for file in os.listdir("."):
    if file.endswith("tar.gz"):
        os.remove(file)


os.chdir("/home/fatih/uludag/trunk/staj-projeleri/paketler/fatih/applications/network/sinerji/")
os.system("sudo pisi bi pspec.xml")

for file in os.listdir("."):
    if file.endswith("pisi"):
        pisiname = file

os.system("lspisi %s" % pisiname)

yanit = raw_input("\n%s paketini kurmak istiyor musun? (evet/hayır): " % pisiname)

if yanit == ("e" or "evet") :
    os.system("sudo pisi it %s" % pisiname)
else:
    print "Paket kurulmadi"





