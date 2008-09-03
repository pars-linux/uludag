import pisi
import time
import sqlite3


class Kertenkele:
    def __init__(self, db_name):
        self.dbi    = PisiDBInterface(db_name)
        self.pi     = pisi.db.installdb.InstallDB()
        
        self.installed_packages = self.pi.list_installed()
        print 'Fetched the installed packages'
        print 'Creating the db file: %s...' % db_name
        self.dbi.create_table()        
        print 'Starting to populate the db.'
        self.insert_all_installed_packages()
        print 'Inserted all the installed packages.'
        self.dbi.create_index()
        print 'Created index for the table on package name.'
        
    def path_of_file(self, file_info_object):
        return file_info_object.path
        
    def file_list_of(self, package):
        return map(self.path_of_file, self.pi.get_files(package).list) 
    
    # ==============================
    
    def insert_all_installed_packages(self):
        import time
        start = time.time()
        for package in self.installed_packages:
            self.insert_package(package, commit=False)
        finish = time.time()
        
        diff = finish - start
        print 'Time:', diff
        self.dbi.db.commit()
        
    def insert_package(self, package, commit=True):
        self.dbi.add_package(package, self.file_list_of(package), commit)
        
    def remove_package(self, package):
        self.dbi.remove_package(package)
         
        
class PisiDBInterface:
    def __init__(self, db_name):
        """Loads the database settings and creates a database connection."""

        self.db_name = db_name

        
        # Create a database connection
        self.db = SQLDB(self.db_name)
        
    def create_table(self):
        """Creates the table."""        
        st = 'CREATE table files (package text, filepath text);'
        
        try:
            self.db.query(st)
        except:
            print 'Table exists, dropping it...'
            self.db.query('DROP table files')
            self.db.query(st)
        
        self.db.commit()
        
    def create_index(self):
        """Creates the index."""
        st = 'CREATE INDEX pkg_index on files (package ASC);'
        self.db.query(st)
        self.db.commit()
        
    # ============ DML QUERIES =================
    
    def add_package(self, package_name, file_paths, commit = True):
        """Adds the given package with the filepaths into the database."""
        for file_path in file_paths:
            st = 'insert into files values(?, ?);'
            self.db.query(st, (package_name, file_path))
        if commit: 
            self.db.commit()
        
    def remove_package(self, package_name):
        """Removes the package with the given name from the database."""
        st = 'delete from files where package = ?;'
        self.db.query(st, [package_name])
        self.db.commit()
        
        
        
    # ============ SELECT QUERIES ============
        
    def get_files_of(self, package_name):
        """Returns the files in a given package"""
        st = 'select filepath from files where package = ?'
        results = self.db.query(st, package_name)
        return results.fetchall()
        
    def get_packages_of(self, file_path):
        """Returns the packages which own the file specified."""
        st = "select package, filepath from files where filepath like '%%%s%%'" % file_path
        print st
        results = self.db.query(st)
        return results.fetchall()
            
    
    def __del__(self):
        del self.db
        

class SQLDB:
    def __init__(self, filename):
        self.conn = sqlite3.connect(filename)
        self.c = self.conn.cursor()
        
    def __del__(self):
        self.close()
        
    def query(self, statement, params=None):
        if params:
            return self.c.execute(statement, params)
        else:
            return self.c.execute(statement)
        
    def commit(self):
        self.conn.commit()
        
    def close(self):
        self.c.close()
        


def main():
    import os
    if os.path.exists('./pisidb'):
        print 'Found another pisidb, creating pisidb2 temporarily.'
        temp = Kertenkele('pisidb2')
        os.rename('pisidb2', 'pisidb')
        print 'Renamed pisidb2 to pisidb'
    else:
        permanent = Kertenkele('pisidb')
    print 'Finished...'
    
    
if __name__ == '__main__':
    main()