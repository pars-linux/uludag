#!/usr/bin/python
# -*- coding: utf-8 -*-

"""The XML generator module for Sahip."""

import piksemel
# from sahiplib import User   # Import user class we need to access the users

import gettext
__trans = gettext.translation('sahip', fallback=True)
_ = __trans.ugettext

class SahipGenerator:
    """Generates XML file with the information filled in the GUI Form."""
    def __init__(self, filename="~/Desktop/kahya.xml", language=None, \
                  variant=None, root_password=None, root_shadowed=False,\
                  timezone=None, hostname=None, users=None, \
                  partitioning_type=None, disk=None,\
                  reponame=None, repoaddr=None ):
        """Initializes the genarator with the information from the GUI Form."""
        self.filename = filename
        self.language = language
        self.variant = variant
        self.root_password = root_password
        self.root_shadowed = root_shadowed
        self.timezone = timezone
        self.hostname = hostname
        self.users = users
        self.partitioning_type = partitioning_type
        self.disk = disk
        self.reponame = reponame
        self.repoaddr = repoaddr        
 
    def generate(self):
        """Generates XML File with the attributes of the object."""
        
        # Put the constant header
        xmlHeader =  '''<?xml version="1.0" encoding="utf-8"?>
'''
        doc = piksemel.newDocument("yali")
        doc.setAttribute("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        doc.setAttribute("xsi:noNamespaceSchemaLocation","yalisema.xsd")
        
        # Set language and variant information
        doc.insertTag("language").insertData(self.language)
        if self.variant:
            doc.insertTag("variant").insertData(self.variant)
        
        # Root password: shadowed or not...
        if self.root_shadowed:
            srp = doc.insertTag("root_password")
            srp.insertData(self.root_password)
            srp.setAttribute("shadowed", "yes")
        else:                    
            doc.insertTag("root_password").insertData(self.root_password)
        
        # Timezone and hostname
        doc.insertTag("timezone").insertData(self.timezone)
        doc.insertTag("hostname").insertData(self.hostname)
                
        # ------ User Stuff ---------------
        # Note that if statement below can be removed if </users> tag is desired.
        if self.users:
            usersTag = doc.insertTag("users")
            for theuser in self.users:
                newuser = usersTag.insertTag("user")
                # If it is autologin, then set set an attribute to it.
                if theuser.autologin:
                    newuser.setAttribute("autologin","yes")
                
                # username and realName
                newuser.insertTag("username").insertData(theuser.username)
                newuser.insertTag("realname").insertData(theuser.realName)
            
                # Password: Normal or shadowed
                if theuser.shadowed:
                    sp = newuser.insertTag("password")
                    sp.insertData(theuser.shadowedPassword)
                    sp.setAttribute("shadowed", "yes")
                else:        
                    newuser.insertTag("password").insertData(theuser.normalPassword)
                
                # Groups for user.
                newuser.insertTag("groups").insertData(",".join(theuser.groups))      
        # ----- USER STUFF FINISHED --------
        
        # Repo and partitioning settings
        doc.insertTag("reponame").insertData(self.reponame)
        doc.insertTag("repoaddr").insertData(self.repoaddr)
        
        pt = doc.insertTag("partitioning")
        pt.insertData(self.disk)
        pt.setAttribute("partitioning_type", self.partitioning_type)
        
        # ------ ALL FINISHED -------------
        
        # Now try to write the XML File.        
        try:
            f = open(self.filename, "w")
            f.write(xmlHeader+doc.toPrettyString())
            f.close()
            return {'status'    : True,
                    'filename'  : self.filename
                    }
        except:
            # print _("Could not write to %s") % self.filename
            return {'status'    : False,
                    'filename'  : self.filename
                    }