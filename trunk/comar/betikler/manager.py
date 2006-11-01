#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005,2006 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import string

notify("System.Manager.notify","started")

try:
    import pisi.api
    import pisi.installdb
    import pisi.packagedb
    import pisi.lockeddbshelve
    import pisi.ui
    import pisi.context
except KeyboardInterrupt:
    fail("System.Manager.cancelled")

class UI(pisi.ui.UI):
    def error(self, msg):
        notify("System.Manager.error","%s" % msg)

    def warning(self, msg):
        notify("System.Manager.warning","%s" % msg)

    def notify(self, event, **keywords):
        if event == pisi.ui.installing:
            data = ",".join(["installing", keywords["package"].name])
        elif event == pisi.ui.configuring:
            data = ",".join(["configuring", keywords["package"].name])
        elif event == pisi.ui.extracting:
            data = ",".join(["extracting", keywords["package"].name])
        elif event == pisi.ui.updatingrepo:
            data = ",".join(["updatingrepo", keywords["name"]])
        elif event == pisi.ui.removing:
            data = ",".join(["removing", keywords["package"].name])
        elif event == pisi.ui.cached:
            data = ",".join(["cached", keywords["name"], str(keywords["size"])])
        elif event == pisi.ui.installed:
            data = "installed"
        elif event == pisi.ui.removed:
            data = "removed"
        elif event == pisi.ui.upgraded:
            data = "upgraded"
        elif event == pisi.ui.packagestogo:
            data = ",".join(keywords["order"])
        else:
            return

        notify("System.Manager.notify","%s" % data)

    def ack(self, msg):
        return True

    def confirm(self, msg):
        return True

    def display_progress(self, operation, percent, info="", **kw):
        if operation == "fetching":
            out = "%s,%s,%d,%d,%s,%d,%d" % (operation, kw["filename"],percent,kw["rate"],kw["symbol"],
                                            kw["downloaded_size"],kw["total_size"])
        else:
            out = "%s,%d,%s" % (operation, percent, info)
        notify("System.Manager.progress", out)

def _init_pisi():
    ui = UI()
    try:
        pisi.api.init(ui=ui)
    except KeyboardInterrupt:
        cancelled()
    except pisi.lockeddbshelve.Error, e:
        notify("System.Manager.error","%s" % str(e))

def cancelled():
    if pisi.context.initialized:
        pisi.api.finalize()
    fail("System.Manager.cancelled")

def finished(operation=""):
    notify("System.Manager.finished", operation)

def installPackage(package=None):
    _init_pisi()
    if package:
        try:
            package = package.split(",")
            pisi.api.install(package)
            pisi.api.finalize()
        except KeyboardInterrupt:
            cancelled()
        except Exception,e:
            fail(unicode(e))
    finished("System.Manager.installPackage")

def updatePackage(package=None):
    _init_pisi()
    if package:
        try:
            package = package.split(",")
            pisi.api.upgrade(package)
            pisi.api.finalize()
        except KeyboardInterrupt:
            cancelled()
        except Exception,e:
            fail(unicode(e))
    finished("System.Manager.updatePackage")

def removePackage(package=None):
    _init_pisi()
    if package:
	try:
            package = package.split(",")
            pisi.api.remove(package)
            pisi.api.finalize()
        except KeyboardInterrupt:
            cancelled()
	except Exception, e:
	    fail(unicode(e))
    finished("System.Manager.removePackage")

def updateRepository(repo=None):
    _init_pisi()
    if repo:
	try:
            notify("System.Manager.updatingRepo","%s" % repo)
            pisi.api.update_repo(repo)
            pisi.api.finalize()
        except KeyboardInterrupt:
            cancelled()
	except Exception, e:
	    fail(unicode(e))
    finished("System.Manager.updateRepository")

def updateAllRepositories():
    _init_pisi()
    try:
        for repo in pisi.context.repodb.list():
            notify("System.Manager.updatingRepo","%s" % repo)
            pisi.api.update_repo(repo)
        pisi.api.finalize()
    except KeyboardInterrupt:
        cancelled()
    except Exception, e:
        fail(unicode(e))
    finished("System.Manager.updateAllRepositories")

def addRepository(name=None,uri=None):
    _init_pisi()
    if name and uri:
        try:
            pisi.api.add_repo(name,uri)
            pisi.api.finalize()
        except KeyboardInterrupt:
            cancelled()
        except Exception, e:
	    fail(unicode(e))
    finished("System.Manager.addRepository")

def removeRepository(repo=None):
    _init_pisi()
    if repo:
	try:
            pisi.api.remove_repo(repo)
            pisi.api.finalize()
        except KeyboardInterrupt:
            cancelled()
	except Exception, e:
	    fail(unicode(e))
    finished("System.Manager.removeRepository")

def installCritical():
    return "NotImplemented"

def getInstalled():
    _init_pisi()
    A = pisi.context.installdb.list_installed()
    A.sort(key=string.lower)
    return A

def getUpgradable(type="all"):
    _init_pisi()
    return pisi.api.list_upgradable()

def getPackageInfo(package=None):
    return "NotImplemented"

def getRepositories():
    _init_pisi()
    A = pisi.api.ctx.repodb.list()
    B = map(lambda x: "%s %s" % (x, pisi.api.ctx.repodb.get_repo(str(x)).indexuri.get_uri()), A)
    return "\n".join(B)

def setRepositories(repos=None):
    _init_pisi()
    if repos:
        try:
            notify("System.Manager.notify", "savingrepos")
            oldRepos = pisi.context.repodb.list()
            repoList = repos.split(",")
            index = 0

            for repo in oldRepos:
                pisi.api.remove_repo(repo)

            while index <= len(repoList)/2:
                pisi.api.add_repo(repoList[index],repoList[index+1])
                index = index + 2

            pisi.api.finalize()
        except KeyboardInterrupt:
            cancelled()
        except Exception, e:
            fail(unicode(e))
    finished("System.Manager.setRepositories")
