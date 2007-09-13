from distutils.core import setup, Extension

defs = []

extractor = Extension('_extractor',
                 include_dirs = ['/usr/qt/3/include'],
                 libraries = ['qt-mt'],
                 library_dirs = ['/usr/qt/3/lib'],
                 define_macros = defs,
                 sources = ['_extractor.cpp'])

setup (name = 'extractor',
       version = '0.0',
       description = 'Image extractor',
       py_modules = ['extractor'],
       ext_modules = [extractor])
