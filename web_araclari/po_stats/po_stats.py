# -*- coding: utf-8 -*-
from pstemplates import *
from os.path import isfile
from urlparse import urlparse
import polib

REPO_PATH = '../../'
REAL_PATH = 'http://svn.pardus.org.tr/uludag/trunk/'

po_files = {}

for lang in ["tr", "nl", "de", "es", "pt_BR", "it","fr","ca", "pl"]:
	po_files[lang] = {"Package Descriptions": REAL_PATH + "repository-scripts/pspec-translations/%s.po" % lang,
		"Network Manager": REAL_PATH + "tasma/network-manager/po/%s.po" % lang,
		"Package Manager": REAL_PATH + "tasma/package-manager/po/%s.po" % lang,
		"Disk Manager": REAL_PATH + "tasma/disk-manager/po/%s.po" % lang,
		"Feedback": REAL_PATH + "feedback/po/%s.po" % lang,
		"Firewall Configurator": REAL_PATH + "tasma/firewall-config/po/%s.po" % lang,
		"Tasma": REAL_PATH + "tasma/tasma/po/%s.po" % lang,
		"Service Manager": REAL_PATH + "tasma/service-manager/po/%s.po" % lang,
		"User Manager": REAL_PATH + "tasma/user-manager/po/%s.po" % lang,
		"PiSi": REAL_PATH + "pisi/po/%s.po" % lang,
		"ÇOMAR": REAL_PATH + "comar/comar/po/%s.po" % lang,
		"Müdür": REAL_PATH + "comar/mudur/po/%s.po" % lang,
		"Sysinfo": REAL_PATH + "sysinfo/po/%s/kio_sysinfo.po" % lang,
		"YALI": REAL_PATH + "yali/po/%s.po" % lang,
		"Kaptan": REAL_PATH + "kaptan/po/%s.po" % lang,
		"PLSA": REAL_PATH + "plsa/po/%s.po" % lang,
		"Knazar": REAL_PATH + "knazar/po/%s.po" % lang,
		"Repokit": REAL_PATH + "repokit/po/%s.po" % lang,
		"Pardusman": REAL_PATH + "pardusman/po/%s.po" % lang,
		"Boot Manager": REAL_PATH + "tasma/boot-manager/po/%s.po" % lang,}

def getFileHandle(fpath):
    if urlparse(fpath)[0] == "http" or urlparse(fpath)[0] == "https":
        from urllib2 import urlopen
        try:
            fhandle = urlopen(fpath)
        except:
            return None
    if urlparse(fpath)[0] == "" and isfile(fpath):
        try:
            fhandle = open(fpath)
        except IOError:
            return None
    return fhandle

for langs in po_files:
	ret = htmlHeaderTemplate['en'] % langs
	for tra in po_files[langs]:
		fhandle = getFileHandle(po_files[langs][tra])
		if fhandle:
			po = polib.pofile(fhandle)
			percent = po.percent_translated()
			translated = len(po.translated_entries())
			untranslated = len(po.untranslated_entries())
			fuzzy = len(po.fuzzy_entries())
			all = translated+untranslated+fuzzy
			percent_fuzzy= (fuzzy*100)/all
			percent_untrans= (untranslated*100)/all
			path = po_files[langs][tra].replace(REPO_PATH, REAL_PATH)
			ret = ret + table(path=path, name=tra, all=str(all), translated=str(translated), fuzzy=str(fuzzy), untranslated=str(untranslated), percent=str(percent)+'%', percent_fuzzy=str(percent_fuzzy), percent_untrans=str(percent_untrans))
		else:
			path = po_files[langs][tra].replace(langs + '.po', '').replace(REPO_PATH, REAL_PATH)
			ret = ret + table(path=path, name=tra, all='no translation', translated='-', fuzzy='-', untranslated='-', percent='0%', percent_fuzzy='0', percent_untrans='100')
	ret = ret + htmlFooterTemplate["en"]
	file = open(REPO_PATH + 'web/miss/eng/projects/translation/stats/stats-' + langs + '.html', 'w')
	file.write(ret)
	file.close()

