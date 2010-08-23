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

        others = ["dump","passvalue"]
        if name in self.dict:
            if name in others:
                return int(self.dict[name])
            else:
                return self.dict[name]
        else:
            return AttributeError(name)

    def __setattr__(self, name, value):

        object.__setattr__(self, name, value)

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

        self.dict["fs"]= str(value)

    def set_mountpoint(self, value):

        self.dict["mountpoint"] = str(value)

    def set_type(self, value):

        self.dict["type"] = str(value)

    def set_opts(self, listvalue):

        self.dict["opts"] = ",".join(listvalue)

    def set_dump(self, value):

        self.dict["dump"] = str(value)

    def set_pass(self, value):

        self.dict["passvalue"] = str(value)

    def set_values(self,
                   fs="fs",
                   mountpoint="mountpoint",
                   type="type",
                   opts=["default"],
                   dump=0,
                   passvalue=0):

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
        mylist = [self.dict["fs"],
                  self.dict["mountpoint"],
                  self.dict["type"],
                  self.dict["opts"],
                  self.dict["dump"],
                  self.dict["passvalue"]]
        return " ".join(mylist)


class Fstab:
    """
    fstab object for loading and saving.

    Notes:
        - To delete a line : fstabobject.lines.pop(0)
        - To add a new line : fstabobject.lines.append(fstab.Line("a b c d e f"))
        - To edit a line : fstabobject.lines[x].set_fs(string)
        - To edit a line's options = fstabobject.lines[x].set_opts(list)
    """

    def __init__(self, path):

        self.path = path
        self.lines = []
        self.descriptions = []
        self.load_lines()

    def load_lines(self):
        """
        loads lines from self.path
        """

        fstabfile = open(self.path,"r")
        lines = fstabfile.readlines()
        for line in lines:
            if line[0] is not "#":
                lineobj = Line(line)
                self.lines.append(lineobj)
            elif line[0] is "#":
                self.descriptions.append(line)

    def write_lines(self):
        """
        writes lines to the given path
        """
        fstabfile = open(self.path,"w")
        fstabfile.write(self.show_lines())

    def show_lines(self):
        """
        shows lines, not writes them
        """
        firstlines = "".join([i for i in self.descriptions]) 
        text = "\n".join([lineobj.return_line() for lineobj in self.lines])
        return firstlines+text


