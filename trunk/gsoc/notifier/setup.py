#!/usr/bin/env python

# I stole [ :) ] and modified this file from Gokmen Goksel's yali4 package :)

import os
import re
import glob
import shutil
from PyQt4 import pyqtconfig
from distutils.core import setup
from distutils.sysconfig import get_python_lib
from distutils.cmd import Command
from distutils.command.build import build
from distutils.command.clean import clean
from distutils.command.install import install
from distutils.spawn import find_executable, spawn

import pnm

PNM_VERSION = pnm.__version__

def qt_ui_files():
	p = "pnm/ui/*.ui"
	return glob.glob(p)

def icon_files():
	p = "icons/*.*"
	return glob.glob(p)

def getRevision():
	try:
		p = os.popen("svn info 2> /dev/null")
		for line in p.readlines():
			line = line.strip()
			if line.startswith("Revision:"):
				return line.split(":")[1].strip()
	except:
		return ""

def getVersion():
	return PNM_VERSION

def py_file_name(ui_file):
	return os.path.splitext(ui_file)[0] + '.py'

##
# build command
class PNMBuild(build):
	def add_gettext_support(self, ui_file):
		# hacky, too hacky. but works...
		py_file = py_file_name(ui_file)
		# lines in reverse order
		lines =  ["\n_ = gettext.translation(\"notman\", fallback = True).ugettext", "\nimport gettext"]
		f = open(py_file, "r").readlines()
		for l in lines:
			f.insert(1, l)
		x = open(py_file, "w")
		keyStart = "QtGui.QApplication.translate"
		keyEnd = ", None, QtGui.QApplication.UnicodeUTF8)"
		styleKey = "setStyleSheet"
		for l in f:
			if not l.find(keyStart)==-1 and l.find(styleKey)==-1:
				z = "%s(_(" % l.split("(")[0]
				y = l.split(",")[0]+', '
				l = l.replace(y,z)
			l = l.replace(keyEnd,")")
			x.write(l)

	def compile_ui(self, ui_file):
		pyqt_configuration = pyqtconfig.Configuration()
		pyuic_exe = find_executable('pyuic4', pyqt_configuration.default_bin_dir)
		if not pyuic_exe:
			# Search on the $Path.
			pyuic_exe = find_executable('pyuic4')
		cmd = [pyuic_exe, ui_file, '-o']
		cmd.append(py_file_name(ui_file))
		os.system(' '.join(cmd))

	def run(self):
		for f in qt_ui_files():
			self.compile_ui(f)
			self.add_gettext_support(f)
		build.run(self)

##
# clean command
class PNMClean(clean):
	def run(self):
		clean.run(self)
		# clean ui generated .py files
		for f in qt_ui_files():
			f = py_file_name(f)
			if os.path.exists(f):
				os.unlink(f)

##
# uninstall command
class PNMUninstall(Command):
	user_options = []

	def initialize_options(self):
		pass

	def finalize_options(self):
		pass

	def run(self):
		pnm_dir = os.path.join(get_python_lib(), "pnm")
		if os.path.exists(pnm_dir):
			print "removing: ", pnm_dir
			shutil.rmtree(pnm_dir)

		data_dir = "/usr/share/pnm"
		if os.path.exists(data_dir):
			print "removing: ", data_dir
			shutil.rmtree(data_dir)
			
		# Uninstall the .service file:
		os.unlink("/usr/share/dbus-1/services/org.pardus.notificationmanager.service")

i18n_domain = "notman"
i18n_languages = ["tr"]

##
# install command
class I18nInstall(install):
	def run(self):
		install.run(self)
		for lang in i18n_languages:
			print "Installing '%s' translations..." % lang
			os.popen("msgfmt i18n/%s.po -o i18n/%s.mo" % (lang, lang))
			if not self.root:
				self.root = "/"
				destpath = os.path.join(self.root, "usr/share/locale/%s/LC_MESSAGES" % lang)
			try:
				os.makedirs(destpath)
			except:
				pass
			shutil.copy("i18n/%s.mo" % lang, os.path.join(destpath, "%s.mo" % i18n_domain))
			
		# Install the .service file to dbus service file directory:
		f = file("auxfiles/org.pardus.notificationmanager.service", "rw+")
		l = f.readlines()
		l[2] = "Exec=/usr/bin/env python " + os.path.join(get_python_lib(), "pnm") + "/notman.py\n"
		f.truncate(0)
		f.seek(0)
		f.writelines(l)
		f.close()
		shutil.copy("auxfiles/org.pardus.notificationmanager.service", os.path.join(self.root, "usr/share/dbus-1/services"))

setup(	name = "pnm",
		version = getVersion(),
		description = "PNM (Pardus Notification Manager)",
		long_description = "Notification manager that will be used (hopefully) by Pardus tools",
		license = "GNU GPL2",
		author = "Mehmet Ozan Kabak (developed as a GSoC 2008 project)",
		author_email = "wanderer2@gmail.com",
		url = "www.pardus.org.tr",
		packages = ["pnm", "pnm.ui"],
		# Install the icons, the XSD file and the sample configuration file.
		data_files = [("/usr/share/pnm/icons", icon_files()), ("/usr/share/pnm", ["auxfiles/pnm.xsd", "auxfiles/sampleconfig.xml"]) ],
		
		cmdclass = {
			'build' : PNMBuild,
			'clean' : PNMClean,
			'install': I18nInstall,
			'uninstall': PNMUninstall
        }
	)
