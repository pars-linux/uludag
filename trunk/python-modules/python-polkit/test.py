#!/usr/bin/python
# -*- coding: utf-8 -*-

import pypolkit

for action_id in pypolkit.action_list():
    print pypolkit.action_info(action_id)
    print "- " * 20
