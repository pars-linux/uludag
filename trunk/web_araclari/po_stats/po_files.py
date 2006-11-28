# -*- coding: utf-8 -*-

po_files = {}

for lang in ["tr", "nl", "de", "es"]:
    po_files[lang] = {"Package Descriptions": "http://svn.pardus.org.tr/uludag/trunk/repository-scripts/pspec-translations/%s.po" % lang,
                      "Network Manager": "http://svn.pardus.org.tr/uludag/trunk/tasma/network-manager/po/%s.po" % lang,
                      "Package Manager": "http://svn.pardus.org.tr/uludag/trunk/tasma/package-manager/po/%s.po" % lang,
                      "Feedback": "http://svn.pardus.org.tr/uludag/trunk/feedback/po/%s.po" % lang,
                      "Firewall Configurator": "http://svn.pardus.org.tr/uludag/trunk/tasma/firewall-config/po/%s.po" % lang,
                      "Tasma": "http://svn.pardus.org.tr/uludag/trunk/tasma/tasma/po/%s.po" % lang,
                      "Service Manager": "http://svn.pardus.org.tr/uludag/trunk/tasma/service-manager/po/%s.po" % lang,
                      "User Manager": "http://svn.pardus.org.tr/uludag/trunk/tasma/user-manager/po/%s.po" % lang,
                      "PiSi": "http://svn.pardus.org.tr/uludag/trunk/pisi/po/%s.po" % lang,
                      "ÇOMAR": "http://svn.pardus.org.tr/uludag/trunk/comar/comar/po/%s.po" % lang,
                      "Müdür": "http://svn.pardus.org.tr/uludag/trunk/comar/mudur/po/%s.po" % lang,
                      "Sysinfo": "http://svn.pardus.org.tr/uludag/trunk/sysinfo/po/%s/kio_sysinfo.po" % lang,
                      "YALI": "http://svn.pardus.org.tr/uludag/trunk/yali/po/%s.po" % lang,
                      "Kaptan": "http://svn.pardus.org.tr/uludag/trunk/kaptan/po/%s.po" % lang}
