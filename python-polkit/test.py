import polkit
import os

for action_id in polkit.action_list():
    print action_id
    print polkit.action_info(action_id)
    print "= " * 20
