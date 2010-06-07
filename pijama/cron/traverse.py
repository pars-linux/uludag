#!/usr/bin/python
# -*- coding: utf-8 -*-

import piksemel
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
os.environ['DJANGO_SETTINGS_MODULE'] = 'pijama.settings'
from pijama.webapp.models import *

#imaginary py files
import sourcepkg
#import binarypkg
#import packager
#import patchpkg

def Traverse(path):

    xml=piksemel.parse(path)
    root=xml.getTag("RootPath")
    rootpath=root.getTagData("Path")
    repo=xml.getTag("RepoName")
    reponame=repo.getTagData("Dirname")
    return os.path.join(rootpath,reponame)


if __name__=="__main__":
    #change this part according to your needs
    path="/home/oguz/neu/innova/people/oguz/pijama/cron/app.cfg"
    cfgpath=Traverse(path)

    for root, dirname, files in os.walk(cfgpath):
        for file in files:
            filepath=os.path.join(root,file)
            if os.path.isfile(filepath) and (file == "pspec.xml" or file == "actions.py"):
                xml=piksemel.parse(os.path.join(root,"pspec.xml"))
                pkg=os.path.split(filepath)[-1]

                #save action for SourcePktTbl
                package=sourcepkg.SourceDetails(pkg)
                
                added_date=package.get_added_date()
                last_change=package.last_change_date()
                srcdetails=SourcePktTbl(pktname=package, added_date=added_date, last_change=last_change)
                try:
                    srcdetails.save()
                except Exception, ex:
                    print ex

                # save action for BinaryPktTbl
                binaries=xml.tags("Package")
                binli=map(lambda x: x.getTagData("Name"), binaries)
                for binpkg in binli:
                    bpkg=BinaryPktTbl(sourcepkt_name=package, binarypkt_name=binpkg)
                    try:
                        bpkg.save()
                    except Exception, ex:
                        print ex

                # save action for PackagerTbl
                source=xml.tags("Source")
                for field in source:
                    pkgr=source.getTag("Packager")
                    name=pkgr.getTagData("Name")
                    email=pkgr.getTagData("Email")
                    packager=PackagerTbl(pktname=package, name=name, email=email)
                    try:
                        packager.save()
                    except Exception, ex:
                        print ex

                # save action for PatchPktTbl
                source=xml.tags("Source")
                for field in source:
                    patches=field.getTag("Patches")
                    ptchname=patches.getTagData("Patch")
                    level=None
                    p=patches.getTag("Patch")
                    if p.attributes:
                        level=p.getAttribute("level")
                    
                    ptch=PatchPktTbl(pktname=package, patchname=ptchname, patch_level=level)
                    try:
                        ptch.save()
                    except Exception, ex:
                        print ex



























