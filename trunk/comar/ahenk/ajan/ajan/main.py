#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import Queue
import logging

import ajan.config
import ajan.policy

def start(debug=False):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    
    logging.debug("Ajan started")
    ajan.config.load()
    
    result_queue = Queue.Queue(0)
    apply_queue = Queue.Queue(0)
    
    # This thread modifies the system according to current policy
    applier = ajan.policy.Applier(apply_queue, result_queue)
    applier.start()
    
    # This thread periodically checks central policy changes
    fetcher = ajan.policy.Fetcher(result_queue)
    fetcher.start()
    
    # Serve forever
    logging.debug("Entering main loop")
    while True:
        op, data = result_queue.get()
        
        logging.debug("CMD %s" % str(data))
        if op == "policy":
            apply_queue.put(data)
