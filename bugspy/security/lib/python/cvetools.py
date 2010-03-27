# Copyright 1999-2008 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

import os
import re
import assign

class CVEData:
    CVEID_RE = re.compile("(CVE-\d+-\d+)")
    """This class handles the CVE database"""
    def __init__(self):
        self.create_cvedata()

    def create_cvedata(self):
        import datetime
        import cPickle
        files = []
        year = datetime.date.today().year

        # read all nvdcve-200*.xml files
        for yr in range(2002, year+1):
            files.append("./cache/nvdcve-%s.xml" % (yr))
        files.append("./cache/nvdcve-modified.xml")

        if os.path.exists("./cache/cvedata.pickle"):
            ptime = os.path.getmtime("./cache/cvedata.pickle")
            newer_files = [xml for xml in files if os.path.getmtime(xml) > ptime]
            if len(newer_files) == 0:
                try:
                    pickle = open("./cache/cvedata.pickle")
                    self.cvedata = cPickle.load(pickle)
                    return
                except Exception, e:
                    print "Error opening Hash-cache, recreating: %s" % (e)

        import nvd
        self.cvedata = nvd.parseAll(files)
        pickle = open("./cache/cvedata.pickle", "w")
        cPickle.dump(self.cvedata, pickle, protocol=-1)


    def get_cve_from(self, entry):
        """ returns the CVE-YYYY-IIII name for an entry or None. """
        if len(entry) == 0:
            return None
        match = CVEData.CVEID_RE.match(entry[0])

        print "looking: %s" % entry[0]

        if not match:
            print "not matched!"
            return None

        cve = match.group(1)
        print "matched cve: %s" % cve
        if not cve in self.cvedata:
            return None

        return cve

    def get_refs_for(self, cve):
        return self.cvedata[cve]['refs']
    
    def guess_name_for(self, cve):
        try:
            refs = self.cvedata[cve]['refs']
        except KeyError:
            return {}
        SAs = []
        names = {}
        for source, url in refs:
            if source == u"SECUNIA" or url.startswith("http://secunia.com/advisories/") or url.startswith("http://www.secunia.com/advisories/"):
                SAs.append(re.sub(r".*advisories/(\d+)", r"\1", url))

        import urllib2
        for SAid in SAs:
            html = urllib2.urlopen("http://secunia.com/advisories/%s/2/" % SAid).read()
            match = re.findall(r'<b>Provided and/or discovered by</b>:(.+?)<b>', html, flags = re.S)
            if match:
                text = re.sub('<.*?>', '', match[0])
                names[SAid] = [re.sub(r'(in|via) a .* bug report', '', re.sub(r'^[\d,) -]*(.* credits|Reported by)?', '', line)).strip(' \r\n.') for line in text.split('\n')]

        return names


    def print_all_about(self, entry):
        """ Prints all info about a list entry.
            Returns the product name if possible or None. """

        cve = self.get_cve_from(entry)
        if not cve:
            print "CVE name not found in CVE database: %s" % (entry)
            return None

        self.print_cveinfo(cve)

        query = ""
        if self.cvedata[cve]['product_vendor']:
            print "Vendor: %s" % (self.cvedata[cve]['product_vendor'])
            query = "%s" % (self.cvedata[cve]['product_vendor'])
        if (self.cvedata[cve]['product_name']):
            productname = self.cvedata[cve]['product_name']
            print "Product: %s" % (productname)
            if productname.lower().find(query.lower()) > -1:
                # productname already contains vendor (or vendor is empty)
                query = "%s" % (productname)
            else:
                query += " %s" % (productname)
        if not query:
            query = self.guess_product(self.cvedata[cve]['desc'])
            if query:
                print "Product (guessed): %s" % (query)
            else:
                print "Product name unknown."

        return (cve, query)


    def print_cveinfo(self, cvename):
        """ Print all info we have about a given CVE id """
        cveinfo = self.cvedata[cvename]

        os.spawnlp(os.P_WAIT, 'clear', 'clear')
        print "="*80
        print "Name:      %s" % (cvename)
        print "URL:       http://cve.mitre.org/cgi-bin/cvename.cgi?name=%s" % (cvename)
        print "Published: %s" % (cveinfo['published'])
        print "Severity:  %s" % (cveinfo['severity'])
        print "Description: \n"
        print self.get_cve_desc(cvename)
        print


    def get_cve_desc(self, cvename, indentation = 0, linelength = 72):
        """ returns the cve description, wrapped to specified line length and given space indentation"""
        cveinfo = self.cvedata[cvename]

        linelength = linelength - indentation
        spaces = "".join(" " for x in range(0, indentation))
        text = ""
        start = 0
        end = 0
        leng = len(cveinfo['desc'])
        while leng - start > linelength:
            end = cveinfo['desc'].rfind(' ', start, min(start + linelength, leng))
            if end == -1:
                # in case we do not find a space, use up as much as we can
                end = start + linelength - 1
            text += spaces + cveinfo['desc'][start:end] + "\n"
            start = end + 1
        text += spaces + cveinfo['desc'][start:]
        return text



    def guess_product(self, desc):
        """ Guess a product name from a description. Returns a string or None. """
        # ... in vulnfile.c in (the) VulApp Application 1.0
        matcher = re.compile(" in (\S+\.\S+) in (?:the )?(?:a )?(\D+) \d+")
        match = matcher.search(desc)
        if match:
            if match.group(2)[-6:] == "before":
                return match.group(2)[:-7]
            else:
                return match.group(2)

        # ... in (the) VulnApp Application 1.0
        matcher = re.compile(" in (?:the )?(?:a )?(\D+) \d+")
        match = matcher.search(desc)
        if match:
            if match.group(1)[-6:] == "before":
                return match.group(1)[:-7]
            else:
                return match.group(1)

        matcher = re.compile(" in (\S+\.\S+) in (?:the )?(?:a )?(\S+) ")
        match = matcher.search(desc)
        if match:
            return match.group(2)

        # ... in (the) VulnApp
        matcher = re.compile(" in (?:the )?(?:a )?(\S+) ")
        match = matcher.search(desc)
        if match:
            return match.group(1)

        # (The) VulnApp
        matcher = re.compile("(?:The )?(\S+) ")
        match = matcher.search(desc)
        if match:
            return match.group(1)

        return None

