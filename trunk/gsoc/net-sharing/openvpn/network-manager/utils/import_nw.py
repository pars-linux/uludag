#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import piksemel
import comar
import struct

import pardus.iniutils

class ComarLink(comar.Link):
    __DUMPPROFILE = 16
    def __pack(self, cmd, id, args):
        size = 0
        args2 = []
        # COMAR RPC is using network byte order (big endian)
        fmt = "!ii"
        for a in args:
                    a = str(a)      # for handling unicode
                    fmt += "h%dsB" % (len(a))
                    size += 2 + len(a) + 1
                    args2.append(len(a))
                    args2.append(a.encode("utf-8"))
                    args2.append(0)
        pak = struct.pack(fmt, (cmd << 24) | size, id, *args2)
        return pak
    
    def dump(self, id=0):
        """Dump profile database.
        """
        pak = self.__pack(self.__DUMPPROFILE, id, [])
        self.sock.send(pak)

def main():
    if os.getuid() != 0:
        print 'Must be run as root'
        return 1
    
    link = ComarLink()
    link.dump()
    reply = link.read_cmd()
    
    doc = piksemel.parseString(reply.data)
    for item in doc.tags():
        model, package, name = item.getTagData('key').split('/')
        if model == 'Net.Link':
            name = name.split('=')[1]
            config = {}
            for data in item.tags():
                key = data.getAttribute('key')
                value = data.getTagData('value')
                if not value:
                    continue
                config[key] = value
            db = pardus.iniutils.iniDB('/etc/network/%s' % package)
            db.setDB(name, config)
            print '%s - %s' % (package, name)
    
    return 0

if __name__ == '__main__':
    main()
