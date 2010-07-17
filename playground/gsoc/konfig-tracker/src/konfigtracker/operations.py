# -*- coding: utf-8 -*-
from PyKDE4.kdecore import KStandardDirs

from time import strftime,localtime
import distutils.dir_util as DirUtil
import git,os

#Path to konfig-tracker db
db_path = str(KStandardDirs().localkdedir() + "KonfigTracker")

#Source path of configuration files
source_path = str(KStandardDirs().localkdedir() + "share/config")
restore_path = str(KStandardDirs().localkdedir() + "share")

def createDatabase(path):
	"""
	Initialize a git repository in path.
	"""
	gitRepo = git.Git(path)
	gitRepo.init()

def gitCommit():
	backupTime = strftime("%a, %d %b %Y %H:%M:%S", localtime())
	repo = git.Git(db_path)
	message = "Backup on "+ backupTime
	try:
		repo.execute(["git","commit","-a","-m",message])
		print message
	except git.errors.GitCommandError:
		pass

def addToDatabase():
	"""
        Add blobs into the repository
        """
        repo = git.Git(db_path)
        repo.execute(["git","add","."])
        git_commit()

def performBackup():
        """
	This will perform the initial import of config files from
	.kde4/share/config to .kde4/konfigtracker-repo.
	"""
	srcPath = str(source_path)
	destPath = str(db_path + "/config")

	if DirUtil.copy_tree(srcPath,destPath,update=1):
		addToDatabase()

def restore(commitId):
	"""
	Restore the config files to a particular commit
	"""
	#check whether this commitId is at the head now. If yes, don't perform the restore.
	repo = git.Git(db_path)
	repo.execute(["git","read-tree", commitId])
	repo.execute(["git","checkout-index","-a","--prefix=/tmp/"])
	srcPath = "/tmp/config"
	DirUtil.copy_tree(srcPath, restore_path, update=1)

def restoreParent(commitId):
	"""
	Restore to parent of a commit passed
	"""
	repo = git.Git(db_path)
	parent = repo.commits(commitId).parents
	repo.execute(["git","read-tree",parent])
	repo.execute(["git","checkout-index","-a","--prefix=/tmp/"])
	srcPath = "/tmp/config"
	DirUtil.copy_tree(srcPath, restore_path, update=1)

def archiveDatabase(commitId):
	"""
	Pack the data at this commit into an archive
	"""
	pass

def slotCommitList():
	"""
	Slot which will return a list of commits. This will be used to update the ui
	"""
	repo = git.Repo(db_path)
	commit_list = repo.commits()
	print commit_list[0].id
