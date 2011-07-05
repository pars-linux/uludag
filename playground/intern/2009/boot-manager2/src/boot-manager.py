#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

import sys
import copy,string

from qt import *
from kdecore import *
from kdeui import *


import dbus.mainloop.qt3

from khtml import *

import locale
import os
import os.path


import dbus
import time
from handler import CallHandler

BOOT_ACCESS, BOOT_ENTRIES, BOOT_SYSTEMS, BOOT_OPTIONS, BOOT_SET_ENTRY, \
BOOT_SET_TIMEOUT, BOOT_UNUSED, BOOT_REMOVE_UNUSED, BOOT_REMOVE_UNUSED_LAST = xrange(1, 10)
image0_data = \
    "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
    "\x49\x48\x44\x52\x00\x00\x00\x20\x00\x00\x00\x20" \
    "\x08\x06\x00\x00\x00\x73\x7a\x7a\xf4\x00\x00\x05" \
    "\x73\x49\x44\x41\x54\x58\x85\xed\x96\x5d\x6c\xd4" \
    "\x55\x1a\xc6\x7f\xe7\xe3\x3f\x33\x65\x98\xcf\xd2" \
    "\xd2\x25\x5d\xda\x80\x42\x45\xfc\x6a\x05\x35\x44" \
    "\xbb\x91\xb6\x9b\x18\x5d\x8d\xa0\xe2\xba\x09\x9b" \
    "\x28\x1b\x03\x26\xea\x85\xc4\x5d\x8d\x2e\x26\x92" \
    "\x10\x75\x37\xc6\xa4\x31\x66\xcd\x62\x8c\xa0\x5e" \
    "\x2c\x18\x8d\x59\xa5\xa5\x6a\xa3\x01\x5a\xe9\x44" \
    "\x10\x94\x40\xa7\x20\x94\xc2\x74\x3a\x33\x9d\x76" \
    "\x3e\xfe\x33\xf3\x3f\x5e\x4c\xad\x24\x98\x76\xb8" \
    "\x30\xde\xf0\x5c\x9d\x8b\x37\xef\xf3\x9c\xe7\x3c" \
    "\xe7\x3d\x07\x2e\xe3\x32\x7e\x63\x88\x4b\x29\x6e" \
    "\xbc\x13\xc6\x52\x88\x65\x8b\xf5\xd2\x9a\x50\xcd" \
    "\x4a\xb7\x55\x15\x04\x43\xde\xce\x26\x62\x89\xd1" \
    "\x03\x03\xdf\x17\x8f\xcd\x0f\x63\x4e\x7d\xfc\x2b" \
    "\x08\x68\xfd\x9b\x9b\xe8\x70\x5e\xad\xb8\xaa\x71" \
    "\x43\x6b\xcb\xbd\x7f\x6f\x69\xba\xbd\x7e\xee\x9c" \
    "\x80\xc4\x40\x3a\x93\x74\xfa\x8f\x76\x9d\xfa\xfc" \
    "\xe0\xae\x17\xf7\x1f\x3a\xf5\xdf\x25\x0d\xee\xd2" \
    "\x67\x6f\xe4\x2b\xea\xab\x2a\x29\xea\xd8\xe4\xc7" \
    "\xef\x0d\x13\xf4\xa9\x3f\xae\x59\xfd\x58\xe7\x5f" \
    "\xee\xd8\x5c\x87\x65\x44\xda\x8e\xe3\xc8\x02\x75" \
    "\xb5\x0d\xe2\xd6\xeb\xee\x09\xda\x85\xdc\xaa\x58" \
    "\x32\xd2\xef\xad\xf2\x47\x1b\x9a\x25\x27\xfa\x66" \
    "\x17\xa1\x2b\x92\x69\x60\xf7\x2b\xa7\xc5\xa6\x6d" \
    "\xad\xf7\xb5\xad\x5c\x17\x1a\x88\xee\xe5\xad\x9e" \
    "\xe7\xc9\x95\x26\x51\x4a\x31\xd7\x1b\x62\xfd\x6d" \
    "\x5b\x68\xbf\xe9\xcf\xd5\xfd\x47\xba\xd6\xbe\xfe" \
    "\x8f\x2f\xbb\xdb\x37\x06\x2a\x6a\x2d\x2b\xaa\x02" \
    "\xb8\x01\x77\xd8\x5f\xd7\xe8\xf7\x86\x89\x44\x7b" \
    "\x48\xe7\xc7\x10\x52\x80\x82\xb4\x1d\xe7\xf0\x99" \
    "\x5e\x02\x73\xab\x09\xfa\x6a\x1b\x59\x84\xab\xd2" \
    "\xc3\x9d\xd9\x81\x65\x40\x02\xf9\xe9\x57\xe3\x2e" \
    "\x65\xe1\x35\xc6\xd1\x08\x70\x44\x09\xa5\x35\x52" \
    "\x4b\x94\x56\x18\x29\x71\x84\x03\x80\xe3\x94\x2c" \
    "\x02\x78\xf7\x7c\x99\x92\xd4\x61\xe3\xc7\xe1\xd8" \
    "\x25\x0a\x68\x7e\x08\x92\x69\xf4\x95\x0b\xc3\x6d" \
    "\x8b\xeb\x97\xaf\xab\x0e\xd4\x2d\x74\x1c\x47\x2f" \
    "\xa8\x59\x74\x8d\x56\x16\x52\x4a\xa4\x96\x48\xad" \
    "\x90\x4a\x62\x94\x41\x4a\x81\xa5\x5d\xd4\xcf\xbf" \
    "\xa2\xf9\x99\x47\xd6\x7e\x20\x84\x2c\xc4\x53\xc3" \
    "\x27\x4f\x9c\xfe\x76\xe7\xb1\xa5\x89\xbd\x61\x3f" \
    "\xa5\x83\xef\x54\x20\xa0\x6d\xa3\x8f\xae\xce\x34" \
    "\xf7\x3e\xd5\xb0\xe1\x4f\xb7\x6d\xd8\xda\x7e\xd3" \
    "\x83\x41\xdf\x9c\x50\xb9\x58\x5b\x58\xda\x0d\x52" \
    "\xa0\x94\x42\xa9\xb2\x08\x94\x01\x29\x70\xbb\xaa" \
    "\x78\xe4\x9e\x2d\xa1\x62\xa9\x70\x2b\x40\x2a\x1d" \
    "\x67\xcf\xfe\x1d\x77\x7f\xd8\xfb\x9f\xcd\xbb\x5e" \
    "\xfe\xe1\xcd\xf6\x8d\x3e\xf6\x74\xa6\x67\x16\x20" \
    "\x85\xe2\x96\xbf\xd2\xf4\x87\x96\x35\x9b\xd7\xae" \
    "\x7e\x2c\x18\x89\xf6\x10\x19\xea\xc1\xa1\x84\x54" \
    "\x12\x24\x0c\x8d\x1e\x42\x59\x56\xd9\x01\x2d\x11" \
    "\x4a\x32\x94\xfc\x86\xb7\x07\x9e\x47\xaa\xb2\x2b" \
    "\x5a\x5b\x2c\xab\x59\xc5\x7d\xed\x8f\x87\x93\x13" \
    "\xa3\x4f\x9f\x59\xff\xda\xe7\x42\xc8\xe3\xb3\x3a" \
    "\xe0\x9b\x13\xc0\xe3\xaa\xba\xb1\xe5\xaa\xd5\x0b" \
    "\x47\x52\x43\x6c\xdf\xfb\x1c\xe9\xfc\x18\xca\xd2" \
    "\xa8\x29\x42\x6d\x59\x68\x4b\x23\x95\x2c\x13\x6a" \
    "\x49\xd2\x3e\x4f\xe4\x5c\xf7\x54\x8d\x42\x48\xc1" \
    "\xf1\xe4\xd7\x3c\x7c\xed\x4b\xb4\x34\xdd\xde\xd8" \
    "\x7d\xe0\xbd\x66\xad\xac\xe3\x90\x9a\x59\x40\x95" \
    "\xc7\x87\xc8\x4f\x86\xbc\x1e\x9f\x8c\xa7\x87\xc9" \
    "\x95\x26\x71\xb9\xdc\x48\xad\xa6\x9b\x4b\xfd\x13" \
    "\xb1\x9a\xce\x82\xba\x60\x2d\x55\xf9\x72\x65\x8b" \
    "\x13\xa4\xec\x18\x5e\x8f\x5f\xbb\x2c\x4f\xd0\x6d" \
    "\x79\x66\xcf\xc0\x85\x10\x42\x20\x95\x44\x28\x71" \
    "\x01\x81\xbc\x80\x78\x8a\x5c\xc9\x9f\xdd\x50\x12" \
    "\x21\x04\xc6\x98\x99\x5a\x4f\xe3\xa2\x39\x90\xc9" \
    "\xa5\xc9\x17\x72\x63\x13\xd9\x94\x53\x13\xa8\xc7" \
    "\xe7\x0d\x61\xa4\x83\x91\x06\x23\x0d\x48\x83\x54" \
    "\x62\x9a\x4c\x4e\x05\x51\x68\x01\xd2\xe0\x98\x12" \
    "\x25\xa7\x88\x63\x8a\xcc\xb1\xfc\x04\xdd\xb5\x4c" \
    "\x64\x53\x45\xbb\x90\x4d\x64\xf3\x93\xb3\x3b\x30" \
    "\x91\x49\x32\x3e\x99\xea\xeb\x3f\xd2\x35\x74\xdd" \
    "\x92\x2d\x8b\xd6\xb7\xbe\xc0\xe1\x33\xbd\x18\xe1" \
    "\x20\xa4\x44\x48\x41\x34\xf9\x0d\xc9\xfc\xb9\x69" \
    "\xeb\x85\x12\xcc\xf3\xd6\xd3\x18\x58\x0e\xa2\x3c" \
    "\x81\x94\xd0\x34\x55\xdf\xcc\x5c\x11\xa6\xff\x68" \
    "\xf7\x60\x2c\x11\xfb\x3a\xe8\xbb\x78\x3a\x5e\x24" \
    "\xc0\x18\x87\x7d\xdb\x39\xf6\xbb\x79\xbb\xb6\xfa" \
    "\xbd\xe1\x6d\x6d\x2b\xd7\x55\x2f\xbd\x61\x05\x08" \
    "\xd0\xca\x85\xdb\x55\xc5\xdb\x07\x9f\x23\x32\x72" \
    "\x6e\x2a\x0b\x12\x94\xa1\x21\x70\x35\x6b\x97\x6c" \
    "\x26\x67\x67\x28\x96\x6c\x30\x90\x48\xc7\xd8\xf9" \
    "\xc5\xbf\x46\x7b\x07\x76\x6f\xdd\xff\x96\x19\x6c" \
    "\xdf\x54\x81\x80\x3d\x9d\x69\xae\x7f\x10\xfa\xbe" \
    "\x3d\xb5\x7d\x32\xf3\xef\xe8\xfe\xc3\x9f\x3c\x10" \
    "\xf6\xcf\x6f\x70\x4c\xc9\xaa\x9f\x7f\xe5\xf5\x0f" \
    "\xdf\xfd\xcf\xf0\x4f\x01\x54\x53\x37\xc0\xc1\x41" \
    "\x08\x41\xce\xce\xf0\xc6\xff\x9e\x8d\x8f\xc4\x4f" \
    "\x46\x84\x90\xc5\xb1\xd4\xc8\x50\x74\xf8\xc8\xbb" \
    "\xdf\x0d\xa5\xbe\x68\x7e\x48\x30\xb0\xe3\xe2\x0c" \
    "\xfc\x62\x08\x23\x3b\x01\x28\x9d\x0e\x25\xf7\x52" \
    "\xf8\xaa\x87\x10\x9a\x10\xde\x67\x1f\xbd\x7f\x77" \
    "\xb1\x54\x68\x15\x52\x4c\x87\x10\x21\x60\x2a\x6f" \
    "\x85\xa2\xcd\x48\xfc\xe4\xc0\xb6\xce\x0f\xd6\x90" \
    "\x21\xc7\x28\x05\x34\x86\x71\xf8\xe1\x97\x88\x98" \
    "\xed\x31\x4a\x00\x13\x98\x8e\xbb\xfc\x05\x24\x39" \
    "\x21\x28\x62\x40\x6b\x17\x42\xc9\xe9\xf3\x06\x83" \
    "\x12\xe5\xbd\x08\x21\x8a\xd8\xe4\xda\xef\x0a\xd8" \
    "\x64\xca\xe4\x33\xa1\xa2\xd7\xd0\x08\x01\x11\xf2" \
    "\xf1\xd4\x48\x34\x35\x11\xe7\xea\xda\x55\x04\x3c" \
    "\xf3\x90\x42\x21\x85\xc2\xef\xae\xa1\xa9\xfa\x16" \
    "\x92\xe3\x31\x12\xe3\xe7\x07\xcd\x09\x63\x57\xfa" \
    "\xd3\xa9\xa8\xae\x6d\x63\x00\xaf\xc7\x4b\x36\x9f" \
    "\x69\x7f\xa0\xe3\x89\x9d\xeb\x3a\x9e\xac\x1e\x77" \
    "\x46\x49\xe5\x63\x00\x04\xdc\xb5\xf8\x44\x98\x1d" \
    "\xff\x7f\x39\xf6\x7e\xd7\xab\xf7\x7b\x5c\xde\xcf" \
    "\x0a\x76\x86\x4f\x3a\x67\xd9\x3e\x15\xfe\x88\x06" \
    "\xfb\xf2\xd4\x2d\xb7\x39\x1a\x9d\x3c\x99\xcd\x0d" \
    "\x9e\x1f\x4d\x9e\xbd\xc6\x65\xaa\xfc\xe4\x95\xb4" \
    "\x27\x0a\x9c\x3d\x1b\x2d\x7d\xd8\xfb\xe6\x89\xee" \
    "\x03\xef\x3d\xb3\xef\xd0\xe8\x47\x21\x7f\xc1\x74" \
    "\xbf\x9e\xa9\xa4\xf5\xa5\x7d\x4a\x17\x74\xc0\xd9" \
    "\xf3\x88\x15\xd7\xaa\xc5\x35\xa1\xf0\x8d\x6e\xab" \
    "\x2a\x00\x90\xb3\xb3\x89\x58\x32\xde\xdf\xb7\xcf" \
    "\x89\x2e\xf8\x3d\x66\xb8\xfb\x52\xba\x5e\xc6\x65" \
    "\xfc\xc6\xf8\x11\xc6\xa7\x0c\x89\x46\x6b\xa2\xe9" \
    "\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82"
