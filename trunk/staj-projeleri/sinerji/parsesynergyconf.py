#!/usr/bin/python
# -*- coding: utf-8 -*-

from socket import gethostname
parsedfilelist = []
parsedfileset = set()
clientlist = []
filename = "synergy.conf"

def parse(synergyfile):
    for line in open(synergyfile, "r").readlines():
        parsedfileset.add(line.strip())
    
    parsedfileset.remove("section: screens")
    parsedfileset.remove("section: links")
    parsedfileset.remove("end") 
    parsedfileset.remove("") 
    parsedfilelist = list(parsedfileset) 
    
    for names in parsedfilelist[:]:
        if names.endswith(":"):
            clientlist.append(names.strip(":"))
            parsedfilelist.remove(names)

    


if __name__ == "__main__":
    parse(filename)



