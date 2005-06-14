# -*- coding: utf-8 -*-
# unpack magic
# maintainer baris and meren

#standart lisbrary modules
import os
import sys
import tarfile
import zipfile

#pisi modules
import config

class ArchiveBase(object):
    def __init__(self, fileName, type):
	self.type = type
	self.fileName = fileName

	self.filePath = config.archives_dir() + '/' + self.fileName

class ArchiveTarFile(ArchiveBase):
    def __init__(self, fileName, type):
	super(ArchiveTarFile, self).__init__(fileName, type)

    def unpack(self):
	if self.type == 'targz':
	    tar = tarfile.open(self.filePath, 'r:gz')
	    for tarinfo in tar:
		tar.extract(tarinfo)
	    tar.close()

class ArchiveZip(ArchiveBase):
    def __init__(self, fileName, type):
	super(ArchiveZip, self).__init__(fileName, type)

    def unpack(self):
        zip = zipfile.ZipFile(self.filePath, 'r')
        fileNames = zip.namelist()
        for file in fileNames:
            ofile = config.archives_dir() + '/' + file
            if not os.path.exists(os.path.dirname(config.archives_dir() + '/' + file)):
                os.mkdir(os.path.dirname(config.archives_dir() + '/' + file))
                continue
	    else: # directory is present, we should still continue (or delete?)
		continue
            buff = open (ofile, 'wb')
            fileContent = zip.read(file)
            buff.write(fileContent)
            buff.close()
        zip.close()
                
class Archive:
    """Unpack magic for Archive files..."""

    def __init__(self, type, fileName):
	"""accepted archive types:
	targz, tarbz2, zip, tar"""	
	
	actions = {
	    'targz': ArchiveTarFile,
	    'tarbz2': ArchiveTarFile,
	    'tar': ArchiveTarFile,
	    'zip': ArchiveZip
	    }
	
	self.archive = actions.get(type)(fileName, type)

    def unpack(self):
	self.archive.unpack()