image1_data = \
    "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
    "\x49\x48\x44\x52\x00\x00\x00\x20\x00\x00\x00\x20" \
    "\x08\x06\x00\x00\x00\x73\x7a\x7a\xf4\x00\x00\x02" \
    "\x8c\x49\x44\x41\x54\x58\x85\xed\x94\xcb\x4f\x53" \
    "\x41\x14\xc6\xbf\x99\xb9\x7d\x40\xbd\x7d\x81\x01" \
    "\x15\x41\x34\x1a\x24\x24\x1a\x50\x12\x13\x13\x0d" \
    "\xd0\x3f\xc0\x57\xc4\xb8\x50\xa3\x1b\x1f\x89\x2e" \
    "\x7c\xac\x5c\x90\x10\x12\x37\x6e\xdc\xb9\x20\xb8" \
    "\x50\x71\xa5\xc6\x95\xc6\x1a\x83\x1b\x51\x84\x85" \
    "\x11\x15\xcb\x43\x94\x42\x80\xf6\xf6\xb6\xb7\x5c" \
    "\x68\xbd\x33\x2e\x2a\x8f\xd2\xda\x96\x35\xf7\x97" \
    "\x9c\xdc\x99\x33\x99\x73\xbe\x7b\xce\xc9\x00\x26" \
    "\x26\x26\x26\xeb\x1d\x92\xf3\xb4\x16\x80\x02\xca" \
    "\x36\xc3\xc6\xac\x20\x10\x85\x47\x35\x12\xe0\xc6" \
    "\x04\x12\x70\x82\x63\x68\x8d\x02\xea\x4f\x03\x91" \
    "\x18\xa4\x9d\x95\xde\x96\x1d\x15\x75\xad\x25\xae" \
    "\xf2\x4a\x42\x28\x2d\x30\x3d\x00\x80\x73\x6e\x84" \
    "\xd4\xe0\xcf\xe1\xdf\x5f\x1e\x0f\x8d\x2b\x6f\xbc" \
    "\x4e\x18\xfd\x0f\x0b\xb8\xe8\xbb\x24\x03\x00\x8e" \
    "\xde\xa8\xba\xd8\xf5\xa2\x5d\x99\x98\x1e\x16\x51" \
    "\x2d\x5c\x98\xc5\x57\x98\x16\x16\xbf\xa6\x7e\x88" \
    "\xce\xe7\x6d\xa1\x23\xd7\xb7\x5e\x58\x19\x7b\x25" \
    "\x52\x46\x49\x08\xc3\x81\xb3\xa8\x39\xdc\x70\xec" \
    "\xe6\xf1\xe6\x2b\xee\xfe\x80\x1f\xfd\x01\x3f\x0c" \
    "\x61\x80\x10\x02\x42\x91\xfa\x12\x02\x2c\xae\x29" \
    "\x59\xf2\x11\x4a\x00\x42\x20\x49\x16\xec\xad\x6a" \
    "\xc2\x09\xdf\x55\x6f\x44\x9b\xbd\x35\x71\xe6\xde" \
    "\x5b\x42\x68\x20\xaf\x00\xb9\xd8\x05\xbb\xb5\x68" \
    "\x5f\xc3\xee\xe6\xca\x49\x65\x14\x9d\xaf\x6e\x23" \
    "\xaa\xcf\x82\x52\x9a\x4a\xb4\x68\x8c\x82\x2e\xed" \
    "\x17\xd7\x74\xe9\x8c\x10\xe0\xfb\x74\x2f\xae\xf9" \
    "\xee\xa3\xa1\xa6\x69\x9b\xff\xc3\x93\x7a\x89\x59" \
    "\x02\x80\x9a\x5b\x40\x91\x5d\x06\x59\x88\x7b\x1c" \
    "\x76\x99\x86\x62\x41\xcc\x1b\x1a\xac\x36\xdb\xaa" \
    "\x44\xcb\xc9\x28\xa5\x20\x2c\xbb\x90\x79\x31\x87" \
    "\x88\x3e\x0d\x47\x91\x53\xb2\x5a\xec\x6e\x9b\xc5" \
    "\x9e\xbf\x05\x69\xed\xa0\x04\x4c\x62\x00\x11\x59" \
    "\xfe\x9c\x66\x26\x65\xe9\x22\x19\x63\xa9\x56\xe5" \
    "\x20\x63\xb2\xe7\xf4\x18\x16\x92\xf3\x61\x4d\x57" \
    "\xf9\x46\x57\x05\xe4\x0d\x1e\x08\xc6\x01\xf6\x4f" \
    "\x2e\x4b\x37\xc2\x44\xca\x2f\x89\xe5\x3d\x03\xc0" \
    "\x04\xe4\x62\x0f\x3c\x8e\x72\x68\x73\xea\x9f\x44" \
    "\x52\x57\xf4\x85\x78\xfe\x0a\x68\x7a\x04\xd1\xb8" \
    "\xfa\xb1\x6f\xf0\xf5\xd8\xf9\x5d\x6d\xdb\xcf\x35" \
    "\xb7\xe3\xf3\x78\x0f\x38\x8c\xb4\x81\xc3\x7f\x86" \
    "\x2f\xe5\x03\x18\xb3\xa0\xae\xec\x20\x64\x56\x8a" \
    "\xbe\xaf\xfe\x91\x19\x65\xe6\x93\x5b\x76\xe5\x17" \
    "\x20\x04\xc7\xfb\x2e\x0c\x6d\x2a\x7d\xda\xe1\x74" \
    "\x78\xef\xb4\x34\xb6\x96\xd4\xec\x6f\xcc\xf7\x64" \
    "\xad\x82\x00\x42\x40\x89\xcd\xa0\xfb\xe5\xdd\xd9" \
    "\x77\x03\xcf\x3a\x7a\x1f\x88\x11\xdf\xe5\x4c\x01" \
    "\x59\xc3\xee\x39\x05\x84\x22\x60\xb5\xd5\xee\x43" \
    "\xd5\x5b\x6a\x4f\x7a\x9d\x65\x55\xa9\x87\xa8\xf0" \
    "\xa7\x90\x0b\xce\xc3\xea\xd4\xd8\x68\x70\xb0\xfb" \
    "\xdb\x98\xda\x53\xea\x06\x1f\x78\x94\x55\x6a\x0e" \
    "\x3c\x00\x92\x20\x28\x83\x05\xd6\xb5\xd5\x00\x09" \
    "\x08\x4c\x22\x09\x09\x02\xd1\x35\xdd\x34\x31\x31" \
    "\x31\x59\x67\xfc\x05\x2d\x0e\x03\x07\x38\x49\xf1" \
    "\x4d\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60" \
    "\x82"
