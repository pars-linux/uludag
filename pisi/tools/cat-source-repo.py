#! /usr/bin/python

import sys
import os

import pisi
import pisi.api
import pisi.config
import pisi.specfile as specfile
import pisi.context as ctx
import pisi.util

options = pisi.config.Options()
if len(sys.argv)>2:
    options.destdir=sys.argv[2]
else:
    options.destdir = '/'
pisi.api.init(database=False, options=options)
repo_uri = sys.argv[1]

for root, dirs, files in os.walk(repo_uri):
    for fn in files:
        if fn == 'pspec.xml':
            #ctx.ui.info(_('Adding %s to package index') % fn)
            sf = specfile.SpecFile()
            sf.read(pisi.util.join_path(root, fn))
            print sf.source.name, sf.source.partOf

pisi.api.finalize()
