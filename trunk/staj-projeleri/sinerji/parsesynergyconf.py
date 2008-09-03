#!/usr/bin/python
# -*- coding: utf-8 -*-

from socket import gethostname


class parseSynergyConf:
    def __init__(self, parsefile):
        self.parsedfilelist = []
        self.parsedfileset = set()
        self.domain = []
        self.clients = []
        self.parsing(parsefile)

    def parsing(self, synergyfile):
        for line in open(synergyfile, "r").readlines():
            self.parsedfileset.add(line.strip())
        
        ### Remove end, section and newlines
        self.parsedfileset.remove("section: screens")
        self.parsedfileset.remove("section: links")
        self.parsedfileset.remove("end") 
        self.parsedfileset.remove("") 
        self.parsedfilelist = list(self.parsedfileset) 
        
        ### Removes lines which ends with ":" 
        for names in self.parsedfilelist[:]:
            if names.endswith(":"):
                self.parsedfilelist.remove(names)

        ### Remove hostnames
        for position in self.parsedfilelist[:]:
            domain = position.split(" = ")
            if domain[1] == gethostname():
                self.parsedfilelist.remove(position)

        ### Create our final client and position list
        for client in self.parsedfilelist:
            self.clients.append(client.split(" = "))

    def getClients(self):
        return self.clients

if __name__ == "__main__":
    parse(filename)



