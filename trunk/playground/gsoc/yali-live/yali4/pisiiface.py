#
# Copyright (C) 2005-2008, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# PiSi module for YALI

import os
import bz2
import time
import glob
import dbus
import pisi
import piksemel
import yali4.sysutils
import yali4.postinstall
from yali4.constants import consts
import yali4.gui.context as ctx
from yali4.gui.installdata import *

repodb = pisi.db.repodb.RepoDB()

class PackageCollection(object):
    def __init__(self, id, title, description, icon, translations, default=False):
        self.default = default
        self.id = id
        self.title = title
        self.description = description
        self.icon =  os.path.join(consts.pisi_collection_dir, icon)
        self.translations = translations
        self.index =  os.path.join(consts.source_dir, "repo/%s-index.xml.bz2" % id)

def initialize(ui, with_comar = False, nodestDir = False):
    options = pisi.config.Options()
    import yali4.gui.context as ctx
    ctx.debugger.log("Pisi initializing..")
    if not nodestDir:
        options.destdir = consts.target_dir
    options.yes_all = True
    options.ignore_dependency = True
    options.ignore_safety = True
    # wait for chrootDbus to initialize
    # generally we don't need this but I think this is safer
    for i in range(20):
        try:
            ctx.debugger.log("DBUS call..")
            bus = dbus.SystemBus()
            break
        except dbus.DBusException:
            time.sleep(1)
    pisi.api.set_dbus_sockname("%s/var/run/dbus/system_bus_socket" % options.destdir)

    try:
        pisi.api.set_dbus_timeout(1200)
    except AttributeError, e:
        # An old pisi running on disc, forget the dbus
        pass

    pisi.api.set_userinterface(ui)
    pisi.api.set_options(options)
    pisi.api.set_comar(with_comar)
    pisi.api.set_signal_handling(False)

def addRepo(name=None, uri=None):
    if name and uri:
        pisi.api.add_repo(name, uri)

def addCdRepo():
    if not repodb.has_repo(consts.cd_repo_name):
        addRepo(consts.cd_repo_name, consts.cd_repo_uri)
        updateRepo()

def addRemoteRepo(name, uri):
    if not repodb.has_repo(name):
        addRepo(name, uri)
        updateRepo(name)

def switchToPardusRepo(repo):
    if ctx.yali.install_type == YALI_LIVEINSTALL:
        addRepo(consts.pardus_repo_name, consts.pardus_repo_uri)
        yali4.postinstall.copyPisiIndex()
        removeRepo(repo)
    else:
        removeRepo(repo)
        addRepo(consts.pardus_repo_name, consts.pardus_repo_uri)


def updateRepo(name=consts.cd_repo_name):
    pisi.api.update_repo(name)

def removeRepo(name):
    pisi.api.remove_repo(name)

def regenerateCaches():
    pisi.db.regenerate_caches()

def takeBack(operation):
    # dirty hack for COMAR to find scripts.
    os.symlink("/",consts.target_dir + consts.target_dir)
    pisi.api.takeback(operation)
    os.unlink(consts.target_dir + consts.target_dir)

def getCollection():
    packageCollection = []
    default = False
    piksemelObj = None
    translations = {}

    def __setLocale(id, translations):
        title = ""
        description = ""
        locale = os.environ["LANG"].split(".")[0]
        if not translations.has_key(locale):
            ctx.debugger.log("Collection (%s) has no translation in %s locale. Default language (%s) is setting ..." %
                                                            (id, locale, translations["default"]))
            locale = translations["default"]

        title = translations[locale][0]
        description = translations[locale][1]
        return (title, description)

    try:
        piksemelObj = piksemel.parse(consts.pisi_collection_file)
    except OSError, msg:
        ctx.debugger.log("Unexcepted error:%s" % msg)
    else:
        for collection in piksemelObj.tags("Collection"):
            default = collection.getAttribute("default")
            if default:
                default = True

            id = collection.getTagData("id")
            icon = collection.getTagData("icon")
            translationsTag = collection.getTag("translations")
            translations["default"] = translationsTag.getAttribute("default")
            for translation in translationsTag.tags("translation"):
                translations[translation.getAttribute("language")]= (translation.getTagData("title"),
                                                                     translation.getTagData("description"))
            title, description = __setLocale(id, translations)
            packageCollection.append(PackageCollection(id, title, description, icon, translations, default))

    return packageCollection

def getCollectionPackages(collectionIndex, kernels=False):
    ctx.debugger.log("index_path%s" % collectionIndex)
    piksemelObj = piksemel.parseString(bz2.decompress(file(collectionIndex).read()))
    collectionPackages = []
    for package in piksemelObj.tags("Package"):
        # ignorekernel assignment changes kernel packages adding into package list
        if kernels:
            partof =  package.getTagData("PartOf")
            # Get collection packages without all kernel components
            if partof and partof.startswith("kernel"):
                continue
            else:
                tagData = package.getTagData("PackageURI")
        else:
            tagData = package.getTagData("PackageURI")
        collectionPackages.append(tagData)
    return collectionPackages

