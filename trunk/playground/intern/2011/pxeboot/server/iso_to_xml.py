#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import iso9660
import bz2, pycdio
import xml.etree.cElementTree as iks
import piksemel
import urwid
import urwid.raw_display


class getMenu():

    def selectionmenu(self,filelist):
        palette = [
                ('header', 'black,underline', 'light gray', 'standout,underline',
                    'black,underline', '#88a'),
                ('panel', 'light gray', 'dark blue', '',
                    '#ffd', '#00a'),
                ('focus', 'light gray', 'dark red', 'standout')
                ]

        screen = urwid.raw_display.Screen()
        screen.register_palette(palette)

        listbox = urwid.SimpleListWalker([])
        editedList = []

        def focus(widget):
            return urwid.AttrMap(widget, None, 'focus')

        def selected_item (cb, state):
            if state==True:
                editedList.append(cb.get_label().split("          ")[0])
            else:
                editedList.remove(cb.get_label().split("          ")[0])

        def createCB(text,i):
            kilo = 1024*1024
            size = (os.path.getsize(os.path.join(isoFolder,text)))/kilo
            text = "%s          Size : %sMB" % (text, size)
            cb = urwid.CheckBox(text, False, has_mixed=False)
            urwid.connect_signal(cb, 'change', selected_item)
            return focus(cb)

        def click_ok(button):
            raise urwid.ExitMainLoop()

        blank = urwid.Divider()

        listbox.extend([
                    blank,
                    blank,
                    urwid.Padding(
                        urwid.AttrMap(
                            urwid.Text("Select Version",align='center'),'header'),
                            ('fixed left',35),('fixed right',35)),
                    blank,
                    blank
                 ])

        i = 1

        for files in filelist:
            listbox.extend([
                urwid.Padding(
                urwid.AttrMap(
                    urwid.Columns([
                        urwid.Pile([
                            createCB(files,i),
                            ]),
                        ]),'panel'),('fixed left',60),('fixed right',60)),
                blank
                    ])

            i = i + 1

        listbox.extend([
            urwid.Padding(
                urwid.GridFlow([
                    urwid.AttrWrap(
                        urwid.Button("OK", click_ok),
                                  'panel','focus')
                               ],10, 2, 2, 'center'),
                         ('fixed left',5), ('fixed right',5)),
                  ])

        def unhandled_input(key):
            if key in ('Q','q','esc'):
                raise urwid.ExitMainLoop()

        urwid.MainLoop(urwid.ListBox(listbox), screen=screen,
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
    return int( round ( x + 0.5 ) )

#Extracting 'pisi-index.xml' and 'gfxboot.cfg' from .iso
def extractData(local_filename):
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

    if local_filename == "repo/pisi-index.xml.bz2":
        data = bz2.decompress(a)
    else:
        for line in a.split("\n"):
            if line.lstrip().startswith("distro="):
                data = line.lstrip().split("=", 1)[1]

    return data


def parseXml():
    xmlStr = extractData("repo/pisi-index.xml.bz2")
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

if len(filelist) == 0:
    print "There is no ISO image file in '%s'" %isoFolder
    print "usage : %s [Path]" %sys.argv[0]
    sys.exit(1)

listObject = getMenu()

filelist = listObject.selectionmenu(filelist)

for files_name in filelist:
        iso = iso9660.ISO9660.IFS ( source = os.path.join( isoFolder,files_name ) )

        root = iks.Element("ISO9660")

        name = extractData("boot/isolinux/gfxboot.cfg")
        name_tag = iks.SubElement(root, "Name")
        name_tag.text = name

        if (name.find("x86_64") > 0):
            architecture = "x64"
        else:
            architecture = "x86"

        architecture_tag = iks.SubElement(root, "Architecture")
        architecture_tag.text = architecture

        isopath = os.path.join(isoFolder, files_name)
        path_tag = iks.SubElement(root, "Path")
        path_tag.text = unicode(isopath)

        isosize = parseXml()
        isosize = "%s" %isosize
        size_tag = iks.SubElement(root, "Size")
        size_tag.text = isosize

        getTree(root)
        treeString += iks.tostring(root)
        treeString += "\n"

xmlfile = open("pxeboot_iso_files.xml","w")
xmlfile.write(treeString)
xmlfile.close()