image2_data = \
    "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
    "\x49\x48\x44\x52\x00\x00\x00\x30\x00\x00\x00\x30" \
    "\x08\x06\x00\x00\x00\x57\x02\xf9\x87\x00\x00\x09" \
    "\x71\x49\x44\x41\x54\x68\x81\xed\xd9\x6b\x4c\x5b" \
    "\xd7\x01\x07\xf0\xff\x7d\xd9\x3c\x8c\xf1\x0b\x08" \
    "\x94\x84\xf7\xc3\x34\x10\xb0\x31\x34\x29\x79\x54" \
    "\x4b\x3a\x2d\x6b\x9b\x44\x8d\x48\x53\x92\x35\x4b" \
    "\xa7\x48\x95\x5a\x91\xaa\xda\xa4\xa9\xea\xba\x65" \
    "\x8d\xd6\x6c\xaa\xb4\x96\xad\x52\xd2\x4e\x28\x6b" \
    "\xa0\x2d\x49\xd1\x54\x2a\x56\xad\x42\x7d\xa8\x6b" \
    "\x35\x1a\xca\x9c\x40\x78\x98\x18\x42\x79\x18\xe3" \
    "\xd7\x35\x36\xbe\xf6\x7d\x9c\x7d\x20\x46\x50\xb5" \
    "\x51\xfa\xe0\x51\x69\x7f\xe9\x7c\xf1\x3d\xf7\xdc" \
    "\xf3\xf3\xb9\xf7\x1c\xfb\x5c\x8a\x10\x82\x1f\x72" \
    "\xe8\xb5\xee\xc0\x77\xcd\xff\x01\x6b\x1d\xf6\x76" \
    "\x2a\x55\x57\x57\x73\x3a\x9d\xae\xda\x62\xb1\x94" \
    "\x64\x65\x65\x99\x38\x8e\x53\x35\x37\x37\x77\xf4" \
    "\xf4\xf4\x5c\x23\x84\xc8\x2b\xdd\xc9\x5b\x86\x10" \
    "\xf2\xb5\xa5\xbc\xbc\x5c\xdf\xdc\xdc\xfc\x97\x89" \
    "\x89\x89\x59\x45\x21\x0a\x59\x12\x59\x96\x15\x97" \
    "\xcb\xe5\x7f\xfd\xf5\xd7\x5f\xb3\x5a\xad\xa9\xb7" \
    "\x6a\x67\x25\xcb\x2d\x0f\xda\x6c\xb6\x3b\x2f\x5d" \
    "\xba\xd4\xed\xf3\xf9\x14\x9f\xcf\x47\x02\x81\x00" \
    "\x09\x87\xc3\xe4\xcb\x71\x3a\x9d\x53\x07\x0e\x1c" \
    "\xd8\xba\xee\x00\x00\x68\x9b\xcd\x96\x7f\xf4\xe8" \
    "\xd1\xdf\x0f\x0f\x3b\x82\x33\x33\x33\x24\x5e\xfc" \
    "\x7e\x3f\x11\x45\x71\x11\x21\x08\x42\xec\xd8\xb1" \
    "\x63\xfb\xd7\x15\x20\x5e\x2a\x2a\x2a\x92\x2d\x16" \
    "\xcb\x8f\x2f\x5c\xb8\xf0\xe9\xcc\xcc\x8c\xe2\x72" \
    "\xb9\x16\x21\x3c\xcf\x2f\x22\x3c\x1e\xef\x9c\xd5" \
    "\x6a\x2d\x58\x77\x80\x9b\xa3\x41\x55\x56\x56\xe6" \
    "\x1e\x3a\x74\xe8\xcc\xf4\xf4\x34\x99\x9e\x9e\x26" \
    "\x71\x88\xdf\xef\x5f\x44\x74\x76\x76\x76\x01\xa0" \
    "\x56\x0b\x70\xdb\xd3\x28\x21\x84\xf4\xf6\xf6\x8e" \
    "\x0d\x0f\x0f\x77\xca\xb2\x22\xc9\xb2\x0c\x45\x51" \
    "\x40\x08\x41\x2c\x16\x03\xcf\xf3\x00\x80\x9d\x3b" \
    "\x77\xd6\x59\xad\xd6\xfc\x95\x98\x70\xbe\x2a\xdf" \
    "\x78\x1d\x50\x14\xc5\x33\x3f\x1f\x8e\xc6\x01\x71" \
    "\x44\x34\x1a\x45\x24\x12\x41\x52\x52\x92\xaa\xa0" \
    "\xa0\x60\xe7\x4a\x74\xf6\xab\xf2\x8d\x01\x2c\xcb" \
    "\xfa\xe6\xe6\xe6\xe6\x15\x45\xc1\xd2\x51\x20\x84" \
    "\x20\x1c\x0e\x03\x00\x2c\x16\xcb\xb6\xef\xbd\xa7" \
    "\x5f\x93\x65\x80\xba\xba\xba\x94\xea\xea\x6a\xee" \
    "\x56\x27\xd8\x6c\xb6\xe3\x26\x93\xc9\xb4\x74\x04" \
    "\x14\x45\x01\x00\x28\x8a\x82\xf9\xf9\x79\x68\xb5" \
    "\x5a\x23\x45\x51\xd4\x0a\xf6\x7b\x31\xcb\x00\x85" \
    "\x85\xc5\x8d\xe7\xce\x9d\x1b\x7c\xe2\x89\x27\x1a" \
    "\x6b\x6b\x6b\x8d\x5f\xae\xbc\x6b\xd7\xae\xed\x4f" \
    "\x3e\xf9\xe4\xd3\x91\x48\x84\x5a\xda\xf9\xa5\xb7" \
    "\x92\x20\x08\x50\x14\x45\x22\x37\x9f\xfc\x15\xcf" \
    "\xd2\x27\xba\xaa\xaa\xea\x27\xd1\x68\x54\x92\x65" \
    "\x99\xdc\xb8\x31\xee\x7b\xf1\xc5\xa6\x57\xad\x56" \
    "\x6b\xe9\xcd\xa9\x34\xfd\xbd\xf7\xba\x1c\x7d\x7d" \
    "\x7d\xe4\xda\xb5\x6b\x64\x68\x68\x88\x8c\x8c\x8c" \
    "\x90\xd1\xd1\x51\xd2\xd7\xd7\x47\x26\x27\x27\x89" \
    "\xcb\xe5\x22\x6e\xb7\x9b\x8c\x8e\x8e\xfa\xea\xea" \
    "\xea\xf4\xab\x3e\x0b\x31\x0c\xe3\x1c\x18\x18\x72" \
    "\x4b\x92\x84\x0d\x1b\x32\xf4\x27\x4e\xfc\xe2\xd1" \
    "\x8e\x8e\x0e\x7b\x6b\x6b\xeb\x87\x0d\x0d\x0d\x67" \
    "\xb3\xb2\x36\x14\x7e\xf9\xe1\xbd\x7a\xf5\x2a\x4e" \
    "\x9d\x3a\x85\xb7\xde\x7a\x6b\xf1\xb3\x4d\x9b\x36" \
    "\xe9\x1b\x1a\x1a\x9a\x57\xe3\x36\x5a\x06\xa0\x69" \
    "\xda\xf3\xce\x3b\x6f\x7f\x10\x8b\xc5\x20\x8a\x22" \
    "\x64\x59\x86\x56\xab\x55\x95\x94\x94\x6c\xde\xbf" \
    "\x7f\xff\xfd\x82\x20\x2c\x5d\x17\xe0\xf1\x78\x70" \
    "\xfe\xfc\x79\x50\x14\x05\x9f\xcf\x87\xa6\xa6\x26" \
    "\x00\x80\x2c\xcb\x68\x68\x68\xb8\x6f\xcf\x9e\x3d" \
    "\x07\x57\x15\xd0\xdd\xdd\xed\x6b\x6f\x6f\x7f\xb5" \
    "\xbb\xfb\x33\xaf\x28\x8a\x10\x45\x11\x1e\x8f\x47" \
    "\x62\x59\x96\xe1\x79\x9e\x89\xd7\xa3\x28\x0a\x84" \
    "\x10\x34\x35\x35\x81\x61\x18\x98\xcd\x66\x38\x1c" \
    "\x0e\xb0\x2c\xbb\x78\x3c\x25\x25\x85\x39\x7d\xfa" \
    "\xf4\x5f\x6b\x6a\x6a\x56\x74\x4d\x58\x06\x20\x84" \
    "\x10\x49\x92\xfe\xd3\xd4\xf4\xd2\x33\x3d\x3d\x3d" \
    "\x91\x48\x24\x82\x2b\x57\xae\x4e\x29\x8a\x92\xca" \
    "\x30\x0c\x68\x9a\x06\x4d\xd3\xa0\x28\x0a\x34\x4d" \
    "\x23\x2b\x2b\x0b\x15\x15\x15\x70\x38\x1c\x48\x4c" \
    "\x4c\xc4\xf1\xe3\xc7\x01\x60\x11\x62\xb3\xd9\xd2" \
    "\x1a\x1b\x1b\x5b\xf7\xee\xdd\xab\x5e\x29\x00\xf5" \
    "\x55\x93\xc5\xf6\xed\xdb\xf5\x1a\x8d\xe6\xd8\x3d" \
    "\xf7\xdc\xf3\xf3\x7d\xfb\xf6\x6d\x16\x04\x81\x02" \
    "\x16\xbe\xd9\x38\x84\x61\x18\x30\x0c\x83\xae\xae" \
    "\x2e\x7c\xf4\xd1\x47\x38\x79\xf2\x24\x36\x6e\xdc" \
    "\x08\x86\x61\x60\x32\x99\x16\xdb\x92\x24\x09\x2f" \
    "\x3f\xf5\xd4\xdf\x12\x04\xe1\xb1\x13\x67\xcf\x8a" \
    "\xab\x02\x00\x80\xaa\xaa\x2a\x1d\xc7\x71\x3f\xdd" \
    "\xb6\x6d\xdb\x83\x77\xdf\x5d\xb7\x35\x2f\x2f\x2f" \
    "\x83\xe3\x58\x8a\xa6\xe9\xc5\x05\x8c\xe3\x38\xa4" \
    "\xa6\xa6\x82\xa6\x69\xb0\x2c\x0b\x9a\xa6\xa1\x52" \
    "\xa9\xa0\xd3\xe9\x16\xdb\xf9\xec\xe2\x45\xa9\xf7" \
    "\xf1\xc7\x91\x63\x36\x7f\xea\x36\x18\x0e\x1e\x6d" \
    "\x6f\x77\xaf\x0a\x00\x00\x28\x8a\xa2\xad\x56\x6b" \
    "\x36\x80\x72\xa3\xd1\xb8\xf3\xc8\x91\x23\x0f\x25" \
    "\x24\x24\x24\x0d\x0e\x0e\x7a\x7b\x7b\x7b\x3f\x2c" \
    "\x2d\x2d\xad\xa8\xaa\xaa\x32\x17\x15\x15\x69\xd3" \
    "\xd3\xd3\xc1\xb2\x2c\x74\x3a\x1d\x54\x2a\x15\x00" \
    "\xa0\xff\xdd\x77\x95\x0f\x1a\x1a\x14\x5a\x96\x59" \
    "\x02\x20\xbf\xac\x6c\x4c\xda\xb0\x61\xff\x7d\xed" \
    "\xed\xf6\x55\x01\x2c\x81\x50\xb5\xb5\xb5\x85\x67" \
    "\xce\x9c\xf9\x40\xaf\xd7\x67\x75\x75\x75\x0d\xb7" \
    "\xb4\xb4\xec\x62\x59\x56\x23\xcb\x72\x75\x4e\x4e" \
    "\xce\x8f\xee\xba\xeb\xae\x9d\xbb\x77\xef\xce\x2f" \
    "\x2f\x2f\xa7\x19\x86\x81\xf3\xe3\x8f\xc9\xe7\x8f" \
    "\x3e\x2a\x27\xa9\xd5\x2c\xaf\x28\xf0\x4c\x4f\x83" \
    "\x96\x24\xe4\x16\x15\xcd\xa9\xf3\xf2\x8e\xed\xbe" \
    "\x78\xb1\x7d\xd5\x00\x00\x50\x5b\x5b\x6b\xdc\xb1" \
    "\x63\xc7\x4b\xc9\xc9\xc9\xa6\xeb\xd7\xaf\x8f\x5f" \
    "\xb9\x72\xe5\xa4\xdd\x6e\x0f\xd7\xd7\xd7\x33\x4e" \
    "\xa7\x33\x1d\x40\x79\x5a\x5a\xda\x9e\x7d\xfb\xf6" \
    "\x1d\xd8\x56\x5c\x9c\x3b\xd9\xd8\x88\xca\xe2\x62" \
    "\x26\x14\x8d\xc2\x13\x0e\x63\x32\x10\xc0\xd4\xe4" \
    "\x24\x98\x68\x14\xd9\xb9\xb9\xb2\xa1\xb0\xf0\x77" \
    "\x3b\xda\xdb\x9f\xfb\xae\x2b\xf6\x6d\x03\x00\xc0" \
    "\x62\xb1\xa4\x25\x24\x24\xa8\xfc\x7e\xbf\x30\x30" \
    "\x30\xe0\x5d\xd6\x10\x45\x51\x35\x35\x35\x06\x51" \
    "\x14\x37\x1f\x08\x04\xce\x16\x44\x22\x25\x26\x83" \
    "\x01\x15\xa5\xa5\x08\xc7\x62\x0b\x08\x9e\xc7\xc4" \
    "\xd4\x14\x98\xf9\x79\x64\x64\x66\x22\xb3\xa4\xa4" \
    "\xcd\x61\x30\x3c\x72\xac\xb9\x59\x58\x15\xc0\x6d" \
    "\x35\x48\x51\xf4\x56\xab\xf5\x81\x87\x66\x67\x4f" \
    "\x9b\x62\xb1\x32\xa3\x5e\x8f\x2d\x66\x33\xe6\x45" \
    "\x11\xde\x70\x18\x53\xc1\x20\x6e\xb8\x5c\xa0\x83" \
    "\x41\x18\x8c\x46\xe4\x94\x96\xf6\xfa\x19\xe6\xfe" \
    "\xfb\x3a\x3a\x26\xbf\xcd\xf5\xbe\xf7\x7d\x21\x42" \
    "\x88\x92\x9d\x9f\xdf\x71\x29\x2d\xed\x69\x9f\x4a" \
    "\x35\xe0\xf5\xfb\xd1\xdb\xdf\x8f\x64\x8e\x83\x29" \
    "\x39\x19\xd9\xa9\xa9\xc8\xcb\xcc\x04\x31\x18\x30" \
    "\xeb\xf5\xc2\x61\xb7\x57\x69\x23\x91\xcb\xef\x1f" \
    "\x3c\x58\xfb\x6d\xae\xf7\xbd\x8f\x40\x3c\xf5\xf5" \
    "\xf5\xcc\xe4\xc8\xc8\xfe\xc3\x5e\xef\x73\x46\x51" \
    "\x2c\x4d\x4d\x49\x81\xb5\xbc\x1c\x11\x51\x84\x6f" \
    "\x7e\x1e\xd3\xc1\x20\xc6\x3c\x1e\x08\x5e\x2f\xb4" \
    "\x1c\x87\xa2\xb2\x32\x41\x95\x91\x71\x62\x5b\x5b" \
    "\xdb\x6b\xeb\x02\x00\x2c\x20\x5c\x23\x23\x07\x0e" \
    "\x79\xbd\xcf\x19\x44\xb1\x44\x9b\x9c\x0c\xdb\x96" \
    "\x2d\x88\x88\x22\xfc\x91\x08\x5c\x73\x73\x18\xf3" \
    "\xf9\xc0\xbb\xdd\xd0\x28\x0a\x4a\xcc\x66\x92\x9a" \
    "\x93\xf3\x82\xad\xad\xed\x57\xb8\xcd\x8e\xad\x28" \
    "\x20\x8e\x98\x1a\x1e\x3e\xf8\xb0\xcf\x77\x4a\x2f" \
    "\x49\xc5\x9a\xa4\x24\xd4\x56\x56\x42\x90\x24\x04" \
    "\x6e\x22\x6e\xf8\xfd\x70\xcf\xcc\x20\x55\x96\x91" \
    "\x5f\x50\x80\xec\x92\x92\x7f\xfa\x64\xb9\x7e\x57" \
    "\x5b\x5b\x68\xcd\x01\x71\xc4\xc4\xe0\xe0\xa1\x23" \
    "\x3c\xff\x5b\x83\x28\x16\x25\x26\x26\x62\xab\xc5" \
    "\x82\xa8\x28\x82\x17\x04\xb8\xe6\xe6\x30\xee\xf7" \
    "\x63\xc2\xed\x46\x6a\x2c\x86\x9c\x4d\x9b\x90\x6f" \
    "\x36\x0f\x0a\x14\xb5\xb7\xa6\xad\x6d\x74\xcd\x01" \
    "\x71\xc4\xf8\xc0\xc0\xe1\x47\x82\xc1\x67\xf5\xa2" \
    "\x58\x98\xa8\x56\xa3\xa6\xaa\x0a\x0a\x21\x08\x08" \
    "\x02\xdc\x73\x73\x18\x0f\x04\x30\xe6\x76\x43\x13" \
    "\x89\x60\x63\x66\x26\x0a\xcc\x66\xbf\x94\x90\xf0" \
    "\x60\xed\x9b\x6f\xbe\xbf\xe6\x00\x60\x61\x93\x38" \
    "\x51\x14\x0f\x37\x04\x02\xbf\xd1\x49\x52\x81\x9a" \
    "\xe3\x60\xab\xa8\x00\xcd\xb2\xe0\x05\x01\xee\x50" \
    "\x08\xe3\x7e\x3f\x9c\xb3\xb3\xe0\x42\x21\x6c\x32" \
    "\x1a\x51\x72\xe7\x9d\x12\xad\xd5\x36\x5a\xdf\x78" \
    "\xe3\xe5\x35\x07\xc4\x11\xea\x58\xac\xe1\x67\x3c" \
    "\xff\x8c\x4e\x92\xf2\x39\x96\x85\x75\xf3\x66\x70" \
    "\x6a\x35\x82\xd1\x28\x66\x43\x21\x7c\xe1\xf7\x63" \
    "\xc4\xe3\x81\xc4\xf3\xc8\xd3\x6a\x51\x52\x56\x86" \
    "\x24\x93\xe9\x95\x4a\x42\x1e\x43\x5b\xdb\xb2\xdd" \
    "\xf0\x55\x07\xc4\x11\x89\xd1\xe8\xd1\x23\xc1\xe0" \
    "\xd3\x3a\x49\xca\x67\x59\x16\x55\x65\x65\x48\x48" \
    "\x4c\x44\x28\x16\x83\x3b\x14\xc2\x44\x20\x80\xeb" \
    "\x1e\x0f\x78\x9f\x0f\x79\x89\x89\x30\x97\x95\xc1" \
    "\x94\x9d\xfd\x31\xa1\xe9\x07\xca\x5b\x5a\xfc\xf1" \
    "\xb6\xd6\xe4\x05\xc7\xe5\xcb\x97\x45\x3f\x21\x17" \
    "\x5a\x74\xba\x3f\x04\x39\x6e\x54\x92\x24\x7c\xde" \
    "\xdf\x8f\x70\x28\x84\x14\x95\x0a\x19\x1a\x0d\x36" \
    "\xe9\xf5\x28\x4a\x4b\x83\xc1\x64\xc2\x60\x24\x82" \
    "\x2b\x76\x3b\xa6\x9c\xce\x3a\x4a\x51\xfe\x7d\x6e" \
    "\xc9\xd6\xcf\x9a\xbd\xa1\xe9\xeb\xeb\x8b\x69\xee" \
    "\xb8\xe3\xb5\x16\xad\xf6\xf9\x20\xc7\x8d\x29\xb2" \
    "\x8c\xff\x0e\x0c\x80\xe7\x79\x68\xd4\x6a\xa4\xdf" \
    "\x44\x6c\xd4\xe9\x82\xda\xf4\xf4\xfe\x31\x8a\x72" \
    "\x3b\x06\x07\x31\x36\x38\x68\x2e\xcf\xcf\xff\xf5" \
    "\x9a\x03\x00\xa0\xb3\xb3\x33\x9a\x94\x9d\x7d\xbe" \
    "\x55\xa7\x7b\x3e\xc8\x71\x37\x08\x21\xb8\x3a\x34" \
    "\x04\x9f\xcf\x07\x8d\x4a\x05\x15\xcb\x06\xff\x48" \
    "\x51\xf7\xbe\x9d\x9a\xfa\xd0\x50\x6e\xee\x9f\x83" \
    "\x34\xcd\xdf\x70\x3a\xe1\xe8\xef\xdf\xbb\x2e\x00" \
    "\xc0\x02\x22\x9a\x94\xf4\xf7\x0b\x06\xc3\x99\x39" \
    "\x96\x1d\x27\x00\xae\x39\x1c\x70\xcf\xce\x22\x46" \
    "\xc8\x80\xc1\x60\xe8\xb1\xdb\xed\x7d\x2e\x96\xfd" \
    "\x07\x9b\x92\x22\x30\x34\x0d\xef\xd4\x94\xa1\xa8" \
    "\xa8\x48\x0d\xac\x03\x00\x00\x7c\xf2\xc9\x27\x91" \
    "\x10\x4d\x9f\x6f\x35\x1a\xff\x14\x62\x98\x2f\x00" \
    "\x60\xd0\xe9\x84\x18\x08\x94\x3d\xab\x56\xe7\x02" \
    "\xc0\xe3\x1c\xf7\x70\x16\xcb\xa6\x31\x14\x05\x41" \
    "\xa5\x72\xaa\xd5\xea\x85\x3d\xff\xb5\x98\x85\xbe" \
    "\x2e\x5b\xb6\x6c\x49\x4e\x67\x98\xe3\x87\xfd\xfe" \
    "\x5f\xa6\x88\xe2\x46\x85\x10\x68\x34\x1a\xc1\x94" \
    "\x91\x11\x98\xe3\xf9\xf4\x89\xa9\x29\x5a\x24\x44" \
    "\xea\x35\x18\x1e\x79\x79\x78\xb8\x15\x58\x27\x23" \
    "\x10\x8f\xdd\x6e\x0f\x4f\xc7\x62\xcd\xad\x3a\xdd" \
    "\x0b\x01\x95\x6a\x84\xa6\x28\x84\x42\xa1\x04\xe7" \
    "\xc8\xc8\x86\x99\x99\x19\x1a\x34\x2d\x3a\x34\x9a" \
    "\x57\xba\xb5\xda\x7f\xc5\xcf\x59\x57\x23\x10\x4f" \
    "\x5d\x5d\x5d\x4a\x28\x14\xda\x7b\xaf\x20\x3c\x98" \
    "\x15\x8b\x15\xab\x25\x29\x99\xa7\x69\x97\x3d\x21" \
    "\xe1\xe2\x35\xb5\xba\xc3\x6e\xb7\x2f\xfe\x3e\x5a" \
    "\x97\x00\x60\xe1\x9f\x5d\x4d\x4d\x4d\x21\x45\x51" \
    "\xe9\x8a\xa2\x30\x84\x10\xaf\x24\x49\x13\xbd\xbd" \
    "\xbd\x81\x65\xf5\xd6\x2b\xe0\x76\xb3\xae\x9e\x81" \
    "\x6f\x93\x1f\x3c\xe0\x7f\xf9\xb2\x6b\xe1\x6a\x66" \
    "\x48\x01\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42" \
    "\x60\x82"

