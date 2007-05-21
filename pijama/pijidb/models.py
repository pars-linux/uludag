from django.db import models

# Create your models here.

VERSION_CHOICES=(
	('<', 'smaller than'),
	('>', 'bigger than'),
	('=', 'equal'),
	('', ''),	  
)

repopath="/home/oguz"#repositories path to define the FilePathField

#table descriptions for Pardus-2007 repo

class RepoPackages(models.Model):
	pkgname=models.CharField(maxlength=50)
	reponame=models.CharField(maxlength=50)
	isa=models.CharField(maxlength=100, null=True)
	partof=models.CharField(maxlength=200, null=True)
	
	def __str__(self):
        	return self.pkgname
	
class BuildDeps(models.Model):
	pkgname=models.ForeignKey(RepoPackages)
	name=models.CharField(maxlength=100, null=True)
	version=models.CharField(maxlength=10, null=True)
	sign=models.CharField(maxlength=2, choices=VERSION_CHOICES)
	
	def __str__(self):
		return self.name
	
class Packager(models.Model):
	pkgname=models.ForeignKey(RepoPackages)
	name=models.CharField(maxlength=100)
	email=models.EmailField()
	
	def __str__(self):
		return self.name
		
class Screenshot(models.Model):
	pkgname=models.ForeignKey(RepoPackages)
	filename=models.FilePathField(path=repopath, match="^[a-z]+\.[jpg|JPG|jpeg|png]$", recursive=True)
	#ftype=model.CharField(maxlength=10) maybe
	
	def __str__(self):
		return self.filename
	
class Patch(models.Model):
	pkgname=models.ForeignKey(RepoPackages)
	name=models.CharField(maxlength=50)
	compressiontype=models.CharField(maxlength=10, null=True)
	level=models.IntegerField(null=True)
	
	def __str__(self):
		return self.name
	
class BinaryPacks(models.Model):
	pkgname=models.ForeignKey(RepoPackages)
	name=models.CharField(maxlength=50)
		
	def __str__(self):
		return self.name
	
class Conflicts(models.Model):
	pkgname=models.ForeignKey(RepoPackages)
	name=models.CharField(maxlength=50)
	version=models.CharField(maxlength=10, null=True)
	sign=models.CharField(maxlength=2, choices=VERSION_CHOICES)
	
	def __str__(self):
		return self.name
	
class RunTimeDeps(models.Model):
	pkgname=models.ForeignKey(RepoPackages)
	name=models.CharField(maxlength=50)
	version=models.CharField(maxlength=10, null=True)
	sign=models.CharField(maxlength=2, choices=VERSION_CHOICES)
	
	def __str__(self):
		return self.name
	
class History(models.Model):#two entrief for each package, one for first relase the other one is the last update
	pkgname=models.ForeignKey(RepoPackages)
	updatetype=models.CharField(maxlength=20, default="normal")
	date=models.DateField()
	
	def __str__(self):
		return self.date
	
class DepoUpdate(models.Model):
	updatedate=models.DateField(unique=True, null=True)# to detect the new packages
	editdate=models.DateField(unique=True, null=True)#to detect the reviews, history updates
	
	def __str__(self):
		return self.updatedate
	
	
	