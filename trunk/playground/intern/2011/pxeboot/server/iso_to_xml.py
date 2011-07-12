#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import iso9660
import bz2, pycdio
import xml.etree.cElementTree as iks
import piksemel
import urwid
import urwid.raw_display

def selectionmenu(filelist):
    palette = [
            ('header','black,underline', 'light gray', 'standout,underline',
                'black,underline', '#88a'),
            ('panel', 'light gray', 'dark blue', '',
                '#ffd', '#00a'),
            ('focus', 'light gray', 'dark red', 'standout',)
            ]
    screen = urwid.raw_display.Screen()
    screen.register_palette(palette)

    lb = urwid.SimpleListWalker([])

    radio_buttons = []
    editedList=[]
    def focus(widget):
        return urwid.AttrMap(widget, None, 'focs')

    def selected_item (rb, state, rb_id):
        if state:
            editedList=rb.label
            return editedList 

    def rb_state(text, rb_id, state=False):
        rb=urwid.RadioButton(radio_buttons,text,state)
        urwid.connect_signal(rb,'change',selected_item,rb_id)
        return focus(rb)
        def click_exit(button):
            raise urwid.ExitMainLoop()
    def click_exit(button):
        raise urwid.ExitMainLoop()

    lb.extend([
        urwid.AttrMap(urwid.Text("Select Version"),'header')])
    i=1
    for files in filelist:
        lb.extend([urwid.AttrMap(
            urwid.Columns([
                urwid.Pile([
                    rb_state(files,i)]),]),'panel')])
        i=i+1

    lb.extend([urwid.AttrMap(
        urwid.Columns([
            urwid.Pile([
                focus(urwid.Button("Exit",click_exit)),
                ])
            ]),'panel')
        ])
    def unhandled_input(key):
        if key in ('Q','q','esc'):
            raise urwid.ExitMainLoop()
    urwid.MainLoop(urwid.ListBox(lb), screen=screen,
        unhandled_input = unhandled_input).run()
    return editedList

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

def ceil(x):
    return int(round(x+0.5))

#Extracting pisi-index.xml from .iso
def extractIndex():
    local_filename = "repo/pisi-index.xml.bz2"
    statbuf = iso.stat (local_filename,True)
    if statbuf is None:
        print "Couldn't get ISO-9660 file information for file"  %local_filename
        iso.close()
        sys.exit(1)
    a = ""
    blocks = ceil(statbuf['size'] / pycdio.ISO_BLOCKSIZE)
    for i in range(blocks):
        lsn = statbuf['LSN'] + i
        size, buf= iso.seek_read (lsn)
        a += buf

        if size <= 0 :
            print "Error reading ISO 9660 file %s at LSN %d" % (local_filename, lsn)
            sys.exit(1)
    data = bz2.decompress(a)
    return data

def parseXml():
    xmlStr = extractIndex()
    doc = piksemel.parseString(xmlStr)
    a = 0
    for tags in doc.tags("Package"):
        size = int(tags.getTagData("InstalledSize"))
        a += int(size)
    return a


#if none given
isoFolder = os.getcwd()

if len(sys.argv) > 1:
    isoFolder = sys.argv[1]
if len(sys.argv) > 2:
    print "usage : %s [Path]" % sys.argv[0]

treeString = ""

#get .iso file from directory
filelist=[files for files in os.listdir(isoFolder) if files.lower().endswith(".iso")]
filelist=selectionmenu(filelist)
if len(filelist) == 0:
    print "There is no ISO image file in '%s'" %isoFolder
    print "usage : %s [Path]" %sys.argv[0]
    sys.exit(1)

for files_name in filelist: 
        iso = iso9660.ISO9660.IFS ( source = os.path.join(isoFolder,files_name))
        name = iso.get_volume_id()
        print "ISO Image Name : %s" % name
        isopath = os.path.join(isoFolder,files_name)
        print "Path : %s" % isopath

        isosize = parseXml()
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
        isosize = "%s " %isosize
        size_tag.text = isosize

        getTree(root)
        treeString += iks.tostring(root)
        treeString +="\n"

xmlfile = open("ISO Files.xml","w")
xmlfile.write(treeString)
xmlfile.close()
