#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
from os.path import join

keys = ["ebegin", "ewarn", "eerror"]
out_file = 'init.tr'
init_dir = '/etc/init.d'

#files to be excluded..
exclude = ['functions.sh']

init_files = [file for file in glob.glob(join(init_dir, '*')) if file not in exclude]

for init_file in init_files:
    lines = [line.strip('\n').strip('\t') for line in open(init_file).readlines() if line[0] is not '#']

    for lnum in range(0, len(lines)):
        for key in keys:
            if lines[lnum].find(key) > -1:
                open(out_file, 'a').writelines('# %s:%s (%s)\n' % (init_file, lnum, key))
                open(out_file, 'a').writelines('msgid %s\n' % (lines[lnum].split(key)[-1:][0].strip()))
                open(out_file, 'a').writelines('msgstr ""\n\n\n')
