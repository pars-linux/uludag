# -*- coding: utf-8 -*-

"""This module for rescue Windows and Grub bootloaders"""

from shell_tools import run_quiet
from os import chmod
from pardus import procutils



def install_grub(pardus_disk, option):
    """This function for rescue Grub bootloaders"""
    root_path = "(%s,%s)" % (pardus_disk[0], pardus_disk[1])
    if option == 0:
        setupto = "(%s)" % pardus_disk[0]
    elif option == 1:
        setupto = "(%s,%s)" % (pardus_disk[0], pardus_disk[1])
    elif option == 2:
        setupto = "(%s)" % pardus_disk[2]

    batch_template = """root %s
setup %s
quit
""" % (root_path, setupto)

    shell = """#!/bin/bash
grub --no-floppy --batch < /tmp/_grub"""

    temp =  file('/tmp/_grub', 'w')
    temp.write(batch_template)
    temp.close()
    temp =  file('/tmp/grub.sh', 'w')
    temp.write(shell)
    temp.close()
    chmod('/tmp/grub.sh', 0100)

    procutils.run_quiet("/tmp/grub.sh")

def install_windows_bootloader(windows):
    """This module for rescue Windows bootloaders"""
    run_quiet("install-mbr  -i n -p D -t  %d %s" % (windows[1], windows[0]))
