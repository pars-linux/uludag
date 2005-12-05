#!/bin/sh 

# Copyright (c) 2004, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This small software collects hardware information
# Usage: ./gethwinformation.sh [token]
# 
# Where token is one of: 
#  
# cpupower
# modelname
# totalmemory
# harddisk
# lspci
# modules
# oi

if [ -z "$1" ] 
then
echo 
echo "This small program collects hardware information"
echo "which are not considered to be confidential." 
echo "TUBITAK/UEKAE respects your privacy."
echo 
echo "Usage: ./gethwinformation.sh [token]"
echo  
echo "Where token is one of: "
echo   
echo "cpupower"
echo "modelname"
echo "totalmemory"
echo "harddisk"
echo "lspci"
echo "modules"
echo "oi"
fi 

RAND1=$RANDOM
RAND2=$RANDOM
RAND3=$RANDOM 

# Get CPU power 
cpupower=$(cat /proc/cpuinfo  |grep -i Mhz| cut -d: -f 2) 

# Get CPU model
modelname=$(cat /proc/cpuinfo  |grep -i 'model name'| cut -d: -f 2) 

# What is our memory?
totalmemory=$(cat /proc/meminfo |grep -i 'MemTotal'| cut -d: -f 2) 

# How did you partition your hard disk?
fdisk -l > /tmp/$RAND3

# How about hardware?
lspci > /tmp/$RAND1

# What modules are installed?
cat /proc/modules > /tmp/$RAND2 

# Print everything 

if [ "$1" == "cpupower" ] 
then
echo $cpupower
fi 

if [ "$1" == "modelname" ] 
then
echo $modelname
fi

if [ "$1" == "totalmemory" ] 
then
echo $totalmemory
fi

if [ "$1" == "harddisk" ] 
then
cat /tmp/$RAND3
fi

if [ "$1" == "lspci" ] 
then
cat /tmp/$RAND1 
fi

if [ "$1" == "modules" ] 
then
cat /tmp/$RAND2
fi

if [ "$1" == "oi" ] 
then
echo "oi!"
fi


# Clean up 
rm -f /tmp/$RAND1 
rm -f /tmp/$RAND2
rm -f /tmp/$RAND3