def getIconSet(name, group=KIcon.Toolbar):
    return KGlobal.iconLoader().loadIconSet(name, group)

class IconButton(QPushButton):
    def __init__(self, parent, icon_name):
        QPushButton.__init__(self, parent)
        self.setFlat(True)
        self.myset = getIconSet(icon_name)
        self.setIconSet(self.myset)
        size = self.myset.iconSize(QIconSet.Automatic)
        self.myWidth = size.width() 
        self.myHeight = size.height() 
        self.resize(self.myWidth, self.myHeight)

class EntryView(QListView):
  
    
    def __init__(self, parent):
        QListView.__init__(self, parent)
	self.addColumn(("Name"))
        self.addColumn(("Type"))
        self.addColumn(("Default"))
        self.addColumn(("Root Device"))
	self.setAllColumnsShowFocus(1)
        self.setShowSortIndicator(1)
        self.setResizeMode(QListView.NoColumn)
        self.viewport().setPaletteBackgroundColor(KGlobalSettings.baseColor())
        self.entries = []
    
    def clear(self):
        for e in self.entries:
            e.hide()
        self.entries = []
    
    def add(self, editWidget, index, title, description, pardus, os_data):
        e = Entry(self.viewport(), editWidget, index, title, description, pardus, os_data)
        self.entries.append(e)
	item = QListViewItem(self,None)
        item.setText(0,e.title)
        item.setPixmap(0,e.icon)
        item.setText(1,e.os_data["os_type"])
        item.setPixmap(2,e.icon2)
        item.setText(3,e.description)
        size = QSize(self.width(), self.height())
        self.resizeEvent(QResizeEvent(size , QSize(0, 0)))
        return e
    
    def resizeEvent(self, event):
        QListView.resizeEvent(self, event)
        self.myResize(self.visibleWidth())
    
    def myResize(self, width):
        mw = 0
        th = 0
        #for e in self.entries:
            
            #h = e.sizeHint().height()
            #mw = max(mw, e.sizeHint().width())
            #e.setGeometry(0, th, width, h)
            #th += h
        self.setMinimumSize(QSize(mw, 0))
        if th > self.height():
            self.resizeContents(width - 12, th)
        else:
            self.resizeContents(width, th)

