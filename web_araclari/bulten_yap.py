#!/usr/bin/env python
# -*- coding: utf-8 -*-

#imports
import os
import sys

sys.path.append(os.getcwd())

import codecs
import time
import datetime
import PyRSS2Gen
from cgi import FieldStorage
from glob import glob
from os.path import basename
from time import ctime

from bulten_entry import Entry
from bulten_indexer import Index
from bulten_conf import *

def check_logs(index):
    logs=glob(LOGS+"/*"+log_prefix)
    # check if all are in index. If not add it.
    for log in logs:
	if not index.check(log):
	    index.add(log)

	    mtime =  index.get_mtime(log)
	    # date <- (year, month)
	    date = time.localtime(mtime)[:2]

    # sort the list using mtimes in the .index
    logs = index.sort_filelist(logs)
    return logs

def list_to_tuple(l):
    """gets a list and converts to tuple"""
    l = l.split(",")
    for i in range(len(l)): 
        l[i] = int(l[i])
    return tuple(l)

def comp_archive(x, y):
    if x[1] > y[1]: return -1
    elif x[1] > y[1]: return 0
    else: return 1

def gen_html(index, logs):
    global entry_count

    # Print the entries
    if not entry_count: 
	entry_count = len(logs)
    else:
	entry_count = int(entry_count)
	if entry_count > len(logs):
	    entry_count = len(logs)

    index_html = open("index.html", "w")
    index_html.write(header_text)
    index_html.write("<center> <p><b>Bülten Arşivi</b></p>")

    for i in range(entry_count):
	hname = Entry(logs[i]).html_name()
	title = Entry(logs[i]).title()
	# first add to index.html
	index_html.write("<a href=\"%s/%s\">%s</a><br>" 
			 % (ARCHIVE, hname, title))
		
	# then write to archive
	hfile = open(ARCHIVE+"/"+hname, "w")
	hfile.write(archive_header)
	hfile.write(Entry(logs[i]).content())
	hfile.write(footer_text)
	hfile.close()

    index_html.write("</center>")
    index_html.write(footer_text)
    index_html.close()


def gen_rss(index, logs):
    global entry_count
    rss_items = []

    if not entry_count: 
	entry_count = len(logs)
    else:
	entry_count = int(entry_count)
	if entry_count > len(logs):
	    entry_count = len(logs)


    for i in range(entry_count):
	file = codecs.open(logs[i], encoding="utf-8")

	# first line is title
        entry_title = file.readline()
        entry_link = "http://www.uludag.org.tr/bulten/arsiv/"+basename(logs[i])[:-3]+"html"
        entry_desc = file.read()
        mtime = index.get_mtime(logs[i])
        entry_date = ctime(mtime)
        # SACMALIK: tarih RFC822 standardinda yazilmali, fakat boye de yapilmaz :(
        t = entry_date.split()
        entry_date = " ".join([t[0]+",", t[2], t[1], t[4], t[3]+" GMT"])

        rss_items.append(PyRSS2Gen.RSSItem(
                title = entry_title,
                link = entry_link,
                description = entry_desc,
                guid = PyRSS2Gen.Guid(entry_link),
                pubDate = entry_date))

    rss = PyRSS2Gen.RSS2(
	title = "Uludağ Bülteni",
	link = "http://www.uludag.org.tr",
	description = "Uludağ Bülteni",
	lastBuildDate = datetime.datetime.now(),
	items = rss_items
	)
                                                                            
    rss.write_xml(open("bulten.xml", "w"))
    

if __name__ == "__main__":
    index = Index(index_file)
    logs = check_logs(index)

    gen_html(index, logs)
    gen_rss(index, logs)
