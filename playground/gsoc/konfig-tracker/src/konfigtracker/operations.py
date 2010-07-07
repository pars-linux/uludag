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
		print message
	except git.errors.GitCommandError:
		pass

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

def restore(commitId):
	"""
	Restore the config files to a particular commit
	"""
	#check whether this commitId is at the head now. If yes, don't perform the restore.
	repo = git.Git(GetLocalDir() + "/KonfigTrackerDB/")
	repo.execute(["git","read-tree",commitId])
	repo.execute(["git","checkout-index","-a","--prefix=/tmp/"])
	destPath = str(GetLocalDir() + "/share")
	srcPath = "/tmp/config"
	DirUtil.copy_tree(srcPath,destPath,update=1)

def restoreParent(commitId):
	"""
	Restore to parent of a commit passed
	"""
	repo = git.Git(GetLocalDir() + "/KonfigTrackerDB/")
	parent=repo.commits(commitId).parents
	repo.execute(["git","read-tree",parent])
	repo.execute(["git","checkout-index","-a","--prefix=/tmp/"])
	destPath = str(GetLocalDir() + "/share")
	srcPath = "/tmp/config"
	DirUtil.copy_tree(srcPath,destPath,update=1)

def packData(commitId):
	"""
	Pack the data at this commit into an archive
	"""
	pass	
