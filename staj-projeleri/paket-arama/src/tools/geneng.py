"""Generates English directory for the search engine, puts an empty dictionary file as msg.py"""

#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import shutil

def generate_english():
    if os.path.exists('search'):
        shutil.rmtree('search')
    shutil.copytree('arama', 'search')
    shutil.copy('tools/msg-en.py', 'search/msg.py')

if __name__ == '__main__':
    generate_english()