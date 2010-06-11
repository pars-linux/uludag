import xml.dom.minidom
import urllib2

from logger import getLogger
log = getLogger("VersionManager")

class Version():
    def __repr__(self):
	return ' '.join((self.name, self.size, self.id))

class Mirror:
    pass

class VersionManager:
    _versions_file_path = 'versions.xml'
    _definitions_file_url = 'http://www.ahmetalpbalkan.com/versions.xml'
    proxyHost, proxyIP = '', ''
    
    def __init__(self):
        self.versions = []
	self.parseDefinitionsFile()
        
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
        self.versions = []
        
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
	ver.type = self._getText(version.getElementsByTagName("type")[0].childNodes)
        ver.id = (version.getAttribute("id"))
        mirrors = version.getElementsByTagName("mirrors")[0].getElementsByTagName("source")
        mirrorList = list()
        for mirror in mirrors:
            mirrorList.append(self._handleMirror(mirror))
        ver.mirrors  = mirrorList
        
        return ver
        
    def _handleMirror(self, mirror):
        mir = Mirror()
        fields = ["hostname", "country", "login", "username", "password", "port",
                  "path", "filename"]
        
        for field in fields:
            value = self._getText(mirror.getElementsByTagName(field)[0].childNodes)
            setattr(mir, field, value)

        return mir  
    
    def updateDefinitionsFile(self, loadUpdated = True):
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
	    err = "Could not reach version definitions URL. Check your internet connection."
            log.error(err)
	    return False

        if contents:
            try:
#                writestream = open(self._versions_file_path, 'w')
#                writestream.close()
		if loadUpdated:
		    self.parseDefinitionsFile()
		return True, None 
            except:
		err = 'Could not write to version definitions file.'
                log.error(err)
		return False, err


    def updateProxy(self, host, ip):
	self.proxyHost = host
	self.proxyIP = ip

    def __repr__(self):
	r = ''
	for v in self.versions:
	    r+= ' '.join((v.name, v.size, v.id, '\n'))
	    for m in v.mirrors:
		r+= ' '.join(('  ', m.hostname, m.country, m.port, m.username, m.password, m.path, '\n'))

	return r