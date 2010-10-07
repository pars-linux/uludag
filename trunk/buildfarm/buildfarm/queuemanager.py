#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2010 TUBITAK/UEKAE
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Please read the COPYING file.
#

import os

from buildfarm import dependency, utils
from buildfarm.config import configuration as conf

# PiSi module to get pspec path from package name using component name
from pisi.db.installdb import InstallDB

class QueueManager:
    def __init__(self):
        self.workQueue = []
        self.waitQueue = []

        self.__deserialize(self.workQueue, "workQueue")
        self.__deserialize(self.waitQueue, "waitQueue")

        # Ignore empty lines
        self.workQueue = list(set([s for s in self.workQueue if s]))
        self.waitQueue = list(set([s for s in self.waitQueue if s]))

        self.waitQueue = dependency.DependencyResolver(self.waitQueue).resolvDeps()
        self.workQueue = dependency.DependencyResolver(self.workQueue).resolvDeps()

    def __del__(self):
        self.__serialize(self.waitQueue, "waitQueue")
        self.__serialize(self.workQueue, "workQueue")

    def __serialize(self, queueName, fileName):
        try:
            queue = open(os.path.join(conf.workdir, fileName), "w")
        except IOError:
            return

        for pspec in queueName:
            queue.write("%s\n" % pspec)
        queue.close()

    def __deserialize(self, queueName, fileName):
        try:
            queue = open(os.path.join(conf.workdir, fileName), "r")
        except IOError:
            return

        for line in queue.readlines():
            if not line.startswith("#"):
                line = line.strip()
                if not os.path.exists(line):
                    # Try to guess absolute path from package name
                    try:
                        component = InstallDB().get_package(line).partOf
                    except:
                        continue

                    if component:
                        path = "%s/%s/%s/pspec.xml" % (utils.get_local_repository_url(), component.replace(".", "/"), line)

                        if os.path.exists(path):
                            queueName.append(path)
                else:
                    queueName.append(line)

        queue.close()

    def getAllPackages(self, resolved = True):
        if resolved:
            return dependency.DependencyResolver(list(set(self.workQueue + self.waitQueue))).resolvDeps()
        else:
            list(set(self.workQueue + self.waitQueue))

    def removeFromWaitQueue(self, pspec):
        if self.waitQueue.__contains__(pspec):
            self.waitQueue.remove(pspec)

    def removeFromWorkQueue(self, pspec):
        if self.workQueue.__contains__(pspec):
            self.workQueue.remove(pspec)

    def appendToWorkQueue(self, pspec):
        if not pspec in self.workQueue:
            self.workQueue.append(pspec)
            self.__serialize(self.workQueue, "workQueue")

    def appendToWaitQueue(self, pspec):
        if not pspec in self.waitQueue:
            self.waitQueue.append(pspec)
            self.__serialize(self.waitQueue, "waitQueue")

    def extendWaitQueue(self, pspecList):
        self.waitQueue = list(set(self.waitQueue + pspecList))
        self.__serialize(self.waitQueue, "waitQueue")

    def extendWorkQueue(self, pspecList):
        self.workQueue = list(set(self.workQueue + pspecList))
        self.__serialize(self.workQueue, "workQueue")

    def transferToWorkQueue(self, pspec):
        self.appendToWorkQueue(pspec)
        self.removeFromWaitQueue(pspec)

    def transferAllPackagesToWorkQueue(self):
        self.workQueue = list(set(self.workQueue + self.waitQueue))
        self.workQueue = dependency.DependencyResolver(self.workQueue).resolvDeps()
        self.waitQueue = []

    def transferToWaitQueue(self, pspec):
        self.appendToWaitQueue(pspec)
        self.removeFromWorkQueue(pspec)
