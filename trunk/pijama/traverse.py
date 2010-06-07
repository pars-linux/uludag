#!/usr/bin/python
# -*- coding: utf-8 -*-

import piksemel
import os
import sys
import datetime

sys.path.append(os.path.dirname(os.getcwd()))
os.environ['DJANGO_SETTINGS_MODULE'] = 'pijama.settings'
from webapp.models import *


def Traverse(path):

    xml=piksemel.parse(path)
    root=xml.getTag("RootPath")
    rootpath=root.getTagData("Path")
    repo=xml.getTag("RepoName")
    reponame=repo.getTagData("Dirname")
    return os.path.join(rootpath,reponame)

def changeToDate(dt):
    li=dt.split("-")
    return datetime.date(int(li[0]), int(li[1]), int(li[2]))


if __name__=="__main__":

    f=file("skipped.txt","w")

    #change this part according to your needs
    path="/home/oguz/neu/innova/people/oguz/pijama/cron"
    fullpath=os.path.join(path,"app.cfg")
    repopath=Traverse(fullpath)
    print "Repo Path: ", repopath

    for root, dirname, files in os.walk(repopath):
        for file in files:
            filepath=os.path.join(root,file)
            if os.path.isfile(filepath) and file == "pspec.xml":
                xml=piksemel.parse(os.path.join(root,"pspec.xml"))
                pkg=os.path.split(root)[-1]
                print root, file
                print "Package: ", pkg

                dateli=[]
                #save action for SourcePktTbl
                try:
                    source=xml.getTag("Source")
                    name=source.getTagData("Name")
                    license=source.getTagData("License")
                    homepage=source.getTagData("Homepage")
                    histories=xml.tags("History")
                    flag=True
                    version=None
                    for history in histories:
                        if history:
                            for h in history.tags("Update"):
                                dateli.append(h.getTagData("Date"))
                                if flag:
                                    version=h.getTagData("Version")
                                    flag=False

                except Exception, ex:
                    print ex
                    s=pkg+"\n"
                    f.write(s)
                    break
               
                added_date=changeToDate(dateli[-1]).strftime("%Y-%m-%d")
                last_change=changeToDate(dateli[0]).strftime("%Y-%m-%d")
                
                source=xml.getTag("Source")
                summary=source.getTagData("Summary")

                srcdetails=None
            
                # check whether the package is already in the db
                try:
                    srcdetails=SourcePktTbl.objects.get(pktname=pkg)
                    #overwriting, checking a date change is the logical way
                    srcdetails.added_date=added_date
                    srcdetails.last_change=last_change
                    srcdetails.summary=summary
                    srcdetails.version=version
                    srcdetails.license=license
                    srcdetails.homepage=homepage
                except:
                    srcdetails=SourcePktTbl(pktname=pkg, added_date=added_date, last_change=last_change, summary=summary, version=version, license=license, homepage=homepage)

                try:
                    srcdetails.save()
                    print "Source details are added."
                except Exception, ex:
                    print ex
                    sys.exit(1)

                # save action for BinaryPktTbl
                binaries=xml.tags("Package")
                binli=dict()
                for bin in binaries:
                    binname=bin.getTagData("Name")
                    smry=bin.getTagData("Summary")
                    if not smry:
                        binli[binname]=smry
                    else: binli[binname]=summary

                #deleting all related records, can be a dumy way but easy
                srcdetails.binarypkttbl_set.all().delete()
                
                for binpkg in binli:

                    bpkg=srcdetails.binarypkttbl_set.create(sourcepkt_name=pkg, binarypkt_name=binpkg, summary=summary, version=version)
                    try:
                        bpkg.save()
                        print "Binary details are added."
                    except Exception, ex:
                        print ex
                        sys.exit(1)

                # save action for PackagerTbl
                source=xml.tags("Source")

                #deleting all related records
                try:
                    srcdetails.packagertbl.delete()
                except:
                    pass

                for field in source:
                    pkgr=field.getTag("Packager")
                    name=pkgr.getTagData("Name")
                    email=pkgr.getTagData("Email")
                    packager=PackagerTbl(source=srcdetails, pktname=pkg, name=name, email=email)
                    try:
                        packager.save()
                        print "Packager details are added."
                    except Exception, ex:
                        print ex
                        sys.exit(1)

                # save action for PatchPktTbl
                source=xml.tags("Source")

                # deleting all related records
                try:
                    srcdetails.patchpkttbl_set.all().delete()
                except:
                    pass

                for node in source:
                    patches=node.getTag("Patches")
                    if patches:
                        for patch in patches.tags("Patch"):
                            ptchname=patch.firstChild().data()
                            level=patch.getAttribute("level")

                            ptch=srcdetails.patchpkttbl_set.create(pktname=pkg, patchname=ptchname, patch_level=level)
                            try:
                                ptch.save()
                                print "Patch details are added."
                            except Exception, ex:
                                print ex
                                sys.exit(1)

                # save action for SourcePktBuildDebsTbl
                source=xml.tags("Source")

                #deletng al related record
                try:
                    srcdetails.sourcepktbuilddebstbl_set.all().delete()
                except:
                    pass

                for node in source:
                    builddebs=node.getTag("BuildDependencies")
                    if builddebs:
                        for deb in builddebs.tags("Dependency"):
                            builddeb=deb.firstChild().data()
                            d=srcdetails.sourcepktbuilddebstbl_set.create(pktname=builddeb)
                        try:
                            d.save()
                            print "Build dependencies are saved"
                        except Exception, ex:
                            print ex
                            sys.exit(1)


                # save action for HistoryPktTbl
                # deleting all history related records, a dumy way, , should be inserting the last histories
                try:
                    srcdetails.historypkttbl_set.all().delete()
                except:
                    pass

                histories=xml.tags("History")
                for history in histories:
                    if history:
                        updates=history.tags("Update")
                        if updates:
                            for update in updates:
                                release=update.getAttribute("release")
                                update_date=update.getTagData("Date")
                                update_version=update.getTagData("Version")
                                comment=update.getTagData("Comment")
                                updater=update.getTagData("Name")

                                hstry=srcdetails.historypkttbl_set.create(pktname=pkg, update=release, update_date=update_date, update_version=update_version, comment=comment, updater=updater)

                                try:
                                    hstry.save()
                                    print "History details are added."
                                except Exception, ex:
                                    print ex
                                    sys.exit(1)


    f.close()
