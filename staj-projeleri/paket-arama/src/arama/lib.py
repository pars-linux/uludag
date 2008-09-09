# encoding: utf8
import MySQLdb
import gettext

__trans = gettext.translation('paketarama', fallback=True)
_ = __trans.ugettext


DOCUMENT_ROOT = '/home/emre/public_html/arama/src/arama'
root = '/~emre/arama/src/arama'


dict = {
            "root": root,
            "menu1": _("Information"),
            "menu2": _("Source Packages"),
            "menu3": _("Binary Packages"),
            "menu4": _("Packagers"),
            "menu5": _("Search"),
        }
        
        
        
header = ('''
<html>
    <head>
        <title>Arama Sayfasi</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <link href="%(root)s/stil.css" rel="stylesheet" type="text/css">
    </head>
    <body>
        <div id='header-bugzilla'>
        </div>

        <div class='menu'>
        <a href='http://paketler.pardus.org.tr/info/2008/index.html'>%(menu1)s</a>
         | <a href='http://paketler.pardus.org.tr/info/2008/sources.html'>%(menu2)s</a>
         | <a href='http://paketler.pardus.org.tr/info/2008/binaries.html'>%(menu3)s</a>
         | <a href='http://paketler.pardus.org.tr/info/2008/packagers.html'>%(menu4)s</a>
         | <a href='%(root)s/'>%(menu5)s</a>
        </div>
        <div class='content'>
        <form action="%(root)s/search" method="post">
        ''' % dict) + '''
        <center>
            <input type="text" name="q" size="80"/>
            <input type="submit" value="Search"/>        
        </center>
        <h2 align='center'>%s</h2>
'''
footer = '''
        <hr width="40%"/>
        </div>
    </body>
</html>
'''

class TableGenerator:
    def __init__(self, headers, data, term_link=None):
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
            return '<a href="search/?q=%(term)s in:%(pkg)s">%(pkg)s</a>' % {'term' : self.term_link,
                                                       'pkg'  : data
                                                       }
        else:
            return data
         
class Table:
    def __init__(self):
        self.code = '<center><table>\n'
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
        self.code += '</table></center>'
    
class Search:
    def __init__(self):
        self.db=MySQLdb.connect("localhost","root","", "paketarama")
        self.cursor = self.db.cursor()
        
    def __del__(self):
        self.db.close()
    
    def list_package_contents(self, package_name):
        """Lists the contents of a given package name."""
        self.cursor.execute('select path from files where package="%s" order by path;' % package_name)
        files = self.cursor.fetchall()
        if package_name:
            heading = _('Contents of package %(pkg)s:')
        else:
            heading = _('No package specified.')
        
        return (header % heading % {'pkg':package_name}) + TableGenerator((_('Path'),), files).table.code + footer
    
    def search_for_package(self, package_name):
        """Searches for a package related to given name in the URL."""
        self.cursor.execute('select package, count(path) from files where package LIKE "%%%(pkg)s%%" group by package order by package;' % {'pkg':package_name})
        packages = self.cursor.fetchall()
        if package_name:
            heading = _('List of packages with a similar name to %(pkg)s:')
        else:
            heading = _('List of packages:')
        return (header % heading % {'pkg':package_name}) + TableGenerator((_('Package'),_('Count')), packages, '').table.code + footer
    
    def search_in_package(self, package_name, term):
        """Searches for term in the given package."""
        self.cursor.execute('select path from files where package = "%(pkg)s" and path like "%%%(term)s%%" order by path;' % {'pkg':package_name, 'term': term})
        files = self.cursor.fetchall()
        return (header % _('Files related to %(term)s in package %(pkg)s:') % {'pkg':package_name,
                                                                               'term': term}) + TableGenerator((_('Path'), ), files).table.code + footer
     
    def search_in_all_packages(self, term = None):
        """Searches for term in all packages' file paths."""
        self.cursor.execute('select package, count(path) from files where path like "%%%(term)s%%" group by package  order by package;"' % {'term': term})
        pairs = self.cursor.fetchall()
        return (header % _('Files related to %(term)s:') % {'term':term}) + TableGenerator((_('Package'), _('Count')), pairs, term).table.code + footer




