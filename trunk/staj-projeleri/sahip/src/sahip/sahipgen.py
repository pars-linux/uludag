#!/usr/bin/python
# -*- coding: utf-8 -*-

"""The XML generator module for Sahip."""

import piksemel
from sahipcore import User

import gettext
__trans = gettext.translation('sahip', fallback=True)
_ = __trans.ugettext

class SahipGenerator:
    """Generates XML file with the information filled in the GUI Form."""
    def __init__(self, filename="~/Desktop/kahya.xml", language=None,\
                  variant=None, root_password=None,\
                  timezone=None, hostname=None, users=None, \
                  partitioning_type=None, disk=None,\
                  reponame=None, repoaddr=None ):
        """Initializes the genarator with the information from the GUI Form."""
        self.filename = filename
        self.language = language
        self.variant = variant
        self.root_password = root_password
        self.timezone = timezone
        self.hostname = hostname
        self.users = users
        self.partitioning_type = partitioning_type
        self.disk = disk
        self.reponame = reponame
        self.repoaddr = repoaddr
        
 
    def generate(self):
        """Generates XML File with the attributes of the object."""
        xmlHeader =  '''<?xml version="1.0" encoding="utf-8"?>
'''
        doc = piksemel.newDocument("yali")
        doc.setAttribute("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        doc.setAttribute("xsi:noNamespaceSchemaLocation","yalisema.xsd")
        
        doc.insertTag("language").insertData(self.language)
        if self.variant: doc.insertTag("variant").insertData(self.variant)        
        doc.insertTag("root_password").insertData(self.root_password)
        doc.insertTag("timezone").insertData(self.timezone)
        doc.insertTag("hostname").insertData(self.hostname)
                
        # USERS
        usersTag = doc.insertTag("users")
        for theuser in self.users:
            newuser = usersTag.insertTag("user")
            if theuser.autologin:
                newuser.setAttribute("autologin","yes")
            newuser.insertTag("username").insertData(theuser.username)
            newuser.insertTag("realname").insertData(theuser.realname)
            newuser.insertTag("password").insertData(theuser.password)
            newuser.insertTag("groups").insertData(",".join(theuser.groups))      
        
        doc.insertTag("reponame").insertData(self.reponame)
        doc.insertTag("repoaddr").insertData(self.repoaddr)
        pt = doc.insertTag("partitioning")
        pt.insertData(self.disk)
        pt.setAttribute("partitioning_type", self.partitioning_type)
        
                
        try:
            f = open(self.filename, "w")
            f.write(xmlHeader+doc.toPrettyString())
            f.close()
            return {'status'    : True,
                    'filename'  : self.filename
                    }
        except:
            print _("Could not write to %s" % self.filename)
            return {'status'    : False,
                    'filename'  : self.filename
                    }