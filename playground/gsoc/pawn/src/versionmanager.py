import xml.dom.minidom
import urllib2

class Version:
    pass

class Mirror:
    pass

class VersionManager:
    _versions_file_path = 'versions.xml'
    _definitions_file_url = 'http://N/A'
    
    def __init__(self):
        self.versions = []
        
    def readFromFile(self):
        try:
            with open(self._versions_file_path,'r') as definitionsFile:
                self._xmlContent = definitionsFile.read()
        except IOError as err:
            log.error("Could not read version definitions file.")
            

    # a module for extracting texts in a nodelist
    def _getText(self, nodelist):
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)
        
    # assume that the XML scheme is:
    # + pardus 
    #   + version
    #        id,name,size etc.
    #        mirrors
    #          + mirror
    #              hostname, login, username etc.
    #          + mirror
    #              ...
    #   + version...
    def parseDefinitionsFile(self):
        self.readFromFile()
        self.versions = list()
        
        try:
            dom = xml.dom.minidom.parseString(self._xmlContent)
            versions = dom.getElementsByTagName("pardus")[0].getElementsByTagName("version")
            for version in versions:
                self.versions.append(self._handleVersion(version))
        except:
            log.error("Error while parsing definitions XML file.")

    def _handleVersion(self, version):
        ver = Version()
        
        ver.size = self._getText(version.getElementsByTagName("size")[0].childNodes)
        ver.name = self._getText(version.getElementsByTagName("name")[0].childNodes)
        ver.id = (version.getAttribute("id"))
        mirrors = version.getElementsByTagName("mirrors")
        mirrorList = list()
        for mirror in mirrors:
            mirrorList.append(self._handleMirror(mirror))
        ver.mirrors  = mirrorList
        
        return ver
        
    def _handleMirror(self, mirror):
        mir = Mirror()
        fields = ["hostname", "login", "username", "password", "port", 
                  "path", "filename"]
        
        for field in fields:
            value = self._getText(mirror.getElementsByTagName(field)[0].childNodes)
            setattr(mir, field, value)
        
        return mir  
    
    def updateDefinitionsFile(self):
        contents = ''
        try:
            stream = urllib2.urlopen(self._definitions_file_url)
            while True:
                buf = stream.read(1024)
                if not len(buf):
                    break
                else:
                    contents += buf
        except:
            log.error("Could not reach version definitions URL.")

        if contents:
            try:
                writestream = open(self._versions_file_path, 'w')
                writestream.close()
            except:
                log.error("Could not write to version definitions file.")
