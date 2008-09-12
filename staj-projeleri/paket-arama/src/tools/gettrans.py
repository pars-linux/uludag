"""Converts po/tr.po file into arama/msg.py as a dictionary called messages."""

#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

def get_between(line, keyword):
	start = line.find(keyword)
	if start == -1:
		# No msgid or msgstr line.
		return ''
	matched = False
	end = line.rfind('"')
	statement = line[start+len(keyword)+1:end]
	return statement


def get_trans():
	messages = {}
	f = open('po/tr.po')
	lines = ['#/usr/bin/python',
		 	'# -*- coding: utf-8 -*-',
		 	'messages = {',]
	
	matched = True
	for line in f:
		if not matched:
			# If not matched yet, msgid seen, now looking for msgstr
			statement = get_between(line, 'msgstr ')
			translation = statement
			new = "'%s' : '%s'," % (original, translation)
			lines.append(new)
			matched = True
		else:
			# If matched, looking for a new msgid
			statement = get_between(line, 'msgid ')
			if statement:
				original = statement
				matched = False
	
	lines.append('}')
	f = open('arama/msg.py','w')
	f.write("\n".join(lines))
	f.close()
	
if __name__ == '__main__':
	get_trans()