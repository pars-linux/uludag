import xml.dom.minidom
from PyQt4.QtNetwork import QHttp
from PyQt4 import QtCore
from utils import levenshtein

import logger
log = logger.getLogger("VersionManager")

class Version():
    def __repr__(self):
	return ' '.join((self.name, self.size, self.id, self.md5sum))

class Mirror:
    pass

class VersionManager():
    _versions_file_path = 'versions.xml'
    _update_host = 'www.ahmetalpbalkan.com'
    _update_path = '/versions.xml'
    proxyHost, proxyIP = '', ''
    updateContents = ''

    def __init__(self):
        self.versions = []
	self.parseDefinitionsFile()

	self.http = QHttp(None)
        QtCore.QObject.connect(self.http, QtCore.SIGNAL('readyRead(QHttpResponseHeader)'), self.updateProgress)
	QtCore.QObject.connect(self.http, QtCore.SIGNAL('done(bool)'), self.updateFinished)
	

    def updateProxy(self, host, ip):
	self.proxyHost = host
	self.proxyIP = ip

    def useProxy(self):
	if self.proxyHost and self.proxyIP:
	    self.http.setProxy(self.proxyHost, int(self.proxyIP))
	    log.error('Proxy activated in update transfer.')

    def readFromFile(self):
        try:
            with open(self._versions_file_path,'r') as definitionsFile:
                self._xmlContent = definitionsFile.read()
        except IOError:
	    self.err = "Could not read version definitions file."
            log.error(self.err)
            

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
	    self.err = "Error while parsing definitions XML file."
            log.error(self.err)

    def _handleVersion(self, version):
        ver = Version()
        fields = ["size", "name", "type", "minmemory", "memory", "minspace",
                  "space", "md5sum", "kernel", "kernelparams", "initrd", "img"]

	for field in fields:
	    value =self._getText(version.getElementsByTagName(field)[0].childNodes).encode('utf8')
	    setattr(ver, field, value)
	ver.id = version.getAttribute("id").encode('utf8')
	
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
            value = self._getText(mirror.getElementsByTagName(field)[0].childNodes).encode('utf8')
            setattr(mir, field, value)

        return mir  
    
    def updateDefinitionsFile(self):
	self.useProxy()
	self.http.setHost(self._update_host)
	self.http.get(self._update_path)
	self.http.close()

    def	updateProgress(self, header):
	self.updateContents += self.http.readAll()

    def updateFinished(self, bool):
	if True:
	    if self.updateContents:
		log.debug('Update file retrieved successfully.')
		try:
		    writestream = open(self._versions_file_path, 'w')
		    writestream.write(self.updateContents)
		    self.updateContents = None
		    writestream.close()
		    log.debug('Update file written successfully.')
		except:
		    self.err = 'Could not write to version definitions file.'
		    log.error(self.err)
		    self.transferDone.emit(False)

		self.parseDefinitionsFile() # inefficient but OK
		self.guiCallback(True)
	    else:
		self.err = 'Retrieved update is empty.\nMost probably update server is broken. If you use proxy, make sure that it works fine.'
		log.error(self.err)
		self.transferDone.emit(False)
	else:
	    self.err = "Could not reach version definitions URL. Check your internet connection."
	    log.error(self.err)
	    self.guiCallback(False)

    def getBySize(self, size):
        'Size in bytes.'
        for version in self.versions:
            if long(version.size) == long(size):
                return version
        return None

    def getByDistance(self, name, tolerance = 10):
        """Returns version if there is a version within Levenshtein distance of
        'tolerance' parameter for 'name' parameter. Nearest version is returned.
        Comparison is done case-insensitively. First appearing in versions.xml
        is chosen on tie. None is returned if no version is in given distance.
        """
        nearest = None
        minDistance = 999

        for version in self.versions:
            n1 = version.name.lower()
            n2 = name.lower()
            l_distance = levenshtein(n1, n2)

            if l_distance < tolerance and l_distance < minDistance:
                minDistance = l_distance
                nearest = version
        return nearest

    def getByMD5Sum(self, hash):
        'MD5 hash as in versions.xml'
        for version in self.versions:
            if str(version.md5sum) == str(hash):
                return version
        return None

    def connectGui(self, guiCallback):
	self.guiCallback = guiCallback

    def __repr__(self):
	r = ''
	for v in self.versions:
	    r+= ' '.join((v.name, v.size, v.id, '\n'))
	    for m in v.mirrors:
		r+= ' '.join(('  ', m.hostname, m.country, m.port, m.username, m.password, m.path, '\n'))

	return r