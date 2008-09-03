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
        if x is not None:    ## If the comboBox is not empty
            domains = x.split("_")
            synergyconf.write("      %s:\n" % domains[2])
        else:
            pass
    synergyconf.write('end\n\n')
    synergyconf.close()


def links(*screen):
    synergyconf = open('synergy.conf', 'a')
    synergyconf.write('section: links\n')
    for y in screen[0]:
        if y is not None: ## If the comboBox is not empty
            subnames.append(y.split('_'))
        else:
            pass
    ### writing the host part ####
    synergyconf.write("      %s:\n" % gethostname())
    for z in subnames:
            if z[0] == 'host':
                pass
            else:
                synergyconf.write("         %s = %s\n" % (z[0], z[2]))

    ### writing the client part ###
    for clients in subnames:
        if clients[2] == gethostname():
            pass
        else:
            synergyconf.write("      %s:\n" % clients[2])
            synergyconf.write("          %s = %s\n" % (clients[1], gethostname()))

    synergyconf.write('end\n')
    synergyconf.close()

if __name__ == "__main__":
    screens(names)
    links(names)
