# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'goodbyedlg.ui'
#
# Created: Sal Oca 24 19:45:13 2006
#      by: The PyQt User Interface Compiler (pyuic) snapshot-20051013
#
# WARNING! All changes made in this file will be lost!


from qt import *
from kdecore import *
from kdeui import *


image0_data = \
    "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
    "\x49\x48\x44\x52\x00\x00\x00\x20\x00\x00\x00\x20" \
    "\x08\x06\x00\x00\x00\x73\x7a\x7a\xf4\x00\x00\x08" \
    "\x8a\x49\x44\x41\x54\x58\x85\xe5\x97\x61\x6c\x5b" \
    "\xd5\x19\x86\x9f\x5b\x6e\xc6\x75\xeb\xb4\x36\x0a" \
    "\xd3\xb5\xd4\x6a\x31\x6d\x51\x6f\xd6\x6e\xbd\x16" \
    "\x99\xb0\x0b\x88\x64\x2b\x1a\xae\x82\x44\xca\x7e" \
    "\x2c\x11\xda\x68\x80\x69\xcb\x80\xa1\x54\x48\x5b" \
    "\x5b\xa6\x89\x0e\x36\xda\x52\x75\x34\x8c\x69\x38" \
    "\x8c\x95\x84\x69\xb4\xa9\x58\xa9\x33\xd1\xd6\x46" \
    "\xa5\xdc\x3b\xb5\x60\x57\x6d\xa9\x2b\xd2\x71\x3d" \
    "\x1a\x25\x51\x95\xf5\x5e\x88\x15\x9f\xd2\x0b\x67" \
    "\x3f\xec\x98\xa4\x2b\xb0\xfd\xda\x8f\x9d\x3f\x47" \
    "\xc7\xc7\xfa\xde\xf7\xfb\xbe\xf7\x3d\xe7\x5c\xf8" \
    "\x7f\x1f\xca\x95\x7e\x94\x52\xce\xc1\x2d\xdf\xc2" \
    "\x91\x3e\x93\x60\x63\x1d\xe7\x6c\xb8\xd6\x00\xc7" \
    "\x82\x6b\x63\xe0\x64\x20\x64\xc2\x88\x0d\x21\x03" \
    "\x8a\x16\x34\xc4\x60\xc4\x82\x06\x60\x44\x80\x5e" \
    "\xdd\xd7\xe1\xb4\x1f\xfd\xa0\xe9\x81\x9d\x7f\x55" \
    "\xae\xbf\xee\x1f\x5f\x48\x40\x9e\x38\xb4\x14\xa1" \
    "\xf5\x31\x9c\x59\x45\x34\xa1\x30\x62\xc1\x42\xad" \
    "\x12\x74\x61\x02\xc6\x2d\xd0\x35\x18\x07\xf4\xd8" \
    "\xa7\xeb\xcf\xdb\x77\x05\x4e\xb1\x50\x8e\x7a\x62" \
    "\x07\x9b\x76\x3e\xaa\x7c\xf9\xba\x4b\x57\x24\x20" \
    "\xdf\x7f\x47\x67\xdc\x3b\x42\x31\xb3\x98\x90\x01" \
    "\x85\x0c\x34\x34\x55\x33\x34\xa0\x68\x57\x32\x2f" \
    "\x66\x2a\x20\xc5\x6a\xa6\xc5\x4a\xa6\xd6\x88\xc0" \
    "\xd4\x4d\xc4\xb9\x3c\x00\x96\x5f\x26\xa1\x26\xd0" \
    "\xea\x0b\x04\xbe\xd5\x05\x25\x47\xe2\x69\x4f\xf3" \
    "\xb3\xcd\x0f\x29\x8a\x72\x05\x02\x27\xde\xde\xce" \
    "\xc9\xf4\x4f\xf0\xc6\x28\x97\x3c\x02\x42\x50\x16" \
    "\x82\x80\x5f\xae\xae\xa1\x5c\x72\x09\x5c\x02\x47" \
    "\x08\xa2\x68\x58\x42\x60\xf8\x60\xf9\x82\x26\x1f" \
    "\x32\xbe\x20\x0e\x64\x7d\x41\x5c\xd5\xb0\x7d\x81" \
    "\x09\x58\x3e\x74\x35\xc7\xf1\x1a\x23\x7e\xb4\xa1" \
    "\xa3\x59\x79\xe8\xae\xe3\x00\x57\xcd\xe8\xbb\xc2" \
    "\xd1\xc1\x67\xb9\x3a\x12\xe2\xfc\x30\x75\x5f\xb9" \
    "\x05\x9a\x6f\xa6\x6e\xc5\x1d\x70\xf6\x18\x75\x73" \
    "\x0d\x38\x7f\x96\xba\x8b\x75\xe0\xfb\x84\x17\xdf" \
    "\x06\x0b\x02\x2c\xba\xb9\x83\xc2\x64\x91\xeb\x4b" \
    "\x82\xc3\xa2\x44\xb3\xaa\x61\x7f\xe2\xd3\x3c\x47" \
    "\x65\xcc\x30\xe9\xfc\xf1\xb3\x9c\x6b\x08\xb1\xe8" \
    "\xcc\x49\xfe\x32\x52\x64\xcd\xd7\xf5\x39\xd6\xf1" \
    "\x03\xe7\xfb\x4e\x8d\xbf\x7e\xb9\xf0\xe6\xca\xfe" \
    "\x57\xcb\x53\x3b\xd6\x49\xb9\x63\x9d\x94\xa3\xef" \
    "\x49\xf9\xde\xa8\x94\xb9\x43\x52\x4a\x29\xe5\xe1" \
    "\xdd\x52\xf6\xbe\x28\xa7\xd2\xcf\x49\x39\x25\xa5" \
    "\x9c\x9a\x92\xf2\x23\x29\xa7\xa6\xf7\xcf\x8f\x4a" \
    "\xf9\xde\xa8\x7c\x67\x47\x8f\x94\x3f\x5d\x27\xa7" \
    "\x72\x6f\x4a\x29\xa5\x7c\x7b\x5b\x8f\x94\x1f\x4a" \
    "\xf9\xf6\xaf\x7b\xe4\xa1\x65\xc8\x9d\xcb\x35\x39" \
    "\x75\x77\xfc\xf9\x69\x5c\x75\x06\x87\xb9\x94\xb2" \
    "\x75\x81\x86\x18\x44\x42\xa0\x45\x61\x7b\x6b\x45" \
    "\xe5\x2f\x6d\x83\x27\xf7\xc3\x32\x08\x9c\xcd\xc1" \
    "\x13\x9d\x20\x1c\x32\xb6\x83\x01\xa4\x85\xa0\x55" \
    "\x8f\xe0\xac\x30\x89\xb5\x6d\x80\x1b\x9a\x08\x1c" \
    "\xcc\xd0\xbb\x22\x80\x09\xf4\x0f\xed\xa1\xf3\x80" \
    "\x43\xef\xde\x7e\x0c\x6f\x9c\xf4\xa4\x57\x3f\x0d" \
    "\x3a\xa7\x06\x3f\xe9\xd6\x23\xca\x4a\xb9\x68\x81" \
    "\x1a\x01\x2f\x07\x3e\x94\x47\x6c\x50\x35\x98\x74" \
    "\x61\xe4\x34\x04\x05\x9c\xc9\x33\xb6\xb2\xbd\xd2" \
    "\x5b\x21\x30\x80\xc1\x11\x07\x86\x06\xe9\xbd\xff" \
    "\xab\xf0\xdb\x3d\xb8\xc1\x32\x26\x02\xcb\x17\x24" \
    "\xb4\x00\xe5\xe1\x1c\x66\xc9\xc3\xf2\xc1\x28\x95" \
    "\x17\x48\x29\x2f\x23\x50\x1f\x0e\x22\x84\x12\xd0" \
    "\x4d\x38\xd0\x0b\xd1\x18\xb4\x75\x13\xd0\x35\xb8" \
    "\xb3\x1b\xce\x38\xb0\x6f\x1b\x8c\x0b\x2c\xd7\x25" \
    "\xb4\xab\x17\xcb\x17\xc4\x54\xc8\x57\x05\x97\xf7" \
    "\x21\xae\x6a\xa4\x76\xdd\x4b\xf8\xc6\x35\xb8\xcd" \
    "\x2d\x24\x1b\x0d\xa2\x4f\xed\x26\x90\xcd\x93\x11" \
    "\x15\x41\xe6\x85\x08\x4d\x1b\xa0\xe6\x02\x79\xe2" \
    "\xd0\x4d\xec\x4b\x1d\x2e\x0b\x4f\x09\xf8\x50\x0e" \
    "\xe9\x04\x1e\x49\x55\x32\xaf\x0f\xe3\x3e\xda\x49" \
    "\xf8\xe1\x7e\x72\x1d\x51\x62\x2d\x49\xf6\xef\x1d" \
    "\x20\x06\xb5\xa0\xb6\x0f\xa6\x4a\x4d\xf5\xb4\x75" \
    "\x90\x78\xbc\x1f\xca\x65\x98\x10\x6c\xbd\xed\x1a" \
    "\x0c\x1f\xf2\x40\x52\x6f\x7c\x37\x96\xce\x35\x29" \
    "\xf3\xaf\xf9\xf8\xd3\x0a\x68\xd1\x6b\xf0\x85\x12" \
    "\xd0\xe3\x20\xca\x04\xfc\x02\x1c\xe8\x87\xfa\x30" \
    "\xfc\x71\x2b\xe1\xbc\xc5\xe9\x75\x4d\xc4\x7c\x70" \
    "\x87\x06\x89\xa9\x1a\x19\x1f\x4c\x55\xc3\x66\x26" \
    "\x78\xa5\x12\x0c\x0d\xc2\x70\x0e\x02\x01\xfa\xef" \
    "\x5f\x45\x8c\x0a\xb8\x09\xd8\x88\x79\x10\x56\x66" \
    "\x8b\xf0\x54\x7a\x3e\x23\x63\xec\x7f\x23\x47\x64" \
    "\xc2\x23\xed\x79\x74\x15\x23\x84\x96\x25\xc8\x3c" \
    "\xb6\x09\xdb\x17\x84\x34\x8d\xac\x0a\x49\x4d\x23" \
    "\xa7\x56\x83\x55\x7d\x6f\x53\x29\xbf\x2d\x04\xa6" \
    "\x5a\xd5\xc6\xf6\x4d\x84\x7f\xf1\x1c\x91\x11\x07" \
    "\xcb\xaf\xc0\xd8\x3e\x24\x7d\xe6\x71\x70\xeb\x55" \
    "\x80\x5f\xab\xc0\x58\x7e\x6c\xfe\xfa\x21\x1b\x71" \
    "\xb6\xc8\xc0\x84\x87\x01\x44\xda\xda\x11\x7b\x33" \
    "\x64\x85\xa0\x35\x18\x22\xba\xcc\xa0\xfb\xd1\x17" \
    "\x89\x3e\xfe\x1c\x6b\x0f\xbb\x64\xab\x19\x89\xb6" \
    "\x76\xba\xd2\x17\x88\xf5\x5d\xa0\xfb\xbe\x2d\xb8" \
    "\x4b\x0c\x12\x9a\x46\x2a\x9b\x06\x35\x82\x6b\xc6" \
    "\x2b\x6d\x01\xe2\x2a\xe4\x4b\x5e\x80\xc6\xe4\xd5" \
    "\xb3\x2a\x60\x9d\x4c\xcf\x8f\xab\x15\x86\x5a\x75" \
    "\x5e\xbb\xac\x95\xf4\x4b\x6b\xd1\x54\x48\x7b\x1e" \
    "\xf1\xe3\x79\xd6\xbf\x75\x17\x9a\x0a\x1d\x3f\xec" \
    "\xa1\xd1\x13\x0c\x08\xc1\x06\x4f\xb0\xa7\x67\x15" \
    "\x91\x42\x01\x4b\x88\x5a\x51\x63\x80\x73\x24\x45" \
    "\xb2\x21\xc2\xb6\x9a\x46\x20\x24\xf8\x92\xeb\x39" \
    "\x73\x81\x0f\x6b\x15\x48\x94\x44\xc8\xf6\x2b\x0c" \
    "\x45\x75\xe6\x78\x9a\xe4\x0d\x9d\xb5\xf5\xcc\xfd" \
    "\xa6\x15\x2d\x64\x85\x20\xae\xc2\xc0\x31\x8b\xe4" \
    "\xad\xdd\x64\x4a\x82\x84\xaa\x01\xd0\x79\x7b\x1c" \
    "\x47\x6f\x24\x7a\x63\x17\xe9\x71\xa7\x06\x1e\x07" \
    "\x3c\x5f\x28\xe1\x85\xb1\xfa\x59\x36\x4c\x43\x58" \
    "\x9b\x01\x62\xfb\x50\x76\x0a\x38\xc1\x72\xa5\xc7" \
    "\x3e\x68\x50\xb5\x1a\xec\xd9\xf5\xcb\x5a\x4f\xf5" \
    "\x09\x8f\xc1\x83\x29\x84\x0f\xe9\x92\xa0\x55\x6f" \
    "\x24\xe7\x69\x98\xbe\x00\xd5\x25\x32\xec\x60\x57" \
    "\x35\x90\xf5\xc1\xf4\x61\xec\x78\xff\x6c\x02\xa6" \
    "\x1a\x9f\x7f\x79\xa6\xe9\x53\x05\x62\xab\xbb\xaa" \
    "\x02\x03\x2d\xa8\xd1\xfd\xdd\x16\x6c\x1f\x5a\x57" \
    "\xb6\xb3\xb5\x6f\x37\x5b\x5f\x1b\x65\xed\x33\x2f" \
    "\x12\x75\x1c\x84\x0f\x3d\xf7\x6c\xc0\x06\xd6\xdc" \
    "\xde\x43\x6c\x75\x3b\x84\xc3\xa4\x27\xc6\x2b\x5a" \
    "\x99\x8e\x0f\x44\xc6\xc4\x6c\x02\xb6\xc8\x2c\xa8" \
    "\x69\xa0\x9a\x59\xf8\xa4\x05\x41\x81\x1e\x0a\x61" \
    "\xfb\xb0\xf1\x81\xfd\x64\x8a\x95\x1e\xa7\x5e\xde" \
    "\x06\xb7\xae\x05\x23\x02\x63\x11\xd2\xe3\xe3\xc4" \
    "\x81\xb1\x25\x11\x4c\x1f\xb6\x3e\x75\x2f\xa8\x09" \
    "\x9c\xbd\x29\xf0\x67\x57\x16\xc0\x19\x4a\x69\xb3" \
    "\x44\x18\x17\x62\xde\xc0\xe5\x15\x98\xf0\x68\x3d" \
    "\x60\xb1\x3e\xed\x82\xef\xc2\xc2\x30\x9d\x91\xcd" \
    "\x24\xf5\x5e\x84\xe6\xd2\x9b\x6c\xa2\xfb\xa9\xfd" \
    "\x6c\x7e\xe2\x9b\x6c\x7e\x78\x0b\x99\xb3\x36\x4d" \
    "\xab\xbb\x61\x45\x37\x89\x85\x80\x77\x9a\xf2\x83" \
    "\xbd\x08\x66\xc7\xb5\x7d\x60\xc2\x53\x61\xc6\x75" \
    "\xfc\x35\x5d\xbd\x5f\x08\xb1\xa8\x38\xe3\x4f\x9a" \
    "\x0a\xe9\xd7\xfe\x8c\xfa\xca\xef\xd0\x16\x87\xa9" \
    "\xd7\xbf\x01\xd7\x87\xe0\xe8\x61\x32\xef\x9c\xe1" \
    "\xdc\x19\x07\x55\x75\x89\xbc\x3b\x4c\xee\xe2\x04" \
    "\x6b\xba\x7e\x05\x8d\x21\x98\xe3\x93\xd9\xf2\x7d" \
    "\x52\x1b\x1e\xe6\xd8\x88\x3d\x2b\x5e\xd1\xaf\x58" \
    "\xf7\x5c\x90\x81\xc1\x51\x7f\xb8\xd6\x82\x8e\x3b" \
    "\x7b\xc6\xaf\xa4\xf6\xa4\xae\xa3\xb5\x25\x19\x7b" \
    "\xc6\xc2\xdd\xd2\x09\xc7\x1d\x02\xf7\xf5\x10\xf5" \
    "\xca\x44\x57\x9a\x24\x5a\xba\xb0\x54\x48\xde\xd4" \
    "\x09\xcb\x63\xf0\xf2\x20\xa9\x75\xab\x30\xd4\x28" \
    "\x3d\xb7\x27\xab\x8f\x92\xd9\xee\x2a\xa8\xd0\xf9" \
    "\xcc\x9b\x53\xb3\x34\xa0\xad\x4e\xec\x4b\x56\x7b" \
    "\x3d\xed\x86\x16\x4d\xc3\x5d\x1a\x25\xbd\xab\x0f" \
    "\xcf\x10\x38\xc7\xf2\x58\x07\x7a\x81\x08\xd1\x27" \
    "\x53\x24\x0d\x93\xcd\x0f\xae\x61\xe3\x6f\x0e\x41" \
    "\x5b\x12\x9e\xdf\xc3\x9e\x83\x29\x92\x4b\xa3\x0c" \
    "\xbe\xd1\x8f\x95\xcd\x20\x96\x1b\x5c\xee\xae\xee" \
    "\xd5\x49\x97\xe5\x46\x6e\x16\x81\x40\x73\xeb\x9f" \
    "\xf4\xfb\xba\x87\x5b\x34\xad\x76\x62\x65\x85\x00" \
    "\xdb\x26\x14\x0a\x11\x3a\x99\xc3\x33\x4d\xc4\xbe" \
    "\x34\x5b\xef\xb8\x8e\xf0\xca\x56\xc2\x37\xb7\x56" \
    "\xc0\x1b\x62\x04\xde\x3a\xcd\xfa\xed\x77\x91\x58" \
    "\xd2\xca\x60\x3e\x47\xd2\x8c\x90\xf5\x3c\xb4\x53" \
    "\xf9\x59\xe7\x48\xfb\x42\x9d\xc8\x3d\x3f\xda\x49" \
    "\x20\xf0\x01\x5c\xfe\x26\xfc\x48\xde\xe4\x3c\xdd" \
    "\x9d\x76\x5f\x1a\xa8\xcf\x94\x3c\xa8\x5a\xc7\x04" \
    "\x8a\x0d\x3a\xed\x86\x41\x6f\x36\x8b\x09\x14\x82" \
    "\x1a\x5d\xf1\x56\x0a\xc1\x10\xd1\x91\x31\x7a\xed" \
    "\x2c\x5a\xb5\xcc\x8f\x7d\xa7\x83\x4d\x2f\x0f\xa0" \
    "\x41\x45\x80\x54\xac\xd7\xd1\xd8\x48\xf4\x91\x8d" \
    "\x87\xc3\x6d\x5d\xdf\x56\x14\xa5\xfc\x6f\x04\xaa" \
    "\x24\x5a\x78\x3d\xf5\x7b\x1c\x77\x31\x43\x7d\x94" \
    "\x3d\x97\x8c\x10\x24\x42\x49\xd2\x13\x83\x18\xfe" \
    "\xa7\xb7\x9e\xe5\x0b\x62\x54\x1e\x9c\x66\xf5\x90" \
    "\x32\x55\x28\x68\x1a\x86\xa0\x7a\x31\x69\x78\x8d" \
    "\x3a\x5d\x77\x6f\xfc\x98\x15\xfa\x5e\x9a\xd7\xfc" \
    "\x40\x51\x94\x0b\xd3\x78\x9f\xf5\x61\xb2\x80\x61" \
    "\x6b\x2d\xc1\xe8\xf7\xf8\x5b\xff\x8d\x9c\x73\xbe" \
    "\x54\x9e\x18\x27\x50\x12\xb8\x25\x97\xb0\x10\x38" \
    "\x93\x2e\x51\x1f\xac\x92\xc0\xf0\x05\x19\x51\x39" \
    "\xfb\x33\xbe\xc0\xf4\xa1\x10\xd2\xe8\x6c\x6e\xc5" \
    "\x8d\xc7\xff\x19\xbe\xb5\xeb\x15\xc4\xd8\x1f\x58" \
    "\xd4\x64\x29\x8a\xf2\xf1\x4c\xac\x2b\x12\x98\x41" \
    "\x44\x01\x96\x51\x28\x77\x10\xf2\x3a\x39\x93\x6e" \
    "\x44\x8f\x2b\x95\xef\x83\x28\x0c\x67\x20\x6c\x54" \
    "\xe6\xa0\x01\xc5\x2c\x34\xb6\x40\x50\x5c\xa2\xa5" \
    "\xfb\x08\x25\xe7\x05\x96\xc6\x5e\x51\x14\xc5\xfb" \
    "\x3c\x9c\xff\x68\x48\x29\xeb\xe4\x47\xf2\x36\x79" \
    "\xe2\xd0\x0b\x72\x74\xf4\xef\xf2\xe8\xab\x17\xe5" \
    "\xfb\xa3\x52\x5a\xbb\xa5\x7c\x7f\xf4\x13\x79\x74" \
    "\xf7\x07\x72\xf4\xc2\x51\x79\xfa\xcd\x9f\x4b\x29" \
    "\x97\x4c\xbf\xf9\xbe\x68\x7c\x6e\x05\x3e\x83\x08" \
    "\x5c\x42\xa5\x8e\x79\x4c\x12\xa6\x1e\x95\x49\xa6" \
    "\xa8\xc7\x05\x2e\x2a\x8a\xf2\xc9\x7f\x1b\xf3\x7f" \
    "\x3a\xfe\x05\xff\x35\x54\x66\xad\xf8\xde\x14\x00" \
    "\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82"

class GoodbyeDlg(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        self.image0 = QPixmap()
        self.image0.loadFromData(image0_data,"PNG")
        if not name:
            self.setName("GoodbyeDlg")

        self.setIcon(self.image0)


        self.goodbyeLabel_2 = QLabel(self,"goodbyeLabel_2")
        self.goodbyeLabel_2.setGeometry(QRect(170,60,400,140))
        self.goodbyeLabel_2.setAlignment(QLabel.WordBreak | QLabel.AlignTop)

        self.goodbyePixmap = QLabel(self,"goodbyePixmap")
        self.goodbyePixmap.setGeometry(QRect(-5,0,142,290))
        self.goodbyePixmap.setScaledContents(1)

        self.languageChange()

        self.resize(QSize(619,288).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(i18n("Feedback Wizard"))
        self.goodbyeLabel_2.setText(i18n("<h2>Thank you</h2>\n"
"We have collected all necessary information in order to send \n"
"to Pardus developers.\n"
"<p>\n"
"Thank you for your support to Pardus operating system."))

