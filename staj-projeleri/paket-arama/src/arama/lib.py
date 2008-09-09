# encoding: utf8
import sqlite3

DOCUMENT_ROOT = '/home/emre/public_html/arama/src/arama'
WEB_ROOT = '/~emre/arama/src/arama'
DB_FILE = DOCUMENT_ROOT + '/pisidb'


header = ('''
<html>
    <head>
        <title>Arama Sayfasi</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <link href="%(WEB_ROOT)s/stil.css" rel="stylesheet" type="text/css">
    </head>
    <body>
        <div id='header-bugzilla'>
        </div>

        <div class='menu'>
        <a href='%(WEB_ROOT)s/index.html'>Genel Bilgiler</a>
         | <a href='%(WEB_ROOT)s/sources.html'>Kaynak Paketler</a>
        
         | <a href='%(WEB_ROOT)s/binaries.html'>İkili Paketler</a>
         | <a href='%(WEB_ROOT)s/packagers.html'>Paketçiler</a>
         | <a href='%(WEB_ROOT)s/'>Arama</a>
        </div>
        ''' % ({'WEB_ROOT'      : WEB_ROOT,}) ) + ('''
        <h2 align='center'>%s</h2>

        <div class='content'>
        <form action="search" method="post">
        <center>
            <input type="text" name="q" size="80"/>
            <input type="submit" value="Search"/>        
        </center>
''')
footer = '''
        </div>
    </body>
</html>
'''

class TableGenerator:
    def __init__(self, headers, data):
        header_len = len(headers)
        row_num = len(data)
        if data:
            col_num = len(data[0])
        else:
            self.table = Table()
            self.table.close()
            return
        print header_len, col_num, row_num
        if header_len != col_num:
            print header_len, col_num
            raise Exception
        
        self.table = Table()
        self.table.tr()
        for header in headers:
            self.table.th(header)
        self.table.trclose()
        for row in data:
            self.table.tr()
            for col in row:
                self.table.td(col)
            self.table.trclose()
        self.table.close()
    
#(u'eric', u'usr/lib/python2.5/site-packages/eric4/QScintilla/Lexers/LexerMakefile.py'), (u'eric', u'usr/lib/python2.5/site-packages/eric4/Documentation/Source/eric4.QScintilla.Lexers.LexerCMake.html'), (u'eric', u'usr/lib/python2.5/site-packages/eric4/Documentation/Source/eric4.QScintilla.Lexers.LexerMakefile.html'), (u'eric', u'usr/lib/python2.5/site-packages/eric4/QScintilla/Lexers/LexerCMake.py'), 
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
    def __init__(self):
        self.connection = sqlite3.connect(DB_FILE)   
        self.cursor = self.connection.cursor()
    
    def list_package_contents(self, package_name):
        files = self.cursor.execute('select filepath from files where package=?', [package_name]).fetchall()
        files.sort()
        return (header % 'Contents of package %s:' % package_name) + TableGenerator(('Path',), files).table.code + footer
    
    def search_for_package(self, package_name):
        """Searches for a package related to given name in the URL."""
        packages = self.cursor.execute('select distinct package from files where (package LIKE "%%%s%%")' % package_name).fetchall()
        packages.sort()
        return (header % 'List of packages with similar name to %s:' % package_name) + TableGenerator(('Package',), packages).table.code + footer
    
    def search_in_package(self, package_name, term):
        """Searches for term in the given package."""
        files = self.cursor.execute('select filepath from files where package = "%s" and filepath like "%%%s%%"' % (package_name, term)).fetchall()
        files.sort()
        return (header % 'Files related to %s in package %s:' % (term, package_name)) + TableGenerator(('Path', ), files).table.code + footer 
    def search_in_all_packages(self, term = None):
        """Searches for term in all packages' file paths."""
        pairs = self.cursor.execute('select package, filepath from files where filepath like "%%%s%%"' % term).fetchall()
        pairs.sort()
        return (header % 'Files related to %s:' % term) + TableGenerator(('Package', 'Path'), pairs).table.code + footer



def index():
    #return Search().list_package_contents('vlc')
    return Search().search_for_package('test')
    #pi = PisiDBInterface(DB_FILE)
    #return (header % 'Packages related:test')+TableGenerator(('Package', 'Path'), pi.get_packages_of('test').fetchall()).table.code + footer
#print index()

