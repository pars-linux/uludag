from distutils.core import setup, Extension

defs = []
try:
    import numarray
    defs.append(('WITH_NUMARRAY',None))
except ImportError:
    pass

sane = Extension('_sane',
                 include_dirs = ['/usr/qt/3/include'],
                 libraries = ['sane','qt-mt'],
                 library_dirs = ['/usr/qt/3/lib'],
                 define_macros = defs,
                 sources = ['_sane.cpp'])

setup (name = 'pysane',
       version = '2.0',
       description = 'This is the pysane package',
       py_modules = ['sane'],
       ext_modules = [sane])
