# -*- coding: utf-8 -*-

from kdeui import *

class NewPackageWizard(KWizard):
    def __init__(self, *args):
        KWizard.__init__(*args)
        
        #add the required pages