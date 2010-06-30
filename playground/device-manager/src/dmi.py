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
        self.__props = [
                    "bios_date",
                    "bios_vendor",
                    "bios_version",
                    "board_asset_tag",
                    "board_name",
                    "board_serial",
                    "board_vendor",
                    "board_version",
                    "chassis_asset_tag",
                    "chassis_serial",
                    "chassis_type",
                    "chassis_vendor",
                    "chassis_version",
                    "modalias",
                    "product_name",
                    "product_serial",
                    "product_uuid",
                    "product_version",
                    "sys_vendor",
                ]

        # Parse DMI data
        self.__parse_dmi_data()

    def __parse_dmi_data(self):
        """Traverse /sys/class/dmi to provide BIOS DMI informations."""
        for key in self.__props:
            try:
                self.__dict__[key] = open(os.path.join(self.__sysfs_dmi_path,
                    key), "r").read().strip()
            except IOError:
                self.__dict__[key] = ""
