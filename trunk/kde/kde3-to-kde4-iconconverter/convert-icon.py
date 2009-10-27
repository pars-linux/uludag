#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import shutil

if len(sys.argv) != 4:
    print "usage: %s old-icon-theme-dir new-icon-theme-name mapfile" % sys.argv[0]
    sys.exit()

oldthemedir = sys.argv[1]
oldthemename = os.path.basename(sys.argv[1])
newthemename= sys.argv[2]
newthemedir= os.path.join(os.getcwd(), newthemename)
mapfile = sys.argv[3]

os.mkdir(newthemedir)

groups = ["actions", "apps", "devices", "places", "mimetypes", "status", "categories", "emblems", "emotes"]
sizes = ["16x16", "22x22", "32x32", "48x48", "64x64", "128x128"]

for size in sizes:
    for group in groups:
        os.makedirs(os.path.join(newthemedir, size, group))
    for mapline in file(mapfile).readlines():
        if mapline.strip().startswith("#"):
            continue
        oldicon = mapline.split()[0].strip()
        newicon = mapline.split()[1].strip()
        try:
            shutil.copyfile(os.path.join(oldthemedir, size, oldicon), os.path.join(newthemedir, size, newicon))
        except:
            print "Icon %s not found in old icon theme, skipping..." % oldicon

indexfile = file(os.path.join(oldthemedir, "index.theme")).read()
indexfile = indexfile.replace("filesystems", "places")
indexfile = indexfile.replace("FileSystems", "Places")
indexfile = indexfile.replace("crystalsvg", "oxygen")
#TODO: change theme name and inherited theme name here
#indexfile = indexfile.replace(oldthemename, newthemename)

newindexfile = file(os.path.join(newthemedir, "index.theme"), "w")
newindexfile.write(indexfile)
newindexfile.close()

print "Do not forget to change theme name in index.theme file..."
