#!/usr/bin/python

import sys
import piksemel as iks

# test accessors
doc = iks.parseString("<a><c>lala<b>merhaba</b>bibi</c><d/></a>")
c = doc.getTag("c")
x = c.firstChild()
if x.root().name() != doc.name():
    print "Error!"
while x:
    if x.type() == iks.CDATA:
        print x.data()
    else:
        print x.name()
    x = x.next()

# test attributes
doc = iks.parseString("<a><blah hede='lala'/></a>")
blah = doc.getTag("blah")
print blah.getAttribute("hede"), blah.getAttribute("hodo")

# test iteration
doc = iks.parse(sys.argv[1])
for a in doc:
    a.toString()
    if a.type() == iks.TAG:
        a.toPrettyString()
doc.toString()
doc.toPrettyString()

# test tag iteration
doc = iks.parse(sys.argv[1])
for tag in doc.tags():
    if tag.getTagData("Size") == "42":
        print tag.toString()

# test builders
doc2 = iks.newDocument("Test")
t = doc2.appendTag("Deneme1")
t.appendTag("isim").appendData("meduketto")
t.setAttribute("url", "6kere9.com")
t = doc2.appendTag("Deneme2")
t.appendTag("isim").appendData("stephen")
t.setAttribute("url", "darktower.com")
print doc2.toPrettyString()


