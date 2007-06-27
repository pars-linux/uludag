#!/usr/bin/python

import partition
import modules

# Search partitions and find users:
users = []      # user1 = (partition, type, username, userdir)
partitions = partition.getPartitions()
for part in partitions:
    if partition.isWindowsPart(part):
        users.extend(partition.getWindowsUsers(part))

# List users
for no,user in enumerate(users):
    print no, user
no = input("Choose an operating system and user:")

partition, parttype, username, userdir = users[no]
myMigration = modules.UserMigration(partition, parttype, userdir)