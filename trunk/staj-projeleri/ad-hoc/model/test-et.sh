#!/bin/bash

hav call wireless_tools Net.Link setConnection "pardus-2" "usb:148f_2573_wlan0"
hav call wireless_tools Net.Link setConnectionMode "pardus-2" "ad-hoc"
hav call wireless_tools Net.Link setAddress "pardus-2" "manual" "192.168.3.1" "255.255.255.0" ""
hav call wireless_tools Net.Link setRemote "pardus-2" "staj2008" ""
hav call wireless_tools Net.Link setAuthentication "pardus-2" "wep" "" "1234567898"
hav call wireless_tools Net.Link setState "pardus-2" "up"
