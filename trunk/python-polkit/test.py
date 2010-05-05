import polkit

print polkit.auth_list_all()
#polkit.auth_block(1000, "tr.org.pardus.comar.net.link.set")
