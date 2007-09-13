__version__ = '0.0'
__author__  = ['Baris Can Daylik']

from qt import *

import sip

import _extractor

def average(image):
    return _extractor.average(sip.voidptr(sip.unwrapinstance(image)))

def extract(image,maxDiff,rgb,minSize):
    return _extractor.extract(sip.voidptr(sip.unwrapinstance(image)),maxDiff,rgb,minSize)
    
def nextImage(image):
    return _extractor.nextImage(sip.voidptr(sip.unwrapinstance(image)))
