#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Please read the COPYING file.
#

""" Standart Python Modules """
import os

""" BuildFarm Modules """
import buildfarm.config as config
import buildfarm.dependency as dependency

class QError(Exception):
    pass

class QueueManager:
    def __init__(self):
        self.workQueue = []
        self.waitQueue = []
        
        self.__deserialize(self.workQueue, "workQueue")
        self.__deserialize(self.waitQueue, "waitQueue")
        
        if len(self.waitQueue):
            self.workQueue += self.waitQueue
            self.waitQueue = []
        else:          
            self.waitQueue = dependency.DependencyResolver(self.waitQueue).resolvDeps()
            
        self.workQueue = dependency.DependencyResolver(self.workQueue).resolvDeps()
        
    def __del__(self):       
        self.__serialize(self.waitQueue, "waitQueue")
        self.__serialize(self.workQueue, "workQueue")
        
    def __serialize(self, queueName, fileName):
        try:
            queue = open(os.path.join(config.workDir, fileName), "w")
        except IOError:
            return
        
        for pspec in queueName:            
            queue.write("%s\n" % pspec)
        queue.close()

    def __deserialize(self, queueName, fileName):
        try:
            queue = open(os.path.join(config.workDir, fileName), "r")
        except IOError:
            return
        
        for line in queue.readlines():            
            if not line.startswith("#"):
                queueName.append(line.strip("\n"))
        queue.close()

    def removeFromWaitQueue(self):
        if self.waitQueue.__contains__(pspec):
            self.waitQueue.remove(pspec)
        
    def removeFromWorkQueue(self, pspec):
        if self.workQueue.__contains__(pspec):
            self.workQueue.remove(pspec)
        
    def appendToWorkQueue(self, pspec):
         if not self.workQueue.__contains__(pspec):
            self.workQueue.append(pspec)
            self.__serialize(self.workQueue, "workQueue")

    def appendToWaitQueue(self, pspec):
         if not self.waitQueue.__contains__(pspec):
            self.waitQueue.append(pspec)
            self.__serialize(self.waitQueue, "waitQueue")

    def transferToWorkQueue(self, pspec):
        self.appendToWorkQueue(pspec)
        self.removeFromWaitQueue(pspec)
        
    def transferToWaitQueue(self, pspec):
        self.appendToWaitQueue(pspec)
        self.removeFromWorkQueue(pspec)
        
