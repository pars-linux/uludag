#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import iso9660

import xml.etree.cElementTree as iks

#get as xml tree from string 
def getTree(item, level = 0):
    i = "\n" + level * "    "
    if len(item):
        if not item.text or not item.text.strip():
            item.text = i + "   "
        for e in item:
            getTree(e, level + 1)
            if not e.tail or not e.tail.strip():
                e.tail = i + "  "
        if not e.tail or not e.tail.strip():
            e.tail = i
    else:
        if level and (not item.tail or not item.tail.strip()):
            item.tail = i

#if none given
isoFolder = os.getcwd()

if len(sys.argv) > 1:
    isoFolder = sys.argv[1]
if len(sys.argv) > 2:
    print "usage : %s [Path]" % sys.argv[0]

treeString = ""

#get .iso file from directory
filelist=[file for file in os.listdir(isoFolder) if file.lower().endswith(".iso")]
if len(filelist) == 0:
    print "There is no ISO image file in '%s'" %isoFolder
    print "usage : %s [Path]" %sys.argv[0]
    sys.exit(1)

for files_name in filelist: 
        iso = iso9660.ISO9660.IFS ( source = isoFolder+"/"+files_name)
        name = iso.get_volume_id()
        print "ISO Image Name : %s" % name
        isopath = isoFolder +"/"+ files_name
        print "Path : %s" % isopath 
        
        isosize = os.path.getsize(isopath)/(1024*1024)
        print "Size : %s MB" %isosize
        version = "default"

        root = iks.Element("ISO9660")
        
        name_tag = iks.SubElement(root,"Name")
        name_tag.text = name

        version_tag = iks.SubElement(root,"Version")
        version_tag.text = version

        path_tag = iks.SubElement(root, "Path")
        path_tag.text = isopath

        size_tag = iks.SubElement(root,"Size")
        isosize = "%s MB" %isosize
        size_tag.text = isosize

        getTree(root)
        treeString += iks.tostring(root)
        treeString +="\n"
xmlfile = open("ISO Files.xml","w")
xmlfile.write(treeString)
xmlfile.close()
