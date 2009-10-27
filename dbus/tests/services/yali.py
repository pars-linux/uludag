from pardus.serviceutils import *
import os

serviceType = "script"
serviceDesc = "Yet Another Linux Installer"
serviceDefault = "on"

def has_livecd():
    if "livecd" in open("/proc/cmdline", "r").read() or "livedisk" in open("/proc/cmdline", "r").read():
        return True
    return False

def start(boot=False):
    if not has_livecd():
        fail("Not in CD root.")

    call("System.Service.start", "acpid")

    if not boot and run("/sbin/zorg") != 0:
        fail("Not starting as zorg returned an error")

    loadEnvironment()
    os.environ["XAUTHLOCALHOSTNAME"]=os.uname()[1]
    os.environ["HOME"]="/root"
    os.environ["USER"]="root"
    # if 0 == run("/usr/bin/xinit /usr/bin/yali-bin -- tty6 vt7 -nolisten tcp -br"):
    if 0 == run("/usr/bin/xinit /usr/bin/yali-bin -- vt7 -nolisten tcp -br"):
        notify("System.Service.changed", "started")

def stop():
    if not has_livecd():
        fail("Not in CD root.")

    if 0 == run("/usr/bin/killall yali-bin"):
        notify("System.Service.changed", "stopped")

def ready():
    if is_on() == "on":
        if run("/sbin/zorg --boot") != 0:
            fail("Not starting as zorg returned an error")

        start(boot=True)
