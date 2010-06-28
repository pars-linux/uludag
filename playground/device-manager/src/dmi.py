#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2010 Ozan Çağlayan <ozan@pardus.org.tr>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# dmi.py: Class which parses and provides BIOS DMI data through
#         /sys/class/dmi/data


import os

class DMI(object):
    """Class implementing BIOS DMI."""
    def __init__(self):
        """DMI class constructor."""
        self.__sysfs_dmi_path = "/sys/class/dmi/id"

        # Provided DMI informations
        self.bios_date = ""
        self.bios_vendor = ""
        self.bios_version = ""
        self.board_asset_tag = ""
        self.board_name = ""
        self.board_serial = ""
        self.board_vendor = ""
        self.board_version = ""
        self.chassis_asset_tag = ""
        self.chassis_serial = ""
        self.chassis_type = ""
        self.chassis_vendor = ""
        self.chassis_version = ""
        self.modalias = ""
        self.product_name = ""
        self.product_serial = ""
        self.product_uuid = ""
        self.product_version = ""
        self.sys_vendor = ""

        # Parse DMI data
        self.__parse_dmi_data()

    def __parse_dmi_data(self):
        """Traverse /sys/class/dmi to provide BIOS DMI informations."""
        dmi_dict = {}
        for _file in [_f for _f in os.listdir(self.__sysfs_dmi_path) if not \
                _f.startswith(("uevent", "power", "subsystem"))]:
            dmi_dict[_file] = open(os.path.join(self.__sysfs_dmi_path,
                                                _file), "r").read().strip()

        self.__dict__.update(dmi_dict)