class Entry(QWidget):
    def __init__(self, parent, editWidget, index, title, description, pardus, os_data):
        QWidget.__init__(self, parent)
        self.editWidget = editWidget
        
        self.index = index
        self.title = title
        self.description = description
        self.pardus = pardus
        self.os_data = os_data
        
        
        if self.pardus:
            os_type = "pardus"
        else:
            os_type = os_data["os_type"]
        
        if not os.path.exists(locate("data", "boot-manager/%s.png" % os_type)):
            os_type = "other"
        
        self.icon = QImage(locate("data", "boot-manager/%s.png" % os_type))
        self.icon.smoothScale(32, 32)
        self.icon = QPixmap(self.icon)
	self.icon2 = QPixmap()
        self.icon2.loadFromData(image1_data,"PNG")
        if "default" in os_data and os_data["default"] != "saved":
	     self.icon2 = QPixmap()
             self.icon2.loadFromData(image0_data,"PNG")
	    
	
    
    def slotEdit(self):
        self.editWidget.editEntry(self.os_data)
    
    def slotDelete(self):
        self.editWidget.deleteEntry(self.index, self.title)
    
    def paintEvent(self, event):
        paint = QPainter(self)
        col = KGlobalSettings.baseColor()
        paint.fillRect(event.rect(), QBrush(col))
        self.pushEdit.setPaletteBackgroundColor(col)
        self.pushDelete.setPaletteBackgroundColor(col)
        
        dip = (self.height() - self.icon.height()) / 2
        paint.drawPixmap(6, dip, self.icon)
        
        font = paint.font()
        font.setPointSize(font.pointSize() + 1)
        font.setBold(True)
	
	     
        fm = QFontMetrics(font)
        paint.drawText(6 + self.icon.width() + 6, fm.ascent() + 5, unicode(self.title))
        
        fark = fm.height()
        font.setPointSize(font.pointSize() - 2)
        font.setUnderline(False)
        fm = self.fontMetrics()
        paint.drawText(6 + self.icon.width() + 6, 5 + fark + 3 + fm.ascent(), unicode(self.description))
        
    def resizeEvent(self, event):
        w = event.size().width()
        h = event.size().height()
        return QWidget.resizeEvent(self, event)
    
    def sizeHint(self):
        f = QFont(self.font())
        f.setPointSize(f.pointSize() + 1)
        f.setBold(True)
        fm = QFontMetrics(f)
        rect = fm.boundingRect(unicode(self.title))
        w = 6 + self.icon.width() + 6 + rect.width() + 30 + self.pushEdit.myWidth + 3 + self.pushDelete.myWidth + 6
        
        f.setPointSize(f.pointSize() - 2)
        fm2 = self.fontMetrics()
        rect2 = fm2.boundingRect(unicode(self.description))
        w2 = 6 + self.icon.width() + 6 + rect2.width() + 30 + self.pushEdit.myWidth + 3 + self.pushDelete.myWidth + 6
        
        w = max(w, w2)
        h = max(fm.height() + 3 + fm2.height(), 32) + 10
        return QSize(w, h)

class ComboList(QComboBox):
    def __init__(self, parent):
        QComboBox.__init__(self, parent)
        self.elements = {}
    
    def addItem(self, name, label):
        label = unicode(label)
        self.elements[name] = label
        self.insertItem(label)
    
    def getSelected(self):
        label = unicode(self.currentText())
        for name in self.elements:
            if label == unicode(self.elements[name]):
                return name
    
    def setSelected(self, name):
        label = self.elements[name]
        self.setCurrentText(label)

