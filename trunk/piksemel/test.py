#!/usr/bin/python

import sys
import piksemel as iks

doc = iks.parse(sys.argv[1])
for tag in doc.tags():
    if tag.getTagData("Size") == "42":
        print tag.toString()

doc2 = iks.newDocument("Test")
t = doc2.appendTag("Deneme1")
t.appendTag("isim").appendData("meduketto")
t.setAttribute("url", "6kere9.com")
t = doc2.appendTag("Deneme2")
t.appendTag("isim").appendData("stephen")
t.setAttribute("url", "darktower.com")
print doc2.toPrettyString()


