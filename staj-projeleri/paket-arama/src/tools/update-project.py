"""Script that has to be run after updating the project.
- Updates the po files.
- Asks for manual po editing.
- Generates msg.py file
- Generates a new search dir.(english version)"""

#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

print 'Updating po file msgids...'
os.system('sh tools/update-po.sh')
print 'Please update the po file msgstr lines.'
c = 'n'
while c not in ['y','Y','e','E']:
    c = raw_input('Are you done (y/n)?')

print 'Great! Then I can generate the msg.py file...'
from gettrans import *
get_trans()
print 'I have generated the msg.py file.'
print 'Now I\'m generating the search directory'

from geneng import *
generate_english()

print 'Finished...'