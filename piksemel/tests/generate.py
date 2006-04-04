#!/usr/bin/python

import piksemel as iks

doc_xml = """
<test>
    <a><b><c/></b></a>
    <item foo="lala">
        <tuktuk>blah &amp; bleh</tuktuk>
        <nanuk/>
    </item>
    <a/>
</test>
""".strip()

doc = iks.newDocument("test")
doc.insertData("\n    ")
a = doc.insertTag("a")
a.insertTag("b").insertTag("c")
doc.insertData("\n    ")
item = doc.insertTag("item")
item.setAttribute("foo", "lala")
item.insertData("\n        ")
item.insertTag("tuktuk").insertData("blah & bleh")
item.insertData("\n        ")
item.insertTag("nanuk")
item.insertData("\n    ")
doc.insertData("\n    ")
a = doc.insertTag("a")
doc.insertData("\n")
assert(doc.toString() == doc_xml)
