#!/usr/bin/python
# -*- coding: utf-8 -*-

from mechanize import Browser
from mechanize import DefaultFactory
from mechanize import LWPCookieJar

from bugspy.constants import Constants

# Test bug number
bugzillaUrl = "http://bugs.pardus.org.tr/show_bug.cgi?id=15012"
username = "svnbot@pardus.org.tr"
password = "svnbot_parolasi_sunucu_yoneticisinden_iste"
bug_id = "15012"
comment = u'author: fatih.arslan (fatih arslan)\nrepository: pardus\ncommit: 125476\n\nchanged files:\nu   playground/fatih.arslan/bugcomment_script\n\ncommit message:\nbug:comment:15012\n\nsee the changes at:\n  http://websvn.pardus.org.tr/pardus?view=revision&revision=125476\n'

constants = Constants(bugzillaUrl)

browser = Browser(factory=DefaultFactory(i_want_broken_xhtml_support=True))

#browser.addheaders = [("User-Agent", constants.USER_AGENT)]
browser.addheaders = [("User-Agent", "Mozilla/5.0 (X11; Linux i686; rv:6.0) Gecko/20100101 Firefox/6.0")]
browser.set_handle_robots(False)
cookiejar = LWPCookieJar(constants.COOKIE_FILE)
browser.set_cookiejar(cookiejar)

### Login
browser.open(bugzillaUrl)

print "## Open website"
print "## Show forms"
print ""
for f in browser.forms():
    print f

browser.select_form(nr=1)
browser["Bugzilla_login"] = username
browser["Bugzilla_password"] = password
response = browser.submit()
response = response.read()

print "## Login to website"
print "## Show forms"
print ""

for f in browser.forms():
    print f

browser.select_form(nr=1)
browser["comment"] = comment
response = browser.submit()
response = response.read()


#bug_data = browser.open(constants.get_bug_url(bug_id, True)).read()

