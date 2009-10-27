from pardus.serviceutils import *

serviceType = "server"
serviceDefault = "off"

serviceDesc = _({"en": "Network UPS Tools",
                 "tr": "UPS Ağ Araçları"})


piddir = "/var/lib/nut"
model = config.get("MODEL", "upsdrvctl")
server = config.get("SERVER", "no")


@synchronized
def start():
    startDependencies("hal")

    error = 0
    if server == "yes":
        if model == "upsdrvctl":
            error = run("/usr/sbin/upsdrvctl start")
        else:
            error = run("/lib/nut/%s %s %s" % (model, \
                                              config.get("MODEL_OPTIONS", ""), \
                                              config.get("DEVICE", "")))

        if error:
            fail("Could not start model %s" % model)
        else:
            error = startService(command="/usr/sbin/upsd",
                                  args=config.get("UPSD_OPTIONS", ""),
                                  pidfile="%s/upsd.pid" % piddir,
                                  donotify=False)

    if error:
        fail("Could not start UPSD server")
    else:
        startService(command="/usr/sbin/upsmon",
                     pidfile="%s/upsmon.pid" % piddir,
                     donotify=True)

@synchronized
def stop():
    error = stopService(command="/usr/sbin/upsmon",
                        donotify=False)

    if server == "yes":
        if error:
            fail("Could not stop upsmon")
        else:
            error = stopService(command="/usr/sbin/upsd",
                                  pidfile="%s/upsd.pid" % piddir,
                                  donotify=False)

        if not error and server == "yes":
            if model == "upsdrvctl":
                error = run("/usr/sbin/upsdrvctl stop")
            else:
                error = stopService(command="/lib/nut/%s" % model)

    if not error:
        notify("System.Service.changed", "stopped")
    else:
        fail()


def status():
    return isServiceRunning(command="/usr/sbin/upsmon")

