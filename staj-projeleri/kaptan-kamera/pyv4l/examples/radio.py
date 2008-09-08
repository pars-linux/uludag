#!/usr/bin/env python
# Sample radio implementation for PyV4L 0.3+ - By Michael Dove <pythondeveloper@optushome.com.au>
import v4l
import sys
from string import atoi

__author__ = "Michael Dove <pythondeveloper@optushome.com.au>"

if len(sys.argv) > 0:
    device = '/dev/radio'
    radio = v4l.radio(device)

try:
    if sys.argv[0] == '-m':
	radio.mute()
    else:
	radio.setFrequency(atoi(sys.argv[0]))
except:
    print "Usage: radio.py [-m] | [frequency Khz]"
    sys.exit(1)

	



