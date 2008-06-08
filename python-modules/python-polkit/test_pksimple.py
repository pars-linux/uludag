import polkit
import os

action_ids = ("org.freedesktop.hal.device-access.camera", "org.gnome.clockapplet.mechanism.configurehwclock")

for a in action_ids:
    print a, polkit.check_auth(os.getpid(), a)

print "= " * 20
print action_ids, polkit.check_auth(os.getpid(), *action_ids)
print "= " * 20
print action_ids, polkit.check_authv(os.getpid(), action_ids)
print "= " * 20
print "org.freedesktop.hal.device-access.camera", polkit.check_auth(os.getpid(), "org.freedesktop.hal.device-access.camera")
print "= " * 20

print polkit.auth_obtain("org.gnome.clockapplet.mechanism.configurehwclock", 0, os.getpid())
