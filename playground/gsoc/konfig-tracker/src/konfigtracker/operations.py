#-----------------------------------------------------------
# Operations.py
# Author : Jain Basil Aliyas
# Date : 8 June, 2010
#-----------------------------------------------------------

from PyKDE4.kdecore import KStandardDirs

from time import strftime,localtime
import distutils.dir_util as DirUtil
import git,os

def GetLocalDir():
	"""
	return the local kde directory here. ie. $HOME/$KDEDIR
	"""
	return KStandardDirs().localkdedir()


def CreateDB(path):
	"""
	Initialize a git repository in path.
	"""
	gitRepo = git.Git(path)
	gitRepo.init()


def Commit():
	backupTime = strftime("%a, %d %b %Y %H:%M:%S", localtime())
	repo = git.Git(GetLocalDir() + "/KonfigTrackerDB/")
	message = "Backup on "+ backupTime
	try:
		repo.execute(["git","commit","-a","-m",message])
	except git.errors.GitCommandError:
		pass
	print message

def AddToDB():
	"""
        Add blobs into the repository
        """
        repo = git.Git( GetLocalDir()+ "/KonfigTrackerDB/")
        repo.execute(["git","add","."])
        Commit()

def Backup():
        """
	This will perform the initial import of config files from
	.kde4/share/config to .kde4/konfigtracker-repo.
	"""
	srcPath = str(GetLocalDir() + "/share/config")
	destPath = str(GetLocalDir() + "/KonfigTrackerDB/config")

	if DirUtil.copy_tree(srcPath,destPath,update=1):
		AddToDB()

