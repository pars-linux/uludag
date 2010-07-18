from setuptools import setup
import py2exe

# Setup file planned for py2exe builds. 

# See http://www.py2exe.org/index.cgi/ListOfOptions for more options
# about distutils and py2exe.

setup (
  name = 'PaW', #TODO: change
  version = '0.1', #TODO: change
  author = 'uekae', #TODO: change
  author_email = '', #TODO: change
  description = 'Paw inst', #TODO: change
  long_description = 'Long description of the package', #TODO: change
  url = '', #TODO: change
  license = '', #TODO: change
  
  download_url= '', #TODO: change

  windows = ['__main__.py'],

  options = {
            'py2exe' : {
                'includes' : ['sip', 'win32api', '_winreg', 'ctypes'],
                'excludes' : ['_ssl'],
                'optimize' : 2,
                'dist_dir': 'dist',
                'xref' : False, # can be enabled for debugging.
                'compressed' : False,
                'ascii' : False
            }
    }
)
