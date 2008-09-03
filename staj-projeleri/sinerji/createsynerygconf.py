#!/usr/bin/python
# -*- coding: utf-8 -*-


from socket import gethostname
hostname = "host_host_sony"
client = "right_left_lenovo"
client2 = "top_bottom_pardus"
names = hostname, client, client2, None, None
subnames = []

### Takes a tuple of names and write the screen section of synergy.conf
def screens(*screen):
    synergyconf = open('synergy.conf', 'w')
    synergyconf.write('section: screens\n')
    for x in screen[0]:
        if x is not None:
            domains = x.split("_")
            synergyconf.write("      %s:\n" % domains[2])
        else:
            pass
    synergyconf.write('end\n\n')
    synergyconf.close()


def links(*screen, **position):
    synergyconf = open('synergy.conf', 'a')
    synergyconf.write('section: links\n')
    for subnames in screen[0]:
        synergyconf.write("      %s:\n" % subnames)
        synergyconf.write("         %s = %s\n" % (subnames, position))
    synergyconf.write('end\n')
    synergyconf.close()


if __name__ == "__main__":
    screens(names)
    links(names, positionnames)
