#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006,2007 TUBITAK/UEKAE
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Please read the COPYING file.

""" Standart Python Modules """
import os

""" BuildFarm Modules """
import config
import dependency

class QueueManager:
    def __init__(self):
        self.workQueue = []
        self.waitQueue = []

        self.__deserialize__(self.workQueue, "workQueue")
        self.__deserialize__(self.waitQueue, "waitQueue")

        if len(self.waitQueue):
            self.workQueue += self.waitQueue
            self.waitQueue = []
        else:
            self.waitQueue = dependency.DependencyResolver(self.waitQueue).resolvDependencies()

        self.workQueue = dependency.DependencyResolver(self.workQueue).resolvDependencies()
        self.__serialize__(self.waitQueue, "waitQueue")
        self.__serialize__(self.workQueue, "workQueue")
        
    def __del__(self):
        self.__serialize__(self.waitQueue, "waitQueue")
        self.__serialize__(self.workQueue, "workQueue")

    def __serialize__(self, queueName, fileName):
        try:
            queue = open(os.path.join(config.workDir, fileName), "w")
        except IOError:
            return

        for pspec in queueName:
            queue.write("%s\n" % pspec)
        queue.close()

    def __deserialize__(self, queueName, fileName):
        try:
            queue = open(os.path.join(config.workDir, fileName), "r")
        except IOError:
            return

        for line in queue.readlines():
            if not line.startswith("#"):
                queueName.append(line.strip("\n"))
        queue.close()
    
    def __initWorkQueueFromFile__(self):
        self.workQueue = []
        self.__deserialize__(self.workQueue, "workQueue")
        
    def __initWaitQueueFromFile__(self):
        self.waitQueue = []
        self.__deserialize__(self.waitQueue, "waitQueue")

    def getWorkQueue(self):
        self.__initWorkQueueFromFile__()
        return self.workQueue

    def getWaitQueue(self):
        self.__initWaitQueueFromFile__()
        return self.waitQueue

    def removeFromWaitQueue(self, pspec):
        self.__initWaitQueueFromFile__()
        if self.waitQueue.__contains__(pspec):
            self.waitQueue.remove(pspec)
            self.__serialize__(self.waitQueue, "waitQueue")
            return True
        return False

    def removeFromWorkQueue(self, pspec):
        self.__initWorkQueueFromFile__()
        if self.workQueue.__contains__(pspec):
            self.workQueue.remove(pspec)
            self.__serialize__(self.workQueue, "workQueue")
            return True
        return False

    def appendToWorkQueue(self, pspec):
        self.__initWorkQueueFromFile__()
        if not self.workQueue.__contains__(pspec):
            self.workQueue.append(pspec)
            self.__serialize__(self.workQueue, "workQueue")
            return True
        return False

    def appendToWaitQueue(self, pspec):
        self.__initWaitQueueFromFile__()
        if not self.waitQueue.__contains__(pspec):
            self.waitQueue.append(pspec)
            self.__serialize__(self.waitQueue, "waitQueue")
            return True
        return False

    def transferToWorkQueue(self, pspec):
        if self.appendToWorkQueue(pspec):
            self.removeFromWaitQueue(pspec)
            return True
        return False

    def transferToWaitQueue(self, pspec):
        if self.appendToWaitQueue(pspec):
            self.removeFromWorkQueue(pspec)
            return True
        return False
