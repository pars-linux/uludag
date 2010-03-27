# nvd.py -- simplistic NVD parser
# Copyright (C) 2005 Florian Weimer <fw@deneb.enyo.de>
# 
# Modifications by Robert Buchholz <rbu@gentoo.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

"""This module parses the XML files provided by the
National Vulnerability Database (NVD) <http://nvd.nist.gov/>
"""

import xml.sax
import xml.sax.handler
import datetime

class _Parser(xml.sax.handler.ContentHandler):
    """Parser helper class."""

    def __init__(self):
        self.result = {}
        self.start_dispatcher = {}
        for x in ('entry', 'local', 'range', 'network', 'local_network', 'user_init',
                  'avail', 'conf', 'int', 'sec_prot', 'prod', 'ref'):
             self.start_dispatcher[x] = getattr(self, 'TAG_' + x)
        self.path = []

    def _noop(*args):
        pass

    def startElement(self, name, attrs):
        self.path.append((name, attrs))
        self.start_dispatcher.get(name, self._noop)(name, attrs)

    def TAG_entry(self, name, attrs):
        try:
            self.name = attrs['name']
            if not isinstance(self.name, unicode):
                self.name = self.name.encode('utf-8')
        except KeyError:
            pass

        try:
            self.published = attrs['published']
            if not isinstance(self.published, unicode):
                self.published = self.published.encode('utf-8')
        except KeyError:
            pass

        try:
            self.modified = attrs['modified']
            if not isinstance(self.modified, unicode):
                self.modified = self.modified.encode('utf-8')
        except KeyError:
            self.modified = str(datetime.date.today()).encode('utf-8')

        try:
            self.severity = attrs['severity']
            if not isinstance(self.severity, unicode):
                self.severity = self.severity.encode('utf-8')
        except KeyError:
            self.severity = u''

        try:
            self.discovered = attrs['discovered']
            if not isinstance(self.discovered, unicode):
                self.discovered = self.discovered.encode('utf-8')
        except KeyError:
            self.discovered = u''

        self.cve_desc = ""
        self.range_local = self.range_network = self.range_local_network \
            = self.range_user_init = None

        self.loss_avail = self.loss_conf = self.loss_int \
            = self.loss_sec_prot_user = self.loss_sec_prot_admin \
            = self.loss_sec_prot_other = 0

        self.product_name = self.product_vendor = None
        
        self.refs = []

    def TAG_range(self, name, attrs):
        self.range_local = self.range_local_network = self.range_network = self.range_user_init = 0

    def TAG_local(self, name, attrs):
        self.range_local = 1
    def TAG_network(self, name, attrs):
        self.range_network = 1
    def TAG_local_network(self, name, attrs):
        self.range_local_network = 1
    def TAG_user_init(self, name, attrs):
        self.range_user_init = 1
    def TAG_loss_types(self, name, attrs):
        self.clear_loss()
    def TAG_avail(self, name, attrs):
        self.loss_avail = 1
    def TAG_conf(self, name, attrs):
        self.loss_conf = 1
    def TAG_int(self, name, attrs):
        self.loss_int = 1
    def TAG_sec_prot(self, name, attrs):
        if attrs.has_key('user'):
            self.loss_sec_prot_user = 1
        if attrs.has_key('admin'):
            self.loss_sec_prot_admin = 1
        if attrs.has_key('other'):
            self.loss_sec_prot_other = 1
    def TAG_prod(self, name, attrs):
        try:
            self.product_name = attrs['name']
            if not isinstance(self.product_name, unicode):
                self.product_name = self.product_name.encode('utf-8')
        except KeyError:
            pass

        try:
            self.product_vendor = attrs['vendor']
            if not isinstance(self.product_vendor, unicode):
                self.product_vendor = self.product_vendor.encode('utf-8')
        except KeyError:
            pass
    def TAG_ref(self, name, attrs):
        if attrs.has_key('url'):
            self.refs.append([attrs['source'], attrs['url']])

    def endElement(self, name):
        if name == 'entry':
            self.result[self.name] = {
                                'desc': self.cve_desc,
                                'discovered': self.discovered,
                                'published': self.published,
                                'modified': self.modified,
                                'severity': self.severity,
                                'range_local': self.range_local,
                                'range_network': self.range_network,
                                'range_local_network': self.range_local_network,
                                'range_user_init': self.range_user_init,
                                'loss_avail': self.loss_avail,
                                'loss_conf': self.loss_conf,
                                'loss_int': self.loss_int,
                                'loss_sec_prot_user': self.loss_sec_prot_user,
                                'loss_sec_prot_admin': self.loss_sec_prot_admin,
                                'loss_sec_prot_other': self.loss_sec_prot_other,
                                'product_name': self.product_name,
                                'product_vendor': self.product_vendor,
                                'refs' : self.refs}
        del self.path[-1]

    def characters(self, content):
        (name, attrs) = self.path[-1]
        if name == 'descript' and attrs['source'] == 'cve':
            self.cve_desc += content

def parseAll(files):
    """Parses the indicated files.  Returns a dictionary,
    containing the following elements:

    - CVE name
    - discovery data (can be empty)
    - publication date
    - last modification date
    - name of the vulnerable software
    - severity (can be empty)
    - local range flag
    - network range flag
    - local_network range flag
    - availability loss type flag
    - confidentiality loss type flag
    - integrity loss type flag
    - security protection (user) loss type flag
    - security protection (admin) loss type flag
    - security protection (other) loss type flag
    """
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    p = _Parser()
    parser.setContentHandler(p)
    for name in files:
        file = open(name)
	try:
        	parser.parse(file)
	except xml.sax._exceptions.SAXParseException, e:
		print "XML Parsing error at %s: %s" % (name, e)
        file.close()
    return p.result

if __name__ == "__main__":
    import sys
    for name in sys.argv[1:]:
        parse(file(name))
