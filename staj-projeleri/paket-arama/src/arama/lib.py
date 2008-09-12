#/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
from settings import *
#import gettext
#__trans = gettext.translation('arama', fallback=True)
#_ = __trans.ugettext

import msg
def _(text):
	return msg.messages.get(text) or text


dict = {
            "root": root,
            "menu1": _("Information"),
            "menu2": _("Source Packages"),
            "menu3": _("Binary Packages"),
            "menu4": _("Packagers"),
            "menu5": _("Search Packages"),
            "title": _("Search Packages"),
            "search": _("Search"),
            "back"  : _("Back"),
            "packages": _("packages"),
        }
        
        
def header(v=2008):
	dict['version']=v
	ov = ''
	root = dict['root']

	for va in versions:
		ov += '| <a href="%s/?v=%s">%s</a>' % (root, va, 'Pardus %s' % va)
	dict['otherversions'] = ov
	
	return ('''
<html>
    <head>
        <title>%(title)s</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <link href="%(root)s/stil.css" rel="stylesheet" type="text/css">
    </head>
    <body>
        <div id='header-bugzilla'>
        	<div style='float:right; margin-right:2em'>
        		<h1>Pardus %(version)s</h1>
        		%(otherversions)s
        	</div>
        </div>

        <div class='menu'>
        <a href='http://%(packages)s.pardus.org.tr/info/%(version)s/index.html'>%(menu1)s</a>
         | <a href='http://%(packages)s.pardus.org.tr/info/%(version)s/sources.html'>%(menu2)s</a>
         | <a href='http://%(packages)s.pardus.org.tr/info/%(version)s/binaries.html'>%(menu3)s</a>
         | <a href='http://%(packages)s.pardus.org.tr/info/%(version)s/packagers.html'>%(menu4)s</a>
         | <a href='%(root)s/?v=%(version)s'>%(menu5)s</a>

        </div>
        <div class='content' align='center'>
        <p><a href='javascript: history.go(-1)'>%(back)s</a></p>
        
        
        <form action="%(root)s/results" method="post">
            <input type="text" name="q" size="80"/>
            <input type="hidden" name="v" value="%(version)s"/>
            <input type="submit" value="%(search)s"/> 
        </form>       
        ''' % dict) + '''
        <h2>%s</h2>
'''
def footer():
	return '''
        <hr width="40%%"/>
        <a href='javascript: history.go(-1)'>%(back)s</a>
        </div>
    </body>
</html>''' % {'back' : _('Back')}

class TableGenerator:
    def __init__(self, version, headers, data, term_link=None):
    	self.version = version
    	if term_link == '" "':
    		term_link = ' '
        self.term_link = term_link
        header_len = len(headers)
        row_num = len(data)
        if data:
            col_num = len(data[0])
        else:
            self.table = Table()
            self.table.close()
            return
        if header_len != col_num:
            raise Exception
        
        self.table = Table()
        self.table.tr()
        for header in headers:
            self.table.th(header)
        self.table.trclose()
        for row in data:
            self.table.tr()
            if self.term_link not in [None, []]:
                for col in row:
                    self.table.td(self.format_link(col))
            else:
                for col in row:
                    self.table.td(col)
            self.table.trclose()
        self.table.close()
        
    def format_link(self, data):
        if type(data) == str and '/' not in data:
            return '<a href="results/?v=%(version)s&q=%(term)s in:%(pkg)s">%(pkg)s</a>' % {'term' : self.term_link,
                                                                                            'pkg'  : data,
                                                                                            'version' :self.version,
                                                                                          }
        else:
            return data
         
class Table:
    def __init__(self):
        self.code = '<table>\n'
        self.tropen = False
        
    def tr(self):
        if self.tropen: # REMOVE THIS
            self.trclose()
            self.tr()    
        self.code += '\t<tr>\n'
        self.tropen = True
        
    def td(self, data):
        self.code += '\t\t<td>%s</td>\n' % data
    def th(self, data):
        self.code += '\t\t<th>%s</th>\n' % data
        
    def trclose(self):
        self.code += '\t</tr>\n'
        self.tropen = False
    def close(self):
        self.code += '</table>'
    
class Search:
    def __init__(self, v):
        self.db=MySQLdb.connect(dbhost, dbuser, dbpass, dbname)
        self.cursor = self.db.cursor()
        self.limit = limit
        self.v = v          # Version: 2008/2009/etc.
        
    def __del__(self):
        self.db.close()
    
    def list_package_contents(self, package_name):
        """Lists the contents of a given package name."""
        self.cursor.execute('select path from %(table)s where package="%(package)s" order by path;' % {'table': 'files%s' % self.v, 
																									   'package': package_name})
        files = self.cursor.fetchmany(self.limit)
        if self.limit>0 and self.limit<self.cursor.rowcount:
            partial = _('(first %s)') % self.limit
        else:
            partial = ''
            
        if package_name:
            heading = _('Contents of package %(pkg)s %(partial)s:')
        else:
            heading = _('No package specified.')
        
        return (header(self.v) % heading % {'pkg':package_name,
                                    'partial' : partial}) + TableGenerator(self.v, (_('Path'),), files).table.code + footer()
    
    def search_for_package(self, package_name):
        """Searches for a package related to given name in the URL."""
        self.cursor.execute('select package, count(path) from %(table)s where package LIKE "%%%(pkg)s%%" group by package order by package;' % {'pkg':package_name,
																																		    'table': 'files%s' % self.v })
        packages = self.cursor.fetchall()
        if package_name:
            heading = _('List of packages with a similar name to %(pkg)s:')
        else:
            heading = _('List of packages:')
        return (header(self.v) % heading % {'pkg':package_name}) + TableGenerator(self.v, (_('Package'),_('Count')), packages, '').table.code + footer()
    
    def search_in_package(self, package_name, term):
        """Searches for term in the given package."""
        if not term:
            return self.list_package_contents(package_name)
        searchTerm = term.strip('"')
        self.cursor.execute('select path from %(table)s where package = "%(pkg)s" and path like "%%%(term)s%%" order by path;' % {'pkg':package_name,
																																  'term': searchTerm,
																																  'table': 'files%s' % self.v})
        files = self.cursor.fetchmany(self.limit)
        if self.limit>0 and self.limit<self.cursor.rowcount:
            partial = _('(first %s)') % self.limit
        else:
            partial = ''

        return (header(self.v) % _('Files related to %(term)s in package %(pkg)s %(partial)s:') % {'pkg':package_name,
                                                                               'term': term,
                                                                               'partial': partial,}) + TableGenerator(self.v, (_('Path'), ), files).table.code + footer()
     
    def search_in_all_packages(self, term = None):
        """Searches for term in all packages' file paths."""
        self.cursor.execute('select package, count(path) from %(table)s where path like "%%%(term)s%%" group by package  order by package;"' % {'term': term,
																																			    'table': 'files%s' % self.v})
        pairs = self.cursor.fetchall()
        if term == ' ':
        	term = '" "'
        return (header(self.v) % _('Files related to %(term)s:') % {'term':term}) + TableGenerator(self.v, (_('Package'), _('Count')), pairs, term).table.code + footer()




