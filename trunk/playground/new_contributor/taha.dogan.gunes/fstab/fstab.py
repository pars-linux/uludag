#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
fstab.py - reads and edits /etc/fstab
"""

# Copyright (C) 2010 Taha Doğan Güneş <tdgunes@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

class Line(object):
    """
    Line object for fstab, keeps the line in a dictionary.

    Notes:
        - To create a blank line:
            >>> line = Line()
            >>> line.set_fs(string)
            >>> line.set_mountpoint(string)
            >>> line.set_type(string)
            >>> line.set_opts(list)
            >>> line.set_dump(integer/string)
            >>> line.set_pass(integer/string)
            or
            >>> line.set_values(fs=string,
                                mountpoint=string,
                                type=string,
                                opts=list,
                                dump=int/str,
                                passvalue=int/str)
    """

    def __init__(self, line=""):
        """
        line is a normal string from fstab object.
        """

        self.line = line
        if line is not "":
            self.dict = self.dict_builder(line)
        else:
            self.dict = self.dict_builder("fs mounpoint type default 0 0")

    def __getattr__(self, name):
        """
        To use line object like line.fs etc.
        """

        others = ["dump",
                  "passvalue"]

        if name in self.dict:
            if name in others:

                return int(self.dict[name])
            else:
                return self.dict[name]
        else:
            return AttributeError(name)

    def __setattr__(self, name, value):
        """
        In other to use normal commands.
        """

        object.__setattr__(self, name, value)


    def __str__(self):
        """
        Returns a normal string line.
        """
        return self.return_line()

    def dict_builder(self, line):
        """
        making dictionary editable
        """
        slist = [i.strip() for i in line.split()]

        mydict = {"fs":slist[0],
                 "mountpoint":slist[1],
                 "type":slist[2],
                 "opts":slist[3],
                 "dump":slist[4],
                 "passvalue":slist[5]}

        return mydict

    def set_fs(self, value):
        """
        to change fs value
        """

        self.dict["fs"] = str(value)

    def set_mountpoint(self, value):
        """
        to change mountpoint value
        """
        self.dict["mountpoint"] = str(value)

    def set_type(self, value):
        """
        to change type
        """
        self.dict["type"] = str(value)

    def set_opts(self, listvalue):
        """
        to change opts but this requires a list
        """
        self.dict["opts"] = ",".join(listvalue)

    def set_dump(self, value):
        """
        to set dump
        int or str
        """
        self.dict["dump"] = str(value)

    def set_pass(self, value):
        """
        to set pass value
        int or str 
        """
        self.dict["passvalue"] = str(value)

    def set_values(self,
                   fs="fs",
                   mountpoint="mountpoint",
                   type="type",
                   opts=["default"],
                   dump=0,
                   passvalue=0):
        """
        This is for setting all values
        dump and passvalue should be integer
        """
        self.dict = {}
        opts = ",".join(opts)
        line = " ".join([fs,
                         mountpoint,
                         type,
                         opts,
                         str(dump),
                         str(passvalue)])

        self.dict = self.dict_builder(line)
                   
    def return_line(self):
        """
        returns line to the __str__
        """
        mylist = [self.dict["fs"],
                  self.dict["mountpoint"],
                  self.dict["type"],
                  self.dict["opts"],
                  self.dict["dump"],
                  self.dict["passvalue"]]
        return " ".join(mylist)


def write_fstab(lineobj, path="/etc/fstab"):
    """
    writes with using given 
    Line object included (or not) in a list
    """
    text = "\n".join([str(line) for line in lineobj])
    fstabfile = open(path, 'w')
    fstabfile.write(text)

def read_fstab(path="/etc/fstab"):
    """
    reads it and returns lines 
    without Line object
    """
    fstabfile = open(path, "r")
    return (fstabfile.read().split("\n"))

def get_lines(path="/etc/fstab"):
    """
    loads lines from path
    """
    returnlist = []
    lines = read_fstab(path)
    for line in lines:
        if line is "":
            returnlist.append(line)
        elif line[0] not in ["#",
                          "\t",
                          " ",
                          ]:
            lineobj = Line(line)
            returnlist.append(lineobj)
        else:
            returnlist.append(line)
    return (returnlist)

def add_line(line, path="/etc/fstab"):
    """
    Add a line to the file
    """
    lines = read_fstab(path)
    lines.append(line)
    write_fstab(lines)

def del_line(fsvalue="", path="/etc/fstab"):
    """
    deletes a line from path with using fs value
    if deleted=True, if not False
    """
    boolean = False
    lines = get_lines()
    lineobjs = []
    for line in lines:
        if type(line) is not type(""): #to get Line objects
            lineobjs.append(line)
    lines = []
    for line in lineobjs:
        if line.fs != fsvalue and line.fs[6:] != fsvalue:
            lines.append(line)
        else:
            boolean = True
    write_fstab(lines, path)
    return (boolean)



