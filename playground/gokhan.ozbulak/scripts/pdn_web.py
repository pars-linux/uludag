#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

import sys
import os
import string
import bz2
import lzma
import urllib2
import piksemel
import pisi
import pickle

class PackageDiffNotify:

    def __init__(self):
        # URLs of Repositories
        # It is recommended to define self.REPO_LIST as from newest repo to oldest one
        self.REPO_LIST = (
                        "http://svn.pardus.org.tr/pardus/2011/devel/pisi-index.xml.bz2",
                        "http://svn.pardus.org.tr/pardus/corporate2/devel/pisi-index.xml.bz2",
                        "http://svn.pardus.org.tr/pardus/2009/devel/pisi-index.xml.bz2"
                    )

        # self.REPO_LIST = []

        # Details about packages
        # Structure : {packager_name -> {package_name -> {distro -> [release, version, #package, #patch, packager_mail, [sub-pack-list], component]}}}
        self.REPOS = {}
        self.RELEASE, self.VERSION, self.NRPACKAGES, self.NRPATCHES, self.MAIL, self.SUBPACKS, self.COMPONENT = range(7)
        self.PACKAGER, self.ID = range(2)

        # This stores packager list maintaining same package in different distributions
        # Structure : { package_name -> [packager_name1,..,packager_nameX]}
        self.CONFLICT_DICT = {}

        # This is used to specify which distro repos entry such as #patch is for
        self.DISTRO_LIST = []

        # This is mapping of obsolete package to the new package
        # Structure : {obsolete_package -> new_package}
        self.OBSOLETE_DICT = {}

        self.PACKAGERSDIR = os.path.join(os.getcwd(), "packagers")

        # self.find_index()

        # self.fetch_repos()

    def fetch_packagers(self):
        packagers = {}
        for p in self.REPOS.keys():
            packagers[p] = self.REPOS[p].values()[0].values()[0][self.MAIL]

        return packagers


    def master_fetch(self):
        self.fetch_repos()
        for packager,mail in self.fetch_packagers().items():
            # Serialize the object storing info about package(s) to keep it in file
            pickle.dump(self.REPOS[packager], open(os.path.join(self.PACKAGERSDIR, "%s.%s" %(packager, mail)), "w"))

    def handle_replaces(self, spec):
        ''' This function moves packagers of obsolete package into new package '''
        # Interested in the sub-package that has same name with the source name
        # Ignoring other sub-packages if any
        for package in spec.packages:
            if package.name == spec.source.name:
                for replace in package.replaces:
                    if not self.OBSOLETE_DICT.has_key(replace.package):
                        self.OBSOLETE_DICT[replace.package] = spec.source.name
                        # Move obsolete package as new package in self.CONFLICT_DICT
                        if self.CONFLICT_DICT.has_key(replace.package):
                            tmp_packager_list = self.CONFLICT_DICT[replace.package]
                            del self.CONFLICT_DICT[replace.package]
                            for tmp_packager in tmp_packager_list:
                                if tmp_packager not in self.CONFLICT_DICT[spec.source.name]:
                                    self.CONFLICT_DICT[spec.source.name].append(tmp_packager)

    def reset_subfields(self):
        self.REPOS = {}
        self.CONFLICT_DICT = {}
        self.DISTRO_LIST = []
        self.OBSOLETE_DICT = {}

    def fetch_repos(self):
        ''' This function reads source pisi index file as remote or local and constructs "repos" structure based on this file '''

        # This is due to re-call of fetch_repos function periodically to keep the packagers' files up-to-date
        self.reset_subfields()

        pisi_index = pisi.index.Index()
        for order, repo in enumerate(self.REPO_LIST):
            print "Parsing index file %s" % repo
            if repo.endswith(".bz2"):
                decompressed_index = bz2.decompress(urllib2.urlopen(repo).read())
            elif repo.endswith(".xz"):
                decompressed_index = lzma.decompress(urllib2.urlopen(repo).read())
            else:
                decompressed_index = urllib2.urlopen(repo).read()

            doc = piksemel.parseString(decompressed_index)
            pisi_index.decode(doc, [])

            # Populate self.DISTRO_LIST in order of iteration done for repositories
            self.DISTRO_LIST.append("%s %s" %(pisi_index.distribution.sourceName, pisi_index.distribution.version))

            for spec in pisi_index.specs:
                omitSpec = False

                if not self.REPOS.has_key(spec.source.packager.name):
                    self.REPOS[spec.source.packager.name] = {}
                if not self.REPOS[spec.source.packager.name].has_key(spec.source.name):
                    self.REPOS[spec.source.packager.name][spec.source.name] = {}
                self.REPOS[spec.source.packager.name][spec.source.name][self.DISTRO_LIST[order]] = ["", "", 0, 0, "", [], ""]

                self.REPOS[spec.source.packager.name][spec.source.name][self.DISTRO_LIST[order]][self.RELEASE] = spec.history[0].release
                self.REPOS[spec.source.packager.name][spec.source.name][self.DISTRO_LIST[order]][self.VERSION] = spec.history[0].version
                self.REPOS[spec.source.packager.name][spec.source.name][self.DISTRO_LIST[order]][self.NRPACKAGES] = len(spec.packages)
                self.REPOS[spec.source.packager.name][spec.source.name][self.DISTRO_LIST[order]][self.NRPATCHES] = len(spec.source.patches)
                self.REPOS[spec.source.packager.name][spec.source.name][self.DISTRO_LIST[order]][self.MAIL] = spec.source.packager.email

                # Inserting sub-packages if any
                for subpack in spec.packages:
                    self.REPOS[spec.source.packager.name][spec.source.name][self.DISTRO_LIST[order]][self.SUBPACKS].append(subpack.name)

                self.REPOS[spec.source.packager.name][spec.source.name][self.DISTRO_LIST[order]][self.COMPONENT] = spec.source.partOf

                # We may have multiple packagers as owner of the same package
                # residing on different repositories
                # In that case, we need to mark the package as in conflict and
                # be aware of it while sending mail to the packager
                if self.CONFLICT_DICT.has_key(spec.source.name):
                    if spec.source.packager.name not in self.CONFLICT_DICT[spec.source.name]:
                        self.CONFLICT_DICT[spec.source.name].append(spec.source.packager.name)
                else:
                    if self.OBSOLETE_DICT.has_key(spec.source.name):
                        # This control flow is redundant,if we have package in
                        # self.OBSOLETE_DICT, it should have been exist in self.CONFLICT_DICT
                        # The flow is here not to lose the track of code
                        if self.CONFLICT_DICT.has_key(self.OBSOLETE_DICT[spec.source.name]):
                            if spec.source.packager.name not in self.CONFLICT_DICT[self.OBSOLETE_DICT[spec.source.name]]:
                                self.CONFLICT_DICT[self.OBSOLETE_DICT[spec.source.name]].append(spec.source.packager.name)
                    else:
                        self.CONFLICT_DICT[spec.source.name] = [spec.source.packager.name]

                # Replaces check and handling
                self.handle_replaces(spec)

    def get_report(self, mail):
        for root, dirs, files in os.walk(self.PACKAGERSDIR):
            for name in files:
                if name.endswith(mail):
                    # De-serialize the object from byte-stream that is stored in the file
                    return pickle.load(open(os.path.join(root, name), "r"))

    def get_packagers(self):
        packagers = {}
        # for p in self.REPOS.keys():
        #    # packagers[p] = self.REPOS[p][self.REPOS[p].keys()[0]]self.REPOS[p][self.REPOS[p].keys()[0]][][self.MAIL]
        #    packagers[p] = self.REPOS[p].values()[0].values()[0][self.MAIL]
        for p in os.listdir(self.PACKAGERSDIR):
            packagers[p.split(".")[self.PACKAGER]] = p.split(".")[self.ID]

        return packagers

rep = PackageDiffNotify()
rep.master_fetch()
print rep.get_report("gozbulak@pardus.org.tr")["amsn"]
# rep.master_fetch()
# print rep.get_report("gozbulak@pardus.org.tr")

