# -*- coding: utf-8 -*-
from pstemplates import *
from os.path import isfile
import polib

REPO_PATH = '../../../'
REAL_PATH = 'http://svn.pardus.org.tr/uludag/trunk/'

po_files = {}

for lang in ["tr", "nl", "de", "es", "pt_BR", "it","fr","ca", "pl"]:
	po_files[lang] = {"Package Descriptions": REPO_PATH + "repository-scripts/pspec-translations/%s.po" % lang,
		"Network Manager": REPO_PATH + "tasma/network-manager/po/%s.po" % lang,
		"Package Manager": REPO_PATH + "tasma/package-manager/po/%s.po" % lang,
		"Disk Manager": REPO_PATH + "tasma/disk-manager/po/%s.po" % lang,
		"Feedback": REPO_PATH + "feedback/po/%s.po" % lang,
		"Firewall Configurator": REPO_PATH + "tasma/firewall-config/po/%s.po" % lang,
		"Tasma": REPO_PATH + "tasma/tasma/po/%s.po" % lang,
		"Service Manager": REPO_PATH + "tasma/service-manager/po/%s.po" % lang,
		"User Manager": REPO_PATH + "tasma/user-manager/po/%s.po" % lang,
		"PiSi": REPO_PATH + "pisi/po/%s.po" % lang,
		"ÇOMAR": REPO_PATH + "comar/comar/po/%s.po" % lang,
		"Müdür": REPO_PATH + "comar/mudur/po/%s.po" % lang,
		"Sysinfo": REPO_PATH + "sysinfo/po/%s/kio_sysinfo.po" % lang,
		"YALI": REPO_PATH + "yali/po/%s.po" % lang,
		"Kaptan": REPO_PATH + "kaptan/po/%s.po" % lang,
		"PLSA": REPO_PATH + "plsa/po/%s.po" % lang,
		"Knazar": REPO_PATH + "knazar/po/%s.po" % lang,
		"Repokit": REPO_PATH + "repokit/po/%s.po" % lang,
		"Pardusman": REPO_PATH + "pardusman/po/%s.po" % lang,
		"Boot Manager": REPO_PATH + "tasma/boot-manager/po/%s.po" % lang,}

for langs in po_files:
	ret = htmlHeaderTemplate['en']
	for tra in po_files[langs]:
		if isfile(po_files[langs][tra]):
			po = polib.pofile(po_files[langs][tra])
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
			ret = ret + table(path=path, name=tra, all='-', translated='-', fuzzy='-', untranslated='-', percent='0%', percent_fuzzy='0', percent_untrans='100')
	ret = ret + htmlFooterTemplate["en"]
	file = open(REPO_PATH + 'web/miss/eng/projects/translation/stats/stats-' + langs + '.html', 'w')
	file.write(ret)
	file.close()


#print htmlHeaderTemplate

