import os
from msg import messages

os.system('sh ../tools/update-po.sh')
f = open('../po/tr.po')
lines = ['messages = {',
	 '#/usr/bin/python',
	 '# -*- coding: utf-8 -*-',]
for line in f:
	start = line.find('msgid ')
	if start == -1:
		continue
	end = line.rfind('"')
	statement = line[start+7:end]
	if statement:
		new = "'%s' : '%s'," % (statement, messages.get(statement))
		lines.append(new)

lines.append('}')
f = open('msg.py','w')
f.write("\n".join(lines))
f.close()

