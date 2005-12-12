# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
#
# Author:  Eray Ozkural <eray@uludag.org.tr>

import pisi
import pisi.context as ctx

class Error(pisi.Error):
    pass

class Exception(pisi.Exception):
    pass

# API

from invertedindex import InvertedIndex
from preprocess import preprocess

def init(ids, langs):
    "initialize databases"
    
    assert type(ids)==type([])
    assert type(langs)==type([])
    
    ctx.invidx = {}
    for id in ids:
        ctx.invidx[id] = {}
        for lang in langs:
            ctx.invidx[id][lang] = InvertedIndex(id, lang)

def finalize():
    import pisi.context as ctx
    
    if ctx.invidx:
        for id in ctx.invidx.iterkeys():
            for lang in ctx.invidx[id].iterkeys():
                ctx.invidx[id][lang].close()
        ctx.invidx = {}    
    
def add_doc(id, lang, docid, str, txn = None):
    terms = preprocess(lang, str)
    ctx.invidx[id][lang].add_doc(docid, terms, txn)

def remove_doc(id, lang, docid, str, txn = None):
    ctx.invidx[id][lang].remove_doc(docid, txn)

def query_terms(id, lang, terms, txn = None):
    import preprocess as p
    terms = map(lambda x: p.lower(lang, x), terms)
    return ctx.invidx[id][lang].query(terms, txn)

def query(id, lang, str, txn = None):
    terms = preprocess(lang, str)
    return query(id, lang, terms, txn)