class widgetEntryList2(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.parent = parent

        layout = QGridLayout(self, 1, 2, 6, 6)

        #bar = QToolBar("main", None, self)
	
	
	
	self.image0 = QPixmap()
        self.image0.loadFromData(image2_data,"PNG")
	self.pushButton3 = IconButton(self,"edittrash")
        self.pushButton3.setGeometry(QRect(500,230,120,31))

       

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setGeometry(QRect(80,20,241,51))

        self.pixmapLabel2 = QLabel(self,"pixmapLabel2")
        self.pixmapLabel2.setGeometry(QRect(20,20,50,50))
        self.pixmapLabel2.setPixmap(self.image0)
        self.pixmapLabel2.setScaledContents(1)

        self.pushButton1 = IconButton(self,"add")
        self.pushButton1.setGeometry(QRect(500,130,120,31))
	self.pushButton3.setEnabled(False)

        self.pushButton2 = IconButton(self,"configure")
        self.pushButton2.setGeometry(QRect(500,180,120,31))
	self.pushButton2.setEnabled(False)

        self.listEntries = EntryView(self)
        self.listEntries.setGeometry(QRect(10,80,470,300))
        self.listEntries.setFocusPolicy(QListView.WheelFocus)
        self.listEntries.setFrameShadow(QListView.Sunken)
        self.listEntries.setAllColumnsShowFocus(1)
        self.listEntries.setShowSortIndicator(0)
        self.listEntries.setResizeMode(QListView.NoColumn)
        self.pushButton3.setText(("Delete"))
        self.textLabel1.setText(("<font><font><font><font size=\"+1\" ><b>Bootloader  Settings<font color=\"#ff5500\" size=\"+1\" face=\"Century Schoolbook L\"></font></b></font></font></font></font>"))
	
        self.pixmapLabel2.setText(QString.null)
        self.pushButton1.setText(("Add..."))
        self.pushButton2.setText(("Properties"))

        self.checkSaved = QCheckBox(self,"checkBox1")
        self.checkSaved.setGeometry(QRect(20,400,220,30))

        self.spinTimeout= QSpinBox(self,"spinBox1")
        self.spinTimeout.setGeometry(QRect(570,400,50,30))

        self.textLabel1_2 = QLabel(self,"textLabel1_2")
        self.textLabel1_2.setGeometry(QRect(510,400,60,30))
        self.checkSaved.setText(("Remember last booted entry."))
        self.textLabel1_2.setText(("Timeout:"))
        

        self.resize(QSize(657,480).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)
        
        """but = QToolButton(getIconSet("add"), "", "main", self.slotAddEntry, bar)
        but.setTextLabel(i18n("New Entry"), False)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)

        but = QToolButton(getIconSet("file_broken"), "", "main", self.slotUnused, bar)
        but.setTextLabel(i18n("Unused Kernels"), False)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)

        lab = QToolButton(bar)
        lab.setEnabled(False)
        bar.setStretchableWidget(lab)

        but = QToolButton(getIconSet("help"), "", "main", self.slotHelp, bar)
        but.setTextLabel(i18n("Help"), False)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        but.hide()
        layout.addMultiCellWidget(bar, 0, 0, 0, 4)
        self.toolbar = bar"""

       
        """layout.addMultiCellWidget(self.listEntries, 1, 1, 6, 4)

        self.checkSaved = QCheckBox(self)
        self.checkSaved.setText(i18n("Remember last booted entry."))
        layout.addWidget(self.checkSaved, 2, 0)

        spacer = QSpacerItem(10, 1, QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addItem(spacer, 2, 1)

        self.labelTimeout = QLabel(self)
        self.labelTimeout.setText(i18n("Timeout:"))
        layout.addWidget(self.labelTimeout,2,2)

        self.spinTimeout = QSpinBox(self)
        self.spinTimeout.setMinValue(3)
        self.spinTimeout.setMaxValue(30)
        layout.addWidget(self.spinTimeout, 0, 3)"""

        self.connect(self.checkSaved, SIGNAL("clicked()"), self.slotCheckSaved)
	self.connect(self.pushButton1,SIGNAL("clicked()"),self.slotAddEntry)
	
	
	  
        self.setTimeoutSlot(True)

        self.init()
	self.connect(self.listEntries,SIGNAL("selectionChanged()"), self.slotChangeButton)
	self.connect(self.pushButton2,SIGNAL("clicked()"),self.slotEdit)
	self.connect(self.pushButton3,SIGNAL("clicked()"),self.slotDelete)
	
    def slotEdit(self):
        item=self.listEntries.selectedItem()
	for d in self.listEntries.entries:
		if(d.title==item.text(0)):
			d.slotEdit()
   
    	
    def slotDelete(self):
        item=self.listEntries.selectedItem()
	for d in self.listEntries.entries:
		if(d.title==item.text(0)):
			d.slotDelete()
			
    def slotChangeButton(self):
        versions = []
        for item in self.listEntries.entries:
            if self.listEntries.isSelected(self.listEntries.findItem(item.title,0)):
                versions.append(item)
    
        if len(versions):
            self.pushButton2.setEnabled(True)
            self.pushButton3.setEnabled(True)
        else:
            self.pushButton2.setEnabled(False)
            self.pushButton3.setEnabled(False)	
    

    def setTimeoutSlot(self, active):
        if active:
            self.connect(self.spinTimeout, SIGNAL("valueChanged(int)"), self.slotTimeoutChanged)
        else:
            self.disconnect(self.spinTimeout, SIGNAL("valueChanged(int)"), self.slotTimeoutChanged)

    def init(self):
        #self.toolbar.setEnabled(True)
        self.listEntries.viewport().setEnabled(True)
        self.checkSaved.setEnabled(True)

    def slotCheckSaved(self):
        def handler():
            self.parent.parent.queryEntries()
        def cancel():
            default = self.parent.parent.options["default"]
            self.checkSaved.setChecked(default == 'saved')
        def error(exception):
            cancel()
        ch = self.parent.parent.callMethod("setOption", "tr.org.pardus.comar.boot.loader.set")
        ch.registerAuthError(error)
        ch.registerDBusError(error)
        ch.registerCancel(cancel)
        ch.registerDone(handler)
        if self.checkSaved.isChecked():
            ch.call("default", "saved")
        else:
            ch.call("default", "0")

    def slotTimeoutChanged(self, value):
        def handler():
            self.spinTimeout.setEnabled(True)
        def cancel():
            handler()
        def error(exception):
            handler()
        self.spinTimeout.setEnabled(False)
        ch = self.parent.parent.callMethod("setOption", "tr.org.pardus.comar.boot.loader.set")
        ch.registerAuthError(error)
        ch.registerDBusError(error)
        ch.registerCancel(cancel)
        ch.registerDone(handler)
        ch.call("timeout", str(value))

   
    
    def slotAddEntry(self):
        self.parent.parent.widgetEditEntry.newEntry()


    def slotHelp(self):
        pass
class widgetEntryList(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.parent = parent

        self.tabWidget2 = QTabWidget(self,"tabWidget2")
        self.tabWidget2.setGeometry(QRect(7,7,640,470))

        self.tab = widgetEntryList2(self)
        self.tabWidget2.insertTab(self.tab,QString.fromLatin1(""))

        self.tab_2 = widgetUnused(self)
        self.tabWidget2.insertTab(self.tab_2,QString.fromLatin1(""))

       

        self.resize(QSize(600,480).expandedTo(self.minimumSizeHint()))
	self.resize(QSize(700,480).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

      
        self.tabWidget2.changeTab(self.tab,("Existing"))
        self.tabWidget2.changeTab(self.tab_2,("Unused"))
	

class Addnew(QDialog):
	def __init__(self, format,parent=None):
           #super(Addnew, self).__init__(parent)
	   QDialog.__init__(self, parent)
	   self.labelSystem = QLabel(self)
           self.labelSystem.setText(("System:"))
	   self.mainwid=widgetEditEntry(win.mainwidget)
	   #self.mainwid.show()  

class widgetEditEntry(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        
	self.parent = parent
        self.systems = self.parent.systems

        self.saved = False
        self.fields = {}
	self.fields2 = {}


        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setGeometry(QRect(20,0,120,40))

        self.textLabel8 = QLabel(self,"textLabel8")
        self.textLabel8.setGeometry(QRect(20,250,141,31))

        LayoutWidget = QWidget(self,"layout3")
        LayoutWidget.setGeometry(QRect(30,290,400,210))
        layout3 = QGridLayout(LayoutWidget,1,1,11,6,"layout3")

        self.labelBoot = QLabel(LayoutWidget)

        layout3.addWidget(self.labelBoot,3,0)

        self.labelSplash = QLabel(LayoutWidget)

        layout3.addWidget(self.labelSplash,2,0)

        self.labelRoot2= QLabel(LayoutWidget)

        layout3.addWidget(self.labelRoot2,0,0)

        self.labelResume = QLabel(LayoutWidget)

        layout3.addWidget(self.labelResume,4,0)

        self.editOptions5 = QComboBox(0,LayoutWidget)
        self.editOptions5.setEditable(1)

        layout3.addWidget(self.editOptions5,4,1)

        self.editOptions1= QLineEdit(LayoutWidget)

        layout3.addWidget(self.editOptions1,0,1)

        self.editOptions4 = QComboBox(0,LayoutWidget)

        layout3.addWidget(self.editOptions4,3,1)

        self.editOptions3 = QComboBox(0,LayoutWidget)

        layout3.addWidget(self.editOptions3,2,1)

        self.labelvga= QLabel(LayoutWidget)

        layout3.addWidget(self.labelvga,1,0)

        self.editOptions2 = QLineEdit(LayoutWidget)

        layout3.addWidget(self.editOptions2,1,1)

        self.checkDefault = QCheckBox(self)
        self.checkDefault.setText(("Set as default boot entry."))
        self.checkDefault.setGeometry(QRect(11,511,188,22))

        self.buttonCancel = IconButton(self,"cancel")
        self.buttonCancel.setText(("Cancel"))
        self.buttonCancel.setGeometry(QRect(349,539,90,29))

        self.buttonOK = IconButton(self,"ok")
        self.buttonOK.setText(("Save"))
        self.buttonOK.setGeometry(QRect(264,540,80,29))

        self.labelRoot = QLabel(self)
	self.labelRoot.setText(("Root:"))
        self.labelRoot.setGeometry(QRect(30,120,50,20))

        self.labelTitle = QLabel(self)
	self.labelTitle.setText(("Title:"))
        self.labelTitle.setGeometry(QRect(30,40,40,20))

        self.toolKernel = IconButton(self,"filefind")
        self.toolKernel.setGeometry(QRect(350,160,90,31))

        self.labelInitrd = QLabel(self)
        self.labelInitrd.setGeometry(QRect(30,200,50,20))

        self.editTitle = QLineEdit(self)
        self.editTitle.setGeometry(QRect(91,40,340,25))

        self.editKernel = QComboBox(0,self)
        self.editKernel.setGeometry(QRect(90,160,251,25))
        self.editKernel.setEditable(1)

        self.labelSystem= QLabel(self)
	self.labelSystem.setText(i18n("System:"))
        self.labelSystem.setGeometry(QRect(30,80,60,20))

        self.editRoot = QComboBox(0,self)
        self.editRoot.setGeometry(QRect(90,120,340,25))
        self.editRoot.setEditable(1)
       
        self.listSystem = ComboList(self)
        self.listSystem.setGeometry(QRect(91,80,340,25))

        self.labelKernel = QLabel(self)
        self.labelKernel.setGeometry(QRect(30,160,60,20))

        self.editInitrd = QComboBox(0,self)
        self.editInitrd.setGeometry(QRect(90,200,250,25))
        self.editInitrd.setEditable(1)

        self.toolInitrd = IconButton(self,"filefind")
        self.toolInitrd.setGeometry(QRect(350,200,90,31))

        self.line1 = QFrame(self,"line1")
        self.line1.setGeometry(QRect(20,230,420,20))
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setFrameShape(QFrame.HLine)
        self.fields["options1"] = (self.labelRoot2, self.editOptions1)
	self.fields["options2"] = (self.labelvga, self.editOptions2)
	self.fields2["options3"] = (self.labelSplash, self.editOptions3)
	self.fields2["options4"] = (self.labelBoot, self.editOptions4)
	self.fields2["options5"] = (self.labelResume, self.editOptions5)
        self.fields2["root"] = (self.labelRoot, self.editRoot)
        self.fields2["kernel"] = (self.labelKernel, self.editKernel)
        self.fields2["initrd"] = (self.labelInitrd, self.editInitrd)


        self.setCaption(("Form1"))
        self.textLabel1.setText((("<b>Basic Settings</b>")))
        self.textLabel8.setText(("<b>Kernel Parameters</b>"))
        self.labelBoot.setText(("Booting mode:"))       
        self.labelSplash.setText("Splash:")
        self.labelRoot2.setText(("Root:"))
        self.labelResume.setText(("Resume:"))
        self.labelvga.setText(("Vga:"))
        self.buttonCancel.setText(("Cancel"))
        self.buttonOK.setText(("Save"))
        self.labelRoot.setText(("Root:"))
        self.labelTitle.setText(("Title:"))
        self.toolKernel.setText(("Browse.."))
        self.labelInitrd.setText(("Initrd:"))
        self.labelSystem.setText(("System:"))
        self.labelKernel.setText(("Kernel:"))
        self.toolInitrd.setText(("Browse.."))
	self.rootdir=QDir("/sys/block/sda","sda?")
	self.kerneldir=QDir("/boot","*vmlinuz* *kernel*")
	self.initdir=QDir("/boot","*initram*")
	self.editOptions3.insertItem("verbose")
	self.editOptions3.insertItem("native")
	self.editOptions3.insertItem("silent")
	self.editOptions4.insertItem("quiet")
	self.editOptions4.insertItem("debug")
	for s in self.rootdir.entryList():
	  self.editRoot.insertItem("/dev/"+s)
	  self.editOptions5.insertItem("/dev/"+s)
	
	for s in self.kerneldir.entryList():
	  self.editKernel.insertItem("/boot/"+s)
	  
	for s in self.initdir.entryList():
	  self.editInitrd.insertItem("/boot/"+s)
	 
       
        self.resize(QSize(455,585).expandedTo(self.minimumSizeHint()))
       
        self.connect(self.listSystem, SIGNAL("activated(const QString &)"), self.slotSystem)
        self.connect(self.buttonOK, SIGNAL("clicked()"), self.slotSave)
	self.connect(self.toolKernel, SIGNAL("clicked()"), self.slotFile1)
	self.connect(self.toolInitrd, SIGNAL("clicked()"), self.slotFile2)
        self.connect(self.buttonCancel, SIGNAL("clicked()"), self.slotExit)

        self.clearWState(Qt.WState_Polished)
	self.resetEntry()

    def slotFile1(self):
        filename=QFileDialog.getOpenFileName("/", "*", self, "Select Kernel image file")
        self.editKernel.setCurrentText(filename)
	
    def slotFile2(self):
        filename=QFileDialog.getOpenFileName("/", "*", self, "Select Initrd file")
        self.editInitrd.setCurrentText(filename)
 


    def newEntry(self):
        self.resetEntry()
        win.resize(QSize(455, 585).expandedTo(win.minimumSizeHint()))
	d=Addnew(self.parent.widgetEditEntry)
	#win.mainwidget.hide()
	#d.show()
        self.parent.stack.raiseWidget(self.parent.widgetEditEntry)
	#win.resize(QSize(800, 480).expandedTo(win.minimumSizeHint()))
	
       

   
    def editEntry(self, entry):
        self.resetEntry()
        win.resize(QSize(455, 585).expandedTo(win.minimumSizeHint()))
        self.entry = entry
        systems = self.parent.systems

        self.checkDefault.setChecked(False)

        self.editTitle.setText(unicode(entry["title"]))

        self.listSystem.setCurrentText(unicode(systems[entry["os_type"]][0]))
        self.slotSystem(unicode(systems[entry["os_type"]][0]))
	
	if "options" in entry:
            c=(unicode(copy.deepcopy(entry["options"])))
            paramlist=c.split(" ")
	    entry["options1"]=paramlist[0].replace("root=","")
	    entry["options2"]=paramlist[1].replace("vga=","")
	    entry["options3"]=paramlist[2].replace("splash=","")
	    entry["options4"]=paramlist[3]
	    entry["options5"]=paramlist[4].replace("resume=","")

        for label, (widgetLabel, widgetEdit) in self.fields.iteritems():
            if label in entry:
                widgetEdit.setText(unicode(entry[label]))
		
	for label, (widgetLabel, widgetEdit) in self.fields2.iteritems():
            if label in entry:
                widgetEdit.setCurrentText(unicode(entry[label]))

        

        if self.parent.widgetEntries.tab.checkSaved.isChecked():
            self.checkDefault.hide()
        else:
            self.checkDefault.show()

        if "default" in entry and entry["default"] != "saved":
            self.checkDefault.setChecked(True)

        self.parent.stack.raiseWidget(self.parent.widgetEditEntry)



    def deleteEntry(self, index, title):
        entries = self.parent.entries
        pardus_root = getRoot()
        pardus_entries = []
        pardus_versions = {}
        for entry in entries:
            if entry["os_type"] in ["linux", "xen"] and entry["root"] == pardus_root:
                pardus_entries.append(entry)
                version = entry["kernel"].split("kernel-")[1]
                if version not in pardus_versions:
                    pardus_versions[version] = 0
                pardus_versions[version] += 1
        if len(pardus_entries) < 2 and entries[index] in pardus_entries:
            KMessageBox.error(self, ("There must be at least one Pardus entry."), ("Access Denied"))
            return
        confirm = KMessageBox.questionYesNo(self, ("Are you sure you want to remove this entry?"), i18n("Delete Entry"))
        if confirm == KMessageBox.Yes:
            uninstall = "no"
            if entries[index] in pardus_entries:
                entry_version = entries[index]["kernel"].split("kernel-")[1]
                if pardus_versions[entry_version] == 1:
                    confirm_uninstall = KMessageBox.questionYesNo(self, ("This is a Pardus kernel entry.\nDo you want to uninstall it from the system?"), ("Uninstall Kernel"))
                    if confirm_uninstall == KMessageBox.Yes:
                        uninstall = "yes"
            self.parent.widgetEntries.tab.listEntries.viewport().setEnabled(False)

            ch = self.parent.callMethod("removeEntry", "tr.org.pardus.comar.boot.loader.removeentry")
            ch.call(index, title, uninstall)

    def resetEntry(self):
        self.entry = None
        systems = self.parent.systems

        self.editTitle.setText("")

        self.listSystem.clear()
        if systems:
            for name in systems:
                label = unicode(systems[name][0])
                self.listSystem.addItem(name, label)

            self.listSystem.setSelected("linux")
            self.slotSystem("Linux")

        for label, (widgetLabel, widgetEdit) in self.fields.iteritems():
            widgetEdit.setText("")

        self.checkDefault.setChecked(False)
        self.buttonOK.setEnabled(True)

    def slotSystem(self, label):
        systems = self.parent.systems
        for name, (sys_label, fields) in systems.iteritems():
            if unicode(sys_label) == label:
                break
        for label, (widgetLabel, widgetEdit) in self.fields.iteritems():
            if label in self.fields:
                widgetLabel.show()
                widgetEdit.show()
            else:
                widgetLabel.hide()
                widgetEdit.hide()
	for label, (widgetLabel, widgetEdit) in self.fields2.iteritems():
            if label in self.fields2:
                widgetLabel.show()
                widgetEdit.show()
            else:
                widgetLabel.hide()
                widgetEdit.hide()

    def showError(self, message):
        KMessageBox.information(self, message, ("Error"))

    def slotSave(self):
        self.buttonOK.setEnabled(False)
        default = "no"
        if self.parent.widgetEntries.tab.checkSaved.isChecked():
            default = "saved"
        elif self.checkDefault.isChecked():
            default = "yes"

        systems = self.parent.systems
        os_type = self.listSystem.getSelected()

        args = {
            "title": unicode(self.editTitle.text()),
            "os_type": os_type,
            "root": "",
            "kernel": "",
            "initrd": "",
            "options": "",
            "default": default,
            "index": -1,
        }

        for label in self.fields:
            if label in systems[os_type][1]:
                value = unicode(self.fields[label][1].text())
                args[label] = value
		
	for label in self.fields2:
            if label in systems[os_type][1]:
                value = unicode(self.fields2[label][1].currentText())
                args[label] = value
		
	args["options"]=unicode("root="+self.editOptions1.text()+" vga="+self.editOptions2.text()+
	                " splash="+self.editOptions3.currentText()+" "+self.editOptions4.currentText()
	                +" resume="+self.editOptions5.currentText())

        if self.entry:
            args["index"] = int(self.entry["index"])

        self.saved = True

        def handlerError(exception):
            self.parent.widgetEditEntry.saved = False
            KMessageBox.error(self, unicode(exception), ("Failed"))
            self.parent.widgetEditEntry.buttonOK.setEnabled(True)
        def handler():
            self.parent.widgetEditEntry.saved = False
            self.parent.queryEntries()
            self.parent.widgetEditEntry.slotExit()
        ch = self.parent.callMethod("setEntry", "tr.org.pardus.comar.boot.loader.set")
        ch.registerDone(handler)
        ch.registerError(handlerError)
        ch.call(args["title"], args["os_type"], args["root"], args["kernel"], args["initrd"], args["options"], args["default"], args["index"])

    def slotExit(self):
        self.resetEntry()
        win.resize(QSize(650, 480).expandedTo(win.minimumSizeHint()))
        self.parent.stack.raiseWidget(self.parent.widgetEntries)
	


class widgetUnused(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.parent = parent
       # self.link = comar_link

        layout = QGridLayout(self, 1, 1, 11, 6)

        self.labelTitle = QLabel(self)
        self.labelTitle.setText(("These kernels are installed in the system but doesn't exist in boot loader list:"))
        layout.addWidget(self.labelTitle, 0, 0)

        self.listKernels = QListBox(self)
        self.listKernels.setMinimumSize(100, 200)
        self.listKernels.setSelectionMode(QListBox.Extended)
        layout.addMultiCellWidget(self.listKernels, 1, 4, 0, 0)
       
        self.buttonAdd = IconButton(self,"add")
        self.buttonAdd.setEnabled(False)
        self.buttonAdd.setText(("Add Entry"))
       
        layout.addWidget(self.buttonAdd, 1, 1)

        self.buttonRemove = IconButton(self,"edittrash")
        self.buttonRemove.setText(("Uninstall"))
        self.buttonRemove.setEnabled(False)
        layout.addWidget(self.buttonRemove, 2, 1)

        spacer = QSpacerItem(10, 1, QSizePolicy.Fixed, QSizePolicy.Expanding)
        layout.addItem(spacer, 3, 1)

        self.buttonOK = IconButton(self,"ok")
        self.buttonOK.setText(("Ok"))
        layout.addWidget(self.buttonOK, 4, 1)

        self.connect(self.buttonAdd, SIGNAL("clicked()"), self.slotAdd)
        self.connect(self.buttonRemove, SIGNAL("clicked()"), self.slotRemove)
        self.connect(self.buttonOK, SIGNAL("clicked()"), self.slotExit)
        self.connect(self.listKernels, SIGNAL("selectionChanged()"), self.slotKernels)

        self.listBusy = False
        self.listUnused()
    
    def listUnused(self):
        def handler(versions):
            self.listKernels.clear()
            for version in versions:
                if version.strip():
                    self.listKernels.insertItem(version)
            self.slotKernels()
        ch = self.parent.parent.callMethod("listUnused", "tr.org.pardus.comar.boot.loader.get")
        ch.registerDone(handler)
        ch.call()
	
    def slotExit(self):
        #self.parent.parent.stack.raiseWidget(self.parent.parent.widgetEntries)
	self.parent.tabWidget2.setCurrentPage(0)
    
    def slotKernels(self):
        item = self.listKernels.firstItem()
        versions = []
        while item:
            if item.isSelected():
                versions.append(str(item.text()))
            item = item.next()
        if len(versions):
            self.buttonAdd.setEnabled(True)
            self.buttonRemove.setEnabled(True)
        else:
            self.buttonAdd.setEnabled(False)
            self.buttonRemove.setEnabled(False)
    
    def slotAdd(self):
        self.buttonAdd.setEnabled(False)
        self.buttonRemove.setEnabled(False)
	self.parent.parent.widgetEditEntry.resetEntry()
        self.parent.parent.stack.raiseWidget(self.parent.parent.widgetEditEntry)
        
        version = str(self.listKernels.currentText())
        root = getRoot()
        self.parent.parent.widgetEditEntry.editTitle.setText(version)
        self.parent.parent.widgetEditEntry.editRoot.setText(root)
        if version.endswith("-dom0"):
            self.parent.parent.widgetEditEntry.listSystem.setCurrentText("Xen")
        else:
            self.parent.parent.widgetEditEntry.listSystem.setCurrentText("Linux")
        self.parent.parent.widgetEditEntry.editKernel.setText("/boot/kernel-%s" % version)
        self.parent.parent.widgetEditEntry.editOptions.setText("root=%s" % root)
    
    def slotRemove(self):
        confirm = KMessageBox.questionYesNo(self, ("Do you want to uninstall selected kernel(s) from the system?"), ("Uninstall Kernel"))
        if confirm == KMessageBox.Yes:
            self.buttonAdd.setEnabled(False)
            self.buttonRemove.setEnabled(False)
            item = self.listKernels.firstItem()
            versions = []
            while item:
                if item.isSelected():
                    versions.append(str(item.text()))
                item = item.next()
            if len(versions):
                self.listBusy = True
                def handler(isLast=False):
                    if isLast:
                        self.listBusy = False
                        self.listUnused()
                for version in versions:
                    ch = self.parent.parent.callMethod("removeUnused", "tr.org.pardus.comar.boot.loader.removeunused")
                    ch.registerDone(handler, version == versions[-1])
                    ch.call(version)
    
    


class widgetMain(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        
        #self.link = None
        self.dia = None
        
        if not self.openBus():
            sys.exit(1)
        
        self.entries = []
        self.options = {}
        self.systems = {}
        self.screens = []
        
        layout = QGridLayout(self, 1, 1, 0, 0)
        self.stack = QWidgetStack(self)
        layout.addWidget(self.stack, 0, 0)
        
        self.widgetEntries = widgetEntryList(self)
        self.stack.addWidget(self.widgetEntries)
        self.screens.append("Entries")
        
        self.widgetEditEntry = widgetEditEntry(self)
        self.stack.addWidget(self.widgetEditEntry)
        self.screens.append("EditEntry")
        
        """self.widgetUnused = widgetUnused(self)
        self.stack.addWidget(self.widgetUnused)
        self.screens.append("Unused")"""
        
        self.setup()
    def openBus(self):
        try:
            self.busSys = dbus.SystemBus()
            self.busSes = dbus.SessionBus()
        except dbus.DBusException:
            KMessageBox.error(self, ("Unable to connect to DBus."), ("DBus Error"))
            return False
        return True
    
    def setup(self):
        self.queryOptions()
        self.querySystems()
        self.queryEntries()
        self.listenSignals()
    
    def callMethod(self, method, action):
        ch = CallHandler("grub", "Boot.Loader", method,
                         action,
                         self.winId(),
                         self.busSys, self.busSes)
        ch.registerError(self.comarError)
        ch.registerAuthError(self.comarError)
        ch.registerDBusError(self.busError)
        ch.registerCancel(self.cancelError)
        return ch

    def cancelError(self):
        message = ("You are not authorized for this operation.")
        KMessageBox.sorry(None, message, ("Error"))

    def busError(self, exception):
        if self.dia:
            return
        self.dia = KProgressDialog(None, "lala",("Waiting DBus..."), ("Connection to the DBus unexpectedly closed, trying to reconnect..."), True)
        self.dia.progressBar().setTotalSteps(50)
        self.dia.progressBar().setTextEnabled(False)
        self.dia.show()
        start = time.time()
        while time.time() < start + 5:
            if self.openBus():
                self.dia.close()
                self.setup()
                return
            if self.dia.wasCancelled():
                break
            percent = (time.time() - start) * 10
            self.dia.progressBar().setProgress(percent)
            qApp.processEvents(100)
        self.dia.close()
        KMessageBox.sorry(None, ("Cannot connect to the DBus! If it is not running you should start it with the 'service dbus start' command in a root console."))
        sys.exit()
    
    def comarError(self, exception):
        if "Access denied" in exception.message:
            message = ("You are not authorized for this operation.")
            KMessageBox.sorry(self, message, ("Error"))
        else:
            KMessageBox.error(self, str(exception),("COMAR Error"))
    
    def listenSignals(self):
        self.busSys.add_signal_receiver(self.handleSignals, dbus_interface="tr.org.pardus.comar.Boot.Loader", member_keyword="signal", path_keyword="path")
    
    def handleSignals(self, *args, **kwargs):
        path = kwargs["path"]
        signal = kwargs["signal"]
        if not path.startswith("/package/"):
            return
        if signal == "Changed":
            if args[0]== "entry":
                self.queryEntries()
                if self.widgetEditEntry.entry and not self.widgetEditEntry.saved:
                    KMessageBox.information(self, ("Bootloader configuration changed by another application."), ("Warning"))
                    self.widgetEditEntry.slotExit()
                if not self.widgetEntries.tab_2.listBusy:
                    self.widgetEntries.tab_2.listUnused()

    
    def showScreen(self, label):
        screen = self.screens.index(label)
        self.stack.raiseWidget(screen)
    
    def queryOptions(self):
        def handler(options):
            for key, value in options.iteritems():
                self.options[key] = value
            # Default entry
            if self.options["default"] == "saved":
                self.widgetEntries.tab.checkSaved.setChecked(True)
            # Timeout
            timeout = int(self.options["timeout"])
            self.widgetEntries.tab.setTimeoutSlot(False)
            self.widgetEntries.tab.spinTimeout.setValue(timeout)
            self.widgetEntries.tab.setTimeoutSlot(True)
        ch = self.callMethod("getOptions", "tr.org.pardus.comar.boot.loader.get")
        ch.registerDone(handler)
        ch.call()
    
    def querySystems(self):
        def handler(systems):
            self.systems = {}
            for name, info in systems.iteritems():
                label, fields_req, fields_opt = info
                fields = fields_req + fields_opt
                self.systems[name] = (label, fields)
        ch = self.callMethod("listSystems", "tr.org.pardus.comar.boot.loader.get")
        ch.registerDone(handler)
        ch.call()
    
    def queryEntries(self):
        def handler(entries):
            self.widgetEntries.tab.listEntries.clear()
            self.entries = []
            for entry in entries:
                index = int(entry["index"])
                pardus = entry["os_type"] == "linux" and getRoot() == entry["root"]
                self.entries.append(entry)
                item = self.widgetEntries.tab.listEntries.add(self.widgetEditEntry, index, unicode(entry["title"]), entry["root"],  pardus, entry)
        self.widgetEntries.tab.listEntries.setEnabled(True)
        ch = self.callMethod("listEntries", "tr.org.pardus.comar.boot.loader.get")
        ch.registerDone(handler)
        ch.call()

def I18N_NOOP(str):
    return str

def getIconSet(name, group=KIcon.Toolbar):
    return KGlobal.iconLoader().loadIconSet(name, group)

class HelpDialog(QDialog):
    def __init__(self, name, title, parent=None):
        QDialog.__init__(self, parent)
        self.setCaption(title)
        self.layout = QGridLayout(self)
        self.htmlPart = KHTMLPart(self)
        self.resize(500, 600)
        self.layout.addWidget(self.htmlPart.view(), 1, 1)

        lang = locale.setlocale(locale.LC_MESSAGES)
        if '_' in lang:
            lang = lang.split('_', 1)[0]
        url = locate('data', '%s/help/%s/main_help.html' % (name, lang))
        if not os.path.exists(url):
            url = locate('data', '%s/help/en/main_help.html' % name)
        self.htmlPart.openURL(KURL(url))

def getRoot():
    import os
    for mount in os.popen("/bin/mount").readlines():
        mount_items = mount.split()
        if mount_items[2] == "/":
            return mount_items[0]

mod_name = 'Boot Manager2'
mod_app = 'boot-manager2'
mod_version = '0.3.3'

def AboutData():
    about_data = KAboutData(
        mod_app,
        mod_name,
        mod_version,
        I18N_NOOP('Boot Manager2'),
        KAboutData.License_GPL,
        '(C) 2006-2007 UEKAE/TÜBİTAK',
        None,
        None,
        'bugs@pardus.org.tr'
    )
    about_data.addAuthor("Fatma Ekici", I18N_NOOP("Current Maintainer"), "rhytm16@yahoo.com")
    return about_data

def attachMainWidget(self):
    KGlobal.iconLoader().addAppDir(mod_app)
    self.mainwidget = widgetMain(self)
    toplayout = QVBoxLayout(self, 0, KDialog.spacingHint())
    toplayout.addWidget(self.mainwidget)
    self.aboutus = KAboutApplication(self)


class Module(KCModule):
    def __init__(self, parent, name):
        KCModule.__init__(self, parent, name)
        KGlobal.locale().insertCatalogue(mod_app)
        self.config = KConfig(mod_app)
        self.setButtons(KCModule.Apply)
        self.aboutdata = AboutData()
        attachMainWidget(self)

    def aboutData(self):
        return self.aboutdata


# KCModule factory
def create_boot_manager(parent, name):
    global kapp

    kapp = KApplication.kApplication()
    if not dbus.get_default_main_loop():
        dbus.mainloop.qt3.DBusQtMainLoop(set_as_default=True)
    return Module(parent, name)


# Standalone
def main():
    global kapp
    global win

    about = AboutData()
    KCmdLineArgs.init(sys.argv, about)
    KUniqueApplication.addCmdLineOptions()

    if not KUniqueApplication.start():
        print ('Boot Manager is already started!')
        return

    kapp = KUniqueApplication(True, True, False)
    
    dbus.mainloop.qt3.DBusQtMainLoop(set_as_default=True)
    
    win = QDialog()
    win.setCaption(('Boot Manager'))
    win.resize(QSize(650, 475).expandedTo(win.minimumSizeHint()))
    attachMainWidget(win)
    kapp.setMainWidget(win)
    sys.exit(win.exec_loop())


if __name__ == '__main__':
    main()
