import piksemel
from sahipcore import *

    
class SahipGenerator:
    def __init__(self, language=None, #keymap=None,\
                  variant=None, root_password=None,\
                  timezone=None, hostname=None, users=None, \
                  partitioning_type=None, disk=None,\
                  reponame=None, repoaddr=None ):
        self.language = language
        #self.keymap = keymap
        self.variant = variant
        self.root_password = root_password
        self.timezone = timezone
        self.hostname = hostname
        self.users = users
        self.partitioning_type = partitioning_type
        self.disk = disk
        self.reponame = reponame
        self.repoaddr = repoaddr


        self.generate()
        
 
    def generate(self):
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
        
                

        f = open("/home/emre/Desktop/output.xml","w")
        f.write(xmlHeader+doc.toPrettyString())
        f.close()
        

pars = User("pars", "Panthera Pardus Tulliana", "pardus", ['audio', 'dialout', 'disk', 'pnp', 'pnpadmin', 'users', 'video', 'wheel'])
pars.autologin = True
caddy = User("caddy", "Panthera Pardus Caddy", "pardus", ['audio', 'dialout', 'disk', 'pnp', 'pnpadmin', 'users', 'video']
)

#x = SahipGenerator("tr", "q", "pardus", "Europe/Istanbul", "pardus-pc", [pars, caddy], "auto", "disk0", "testrepo", "http") 
