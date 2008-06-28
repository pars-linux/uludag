#!/bin/bash

sudo hav call wireless_tools Net.Link setConnection "pardus-2" "pci:8086_4220_eth0"
sudo hav call wireless_tools Net.Link setConnectionMode "pardus-2" "ad-hoc"
sudo hav call wireless_tools Net.Link setAddress "pardus-2" "manual" "192.168.3.1" "255.255.255.0" ""
sudo hav call wireless_tools Net.Link setRemote "pardus-2" "staj-adhoc-test" ""
sudo hav call wireless_tools Net.Link setAuthentication "pardus-2" "wep" "" "1234567898"
sudo hav call wireless_tools Net.Link setState "pardus-2" "up"
