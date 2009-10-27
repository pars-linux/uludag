from pardus.serviceutils import *

serviceType = "server"
serviceDesc = _({"en": "DHCP Daemon",
                 "tr": "DHCP Sunucusu"})
serviceConf = "dhcpd"

@synchronized
def start():
    startService(command="/usr/sbin/dhcpd",
                 args="-user dhcp -group dhcp %s %s" % (config.get("DHCPD_IFACE", ""), config.get("DHCPD_OPTS", "")),
                 pidfile="/var/run/dhcp/dhcpd.pid",
                 donotify=True)

@synchronized
def stop():
    stopService(command="/usr/sbin/dhcpd",
                pidfile="/var/run/dhcp/dhcpd.pid",
                donotify=True)

def status():
    return isServiceRunning("/var/run/dhcp/dhcpd.pid")