def getXmlObject(path):
    return piksemel.parseString(bz2.decompress(file(path).read()))

def getPackages(tag=None, value=None, index=None):
    if not index:
        index = os.path.join(consts.source_dir, "repo/pisi-index.xml.bz2")
    piksemelObj = piksemel.parseString(bz2.decompress(file(index).read()))
    ret = []
    for package in piksemelObj.tags("Package"):
        tagData = package.getTagData(tag)
        if tagData:
            for node in package.tags(tag):
                data = node.firstChild().data()
                #if (not data.find(':') == -1 and data.startswith(value)) or (data.find(':') == -1 and data == value):
                #Really don't understand why this control clauses used.
                if data.startswith(value):
                    ret.append("%s,%s" % (package.getTagData("PackageURI"), data))
    return ret

def mergePackagesWithRepoPath(packages):
    return map(lambda x: os.path.join(consts.source_dir, 'repo', x.split(',')[0]), packages)

def getNeededKernel(type, index):
    return mergePackagesWithRepoPath(filter(lambda x: x.split(',')[1].startswith(kernels[type]), getPackages("PartOf", "kernel", index)))

def getNotNeededLanguagePackages():
    return mergePackagesWithRepoPath(filter(lambda x: not x.split(',')[1].split(':')[1].startswith((consts.lang, "en")), getPackages("IsA", "locale:")))

def getBasePackages():
    systemBase = getPackages("PartOf", "system.base")
    systemBase.extend(getPackages("Name", "kernel"))
    systemBase.extend(getPackages("Name", "gfxtheme-pardus-boot"))
    return mergePackagesWithRepoPath(systemBase)

def getHistory(limit=50):
    pdb = pisi.db.historydb.HistoryDB()
    result = []
    i=0
    for op in pdb.get_last():
        # Dont add repo updates to history list
        if not op.type == 'repoupdate':
            result.append(op)
            i+=1
            if i==limit:
                break
    return result

def finalize():
    pass

def install(pkg_name_list):
    pisi.api.install(pkg_name_list, reinstall=False)

#def getAllCollectionPackagesWithPaths(collectionName):
#    packages = getCollectionPackages(collectionName)
#    # Get packages with their full paths
#    repoPackages = glob.glob('%s/repo/*.pisi' % consts.source_dir)
#    for package in packages:

def getAllPackagesWithPaths(collectionIndex="", use_sort_file=False, ignoreKernels=False) :
    packages = []

    if use_sort_file and os.path.exists("%s/repo/install.order" % consts.source_dir):
        # Read the installation order from the sort_list generated by pardusman
        # baselayout is explicitly moved to the top of the list in pardusman
        for package in [l.split(" ")[0] for l in open("%s/repo/install.order" % consts.source_dir, "r").readlines() if l]:
            packages.append(os.path.join(consts.source_dir, "repo", os.path.basename(package)))

    # DVD Collection Get Packages With Paths
    elif collectionIndex and not use_sort_file:
        # With dvd collection selection different kernel can be selected. If ignoreKernels is True collection package list return without kernel packages
        packages = mergePackagesWithRepoPath(getCollectionPackages(collectionIndex, kernels=ignoreKernels))
    else:
        # Get packages with their full paths
        packages = glob.glob('%s/repo/*.pisi' % consts.source_dir)

    # Make baselayout package first
    baselayout = None
    for package in packages:
        if 'baselayout' in package:
            baselayout = packages.index(package)
            break

    if baselayout:
        packages.insert(0, packages.pop(baselayout))

    return packages

def getAvailablePackages():
    return pisi.api.list_available()

def configurePending():
    # dirty hack for COMAR to find scripts.
    os.symlink("/",consts.target_dir + consts.target_dir)
    # Make baselayout configure first
    pisi.api.configure_pending(['baselayout'])
    # And all of pending packages
    pisi.api.configure_pending()
    os.unlink(consts.target_dir + consts.target_dir)

def checkPackageHash(pkg_name):
    repo_path = os.path.dirname(consts.cd_repo_uri)

    pkg = pisi.db.packagedb.PackageDB().get_package(pkg_name)
    file_name = pisi.util.package_name(pkg.name,
                                       pkg.version,
                                       pkg.release,
                                       pkg.build)
    file_hash = pisi.util.sha1_file(
        os.path.join(repo_path, file_name))

    if not pkg.packageHash == file_hash:
        raise Exception
