import piksemel as iks

doc = iks.newDocument("a")
x = doc.insertTag("b")
x.insertTag("lala")
y = x.insertTag("bibi")
y.prependData("hodo")
assert(x.toString() == "<b><lala/>hodo<bibi/></b>")
x.setData("merhaba")
print x.type()==iks.TAG
print x.data()
assert(x.toString() == "<b>merhaba</b>")
