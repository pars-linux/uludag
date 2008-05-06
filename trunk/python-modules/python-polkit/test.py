#!/usr/bin/python
# -*- coding: utf-8 -*-

import pypolkit

print "= " * 20

i = 0
for action_id in pypolkit.action_list():
    print pypolkit.action_info(action_id)
    print "- " * 20
    i += 1
    if i > 5:
        break

print "= " * 20

print pypolkit.auth_list_uid(1000)

print "= " * 20

print pypolkit.auth_list_all()