class BugReporter:
    CVEGROUPALL = re.compile(r'[ (]*CVE-(\d{4})([-,(){}|, \d]+)')
    CVEGROUPSPLIT = re.compile(r'(?<=\D)(\d{4})(?=\D|$)')
    def __init__(self, username = None, password = None):
        postconfig = {
            'product': 'Gentoo Security',
            'version': 'unspecified',
            'rep_platform': 'All',
            'op_sys': 'Linux',
            'priority': 'P2',
            'bug_severity': 'normal',
            'bug_status': 'NEW',
            'assigned_to': '',
            'keywords': '',
            'dependson':'',
            'blocked':'',
            'component': 'Vulnerabilities',
            # needs to be filled in
            'bug_file_loc': '',
            'short_desc': '',
            'comment': '',
            }
        
        try:
            import bugz.bugzilla
            bugz.bugzilla.config.params['post'] = postconfig
            Bugz = bugz.bugzilla.Bugz
        except:
            try:
                import bugz
            except:
                return
            bugz.config.params['post'] = postconfig
            Bugz = bugz.Bugz

        self.bugz_auth = Bugz(base = "https://bugs.gentoo.org",
            user = username,
            password = password,
            forget = False)

    def post_bug(self, title, description, component="", whiteboard="", url=""):
        """ Posts a security bug, returning the Bug number or 0 """
        bugno = 0
        ccs = assign.get_cc_from_string(title)
        ccs = ",".join(ccs)
        
        severity = 'normal'
        try:
            try:
                bugno = self.bugz_auth.post(title = title, description = description, cc = ccs, url = url)
                print "Ignoring Bug component, please upgrade pybugz."
            except TypeError:
                # pybugz since 0.7.4 requires to specify product and component
                bugno = self.bugz_auth.post(title = title, product="Gentoo Security", component=component, description = description, cc = ccs, url = url)
        except Exception, e:
            print "An error occurred posting a bug: %s" % (e)

        if bugno and whiteboard:
            severity = self.severity_from_whiteboard(whiteboard)
            self.bugz_auth.modify(bugid = bugno, whiteboard = whiteboard, severity = severity)
        return bugno

    def modify_bug(self, bugid, title, comment):
        """ Modifies bug and adds comment """
        try:
            bugno = self.bugz_auth.modify(bugid, comment = comment, title = title)
        except Exception, e:
            print "An error occurred modifying a bug: %s" % (e)

    def get_bug_title(self, bugno):
        """ Get the title of a bug number """
        try:
            return self.bugz_auth.get(bugno).find('//short_desc').text
        except Exception, e:
            pass
        return None

    def get_bug_cves(self, bugno, title = ""):
        """ Get a list of CVEs on a bug number """
        bug_cves = []
        try:
            title = title or self.get_bug_title(bugno)
            if not title:
                return bug_cves
            for (year, split_cves) in BugReporter.CVEGROUPALL.findall(title):
                for cve in BugReporter.CVEGROUPSPLIT.findall(split_cves):
                    bug_cves.append('CVE-%s-%s' % (year, cve))
        except Exception, e:
            pass
        return bug_cves

    def severity_from_whiteboard(self, whiteboard):
        if (len(whiteboard)) < 2:
            return 'normal'
        evaluation = whiteboard[0:2]
        if evaluation in ['A0', 'B0']:
            return 'blocker'
        if evaluation in ['A1', 'C0']:
            return 'critical'
        if evaluation in ['A2', 'B1', 'C1']:
            return 'major'
        if evaluation in ['A3', 'B2', 'C2']:
            return 'normal'
        if evaluation in ['A4', 'B3', 'B4', 'C3']:
            return 'minor'
        if evaluation in ['C4', '~0', '~1', '~2', '~3', '~4']:
            return 'trivial'

        return 'normal'
