
def drop_all_tables(cursor):
    cursor.execute('DROP TABLE IF EXISTS history ')
    cursor.execute('DROP TABLE IF EXISTS description ')
    cursor.execute('DROP TABLE IF EXISTS person ')
    cursor.execute('DROP TABLE IF EXISTS package ')
    cursor.execute('DROP TABLE IF EXISTS repository ')
    cursor.execute('DROP TABLE IF EXISTS patch ')
    cursor.execute('DROP TABLE IF EXISTS revdep ')
    cursor.execute('DROP TABLE IF EXISTS component ')
    cursor.execute('DROP TABLE IF EXISTS dependency ')
    cursor.execute('DROP TABLE IF EXISTS conflict ')

def create_all_tables(cursor):
    cursor.execute('CREATE TABLE history (id INTEGER PRIMARY KEY, \
                    release VARCHAR(10), type VARCHAR(10), \
                    date VARCHAR(15), version VARCHAR(20), \
                    comment VARCHAR (250), name VARCHAR(20), \
                    email VARCHAR(25))'
                    )

    cursor.execute('CREATE TABLE package (id INTEGER PRIMARY KEY, \
                    repo INTEGER, name VARCHAR(50), isA VARCHAR(20), \
                    partof VARCHAR(20), license VARCHAR(20), \
                    icon VARCHAR (25))'
                    )

    cursor.execute('CREATE TABLE description (id INTEGER PRIMARY KEY, \
                    packageID INTEGER, locale VARCHAR(6), \
                    summary VARCHAR(250), description VARCHAR(500))' 
                    )

    cursor.execute('CREATE TABLE person (id INTEGER PRIMARY KEY, \
                    name VARCHAR(25), email VARCHAR(40))'
                    )
    
    cursor.execute('CREATE TABLE dependency (id INTEGER PRIMARY KEY, \
                    packageID INTEGER, \
                    version VARCHAR(15), versionfrom VARCHAR(15), versionto VARCHAR(15), \
                    release VARCHAR(15), releasefrom VARCHAR(15), releaseto VARCHAR(15))'
                    )

    cursor.execute('CREATE TABLE conflict (id INTEGER PRIMARY KEY, \
                    packageID INTEGER, \
                    version VARCHAR(15), versionfrom VARCHAR(15), versionto VARCHAR(15), \
                    release VARCHAR(15), releasefrom VARCHAR(15), releaseto VARCHAR(15))'
                    )

    cursor.execute('CREATE TABLE repository (id INTEGER PRIMARY KEY,\
                    name VARCHAR(50), isdefault VARCHAR(10), repoorder INTEGER,\
                    uri VARCHAR(250))'
                    )

    cursor.execute('CREATE TABLE patch (id INTEGER PRIMARY KEY,\
                    packageID INTEGER,\
                    filename VARCHAR(250), compressiontype VARCHAR(10), level INTEGER)'
                    )

    cursor.execute('CREATE TABLE revdep (id INTEGER PRIMARY KEY,\
                    depname VARCHAR(50), packageID INTEGER, deppackageID INTEGER)'
                    )
    
    cursor.execute('CREATE TABLE component (id INTEGER PRIMARY KEY,\
                    name VARCHAR(50))'
                    )
connection = None

def get_connection():
    if connection == None:
        connection = sqlite.connect('pisi.db')
    return conenction 

def get_cursor():
    return get_connection().cursor()
