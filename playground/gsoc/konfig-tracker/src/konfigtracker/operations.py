# -*- coding: utf-8 -*-
from PyKDE4.kdecore import KStandardDirs
from PyQt4.QtCore import QString, QDir

from time import strftime, localtime, asctime
import distutils.dir_util as DirUtil
import git
import os

# Path to konfig-tracker db
db_path = str(KStandardDirs().localkdedir() + "konfigtracker-db")

# Source path of configuration files
source_path = str(KStandardDirs().localkdedir() + "share/config")
restore_path = str(KStandardDirs().localkdedir() + "share/config")


def createDatabase(path):
	"""
	Initialize a git repository in path.
	"""
	gitRepo = git.Git(path)
	gitRepo.init()

def gitCommit():
	backupTime = strftime("%d %b %Y %H:%M:%S, %a", localtime())
	repo = git.Git(db_path)
        message = "Configuration Backup on : " + backupTime
	try:
		repo.execute(["git","commit","-a","-m",message])
	except git.errors.GitCommandError:
		pass

def addToDatabase():
	"""
        Add blobs into the repository
        """
        repo = git.Git(db_path)
        repo.execute(["git","add","."])
        gitCommit()

def performBackup():
        """
	This will perform the initial import of config files from
	.kde4/share/config to .kde4/konfigtracker-repo.
	"""
	dest_path = str(db_path + "/config")

	if DirUtil.copy_tree(source_path,dest_path,update=1):
		addToDatabase()

def restore(commitId):
	"""
	Restore the config files to a particular commit
	"""
	#check whether this commitId is at the head now. If yes, don't perform the restore.
	repo = git.Git(db_path)
	srcPath = "/tmp/config"
	if QDir().exists(QString(srcPath)):
		DirUtil.remove_tree(srcPath,1)
	repo.execute(["git","read-tree", commitId])
	repo.execute(["git","checkout-index","-a","--prefix=/tmp/"])
	if DirUtil.copy_tree(srcPath, restore_path, update=1):
		addToDatabase()

def exportDatabase(commitId, savePath):
	"""
	Pack the data at this commit into an archive
	"""
        repo = git.Git(db_path)
        repo.execute(["git", "archive", commitId, "-o", str(savePath)])
                

def getCommitMap():
	"""
	Get the list of commits from database, form a dictionary of commitid
        and committed_date
	"""
	repo = git.Repo(db_path)
	commit_list = repo.commits('master',max_count=100)
	return dict([(c.message,c.id) for c in commit_list])

def getCommitLog(commit):
	"""
	Return the commit log as a QString
	"""
	repo = git.Git(db_path)
	commitLog = repo.execute(["git","show",commit])
	return QString(commitLog)

def getPathMap(commitId):
	repo = git.Repo(db_path)
	commit = repo.commit(commitId)
	diff = repo.commit_diff(commit)
	return dict([(d.b_path,d) for d in diff])
