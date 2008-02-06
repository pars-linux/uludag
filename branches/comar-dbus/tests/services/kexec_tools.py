from pardus.serviceutils import *

serviceType = "script"
serviceDesc = _({"en": "KExec Tools",
                 "tr": "KExec Araçları"})
serviceConf = "kexec"

@synchronized
def start():
    kname = config.get("KNAME", "latestkernel")
    rootpart = config.get("ROOTPART", [i.split(" ")[0] for i in open("/etc/mtab") if i.split(" ")[1] == "/"][0])
    kparam = config.get("KPARAM", "")
    initrdopt = config.get("INITRDOPT", "latestinitramfs")

    if run("/usr/sbin/kexec --load /boot/%s --append=\"root=%s %s\" --initrd=/boot/%s" % (kname, rootpart, kparam, initrdopt)) == 0:
        notify("System.Service.changed", "started")
    else:
        fail("kexec failed!")

@synchronized
def stop():
    # Stop only if we are not rebooting
    whereWeAre = run("/sbin/runlevel").stdout.split()[1].strip()

    if whereWeAre != "6":
        if run("/usr/sbin/kexec -u") == 0:
            notify("System.Service.changed", "stopped")
        else:
            fail("kexec failed!")

def status():
    return int(file("/sys/kernel/kexec_loaded").read().strip())
