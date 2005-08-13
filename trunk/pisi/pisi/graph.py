# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

# the most simple minded digraph class ever


# for python 2.3 compatibility
import sys
ver = sys.version_info
if ver[0] <= 2 and ver[1] < 4:
    from sets import Set as set

import pisi

# not an error!

class CycleException(pisi.Exception):
    pass

class digraph(object):

    def __init__(self):
        self.__v = set()
        self.__adj = {}
        self.__vdata = {}
        self.__edata = {}
        
    def vertices(self):
        "return set of vertex descriptors"
        return self.__v

    def edges(self):
        "return a list of edge descriptors"
        list = []
        for u in self.__v:
            for v in self.__u:
                list.append( (u,v) )
        return list

    def from_list(self, el):
        "convert a list of edges (u,v) to graph"
        for (u,v) in el:
            self.add_edge(u,v)

    def add_vertex(self, u, data = None):
        "add vertex u, optionally with data"
        assert not u in self.__v
        self.__v.add(u)
        self.__adj[u] = set()
        if data:
            self.__vdata[u] = data
            self.__edata[u] = {}

    def add_edge(self, u, v, edata = None, udata = None, vdata = None):
        "add edge u -> v"
        if not u in self.__v:
            self.add_vertex(u, udata)
        if not v in self.__v:
            self.add_vertex(v, vdata)
        self.__adj[u].add(v)
        if edata != None:
            self.__edata[u][v] = edata

    def add_biedge(self, u, v, edata = None):
        self.add_edge(u, v, edata)
        self.add_edge(v, u, edata)

    def set_vertex_data(self, u, data):
        self.__vdata[u] = data

    def vertex_data(self, u):
        return self.__vdata[u]

    def edge_data(self, u, v):
        return self.__edata[u][v]

    def has_vertex(self, u):
        return u in self.__v

    def has_edge(self, u,v):
        if u in self.__v:
            return v in self.__adj[u]
        else:
            return False

    def adj(self, u):
        return self.__adj[u]

    def dfs(self, finish_hook = None):
        self.color = {}
        self.p = {}
        self.d = {}
        self.f = {}
        for u in self.__v:
            self.color[u] = 'w'         # mark white (unexplored)
            self.p[u] = None
        self.time = 0
        for u in self.__v:
            if self.color[u] == 'w':
                self.dfs_visit(u, finish_hook)

    def dfs_visit(self, u, finish_hook):
        self.color[u] = 'g'             # mark green (discovered)
        self.d[u] = self.time = self.time + 1
        for v in self.adj(u):
            if self.color[v] == 'w':    # explore unexplored vertices
                self.p[v] = u
                self.dfs_visit(v, finish_hook)
            elif self.color[v] == 'g':  # cycle detected
                raise CycleException
        self.color[u] = 'b'             # mark black (completed)
        if finish_hook:
            finish_hook(u)
        self.f[u] = self.time = self.time + 1

    def cycle_free(self):
        try:
            self.dfs()
            return True
        except CycleException:
            return False

    def topological_sort(self):
        list = []
        self.dfs(lambda u: list.append(u))
        list.reverse()
        return list

    def write_graphviz(self, f):
        f.write('digraph G {\n')
        for u in self.vertices():
            f.write(u)
            self.write_graphviz_vlabel(f, u)
            f.write(';\n')
        f.write('\n')
        for u in self.vertices():
            for v in self.adj(u):
                f.write(u + ' -- ' + v)
                self.write_graphviz_elabel(f, u, v)
                f.write(';\n')
        f.write('\n')
        f.write('}\n')

    def write_graphviz_vlabel(self, f, u):
        pass

    def write_graphviz_elabel(self, f, u, v):
        pass

