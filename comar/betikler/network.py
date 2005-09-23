#!/usr/bin/python
# -*- coding: utf-8 -*-

import array
import fcntl
import struct
import socket
import sys
import os

class ifconfig:
    """ ioctl stuff """

#   From <bits/ioctls.h>

    IFNAMSIZ = 16               # interface name size

    # Socket configuration controls
    SIOCGIFNAME = 0x8910        # get iface name
    SIOCSIFLINK = 0x8911        # set iface channel
    SIOCGIFCONF = 0x8912        # get iface list
    SIOCGIFFLAGS = 0x8913       # get flags
    SIOCSIFFLAGS = 0x8914       # set flags
    SIOCGIFADDR = 0x8915        # get PA address
    SIOCSIFADDR = 0x8916        # set PA address
    SIOCGIFDSTADDR  = 0x8917    # get remote PA address
    SIOCSIFDSTADDR  = 0x8918    # set remote PA address
    SIOCGIFBRDADDR  = 0x8919    # get broadcast PA address
    SIOCSIFBRDADDR  = 0x891a    # set broadcast PA address
    SIOCGIFNETMASK  = 0x891b    # get network PA mask
    SIOCSIFNETMASK  = 0x891c    # set network PA mask
    SIOCGIFMETRIC = 0x891d      # get metric
    SIOCSIFMETRIC = 0x891e      # set metric
    SIOCGIFMEM = 0x891f         # get memory address (BSD)
    SIOCSIFMEM = 0x8920         # set memory address (BSD)
    SIOCGIFMTU = 0x8921         # get MTU size
    SIOCSIFMTU = 0x8922         # set MTU size
    SIOCSIFNAME = 0x8923        # set interface name
    SIOCSIFHWADDR = 0x8924      # set hardware address
    SIOCGIFENCAP = 0x8925       # get/set encapsulations
    SIOCSIFENCAP = 0x8926
    SIOCGIFHWADDR = 0x8927      # Get hardware address
    SIOCGIFSLAVE = 0x8929       # Driver slaving support
    SIOCSIFSLAVE = 0x8930
    SIOCADDMULTI = 0x8931       # Multicast address lists
    SIOCDELMULTI = 0x8932
    SIOCGIFINDEX = 0x8933       # name -> if_index mapping
    SIOGIFINDEX = SIOCGIFINDEX  # misprint compatibility :-)
    SIOCSIFPFLAGS = 0x8934      # set/get extended flags set
    SIOCGIFPFLAGS = 0x8935
    SIOCDIFADDR = 0x8936        # delete PA address
    SIOCSIFHWBROADCAST = 0x8937 # set hardware broadcast addr
    SIOCGIFCOUNT = 0x8938       # get number of devices
    SIOCGIFBR = 0x8940          # Bridging support
    SIOCSIFBR = 0x8941          # Set bridging options
    SIOCGIFTXQLEN = 0x8942      # Get the tx queue length
    SIOCSIFTXQLEN = 0x8943      # Set the tx queue length

    # ARP cache control calls
    SIOCDARP = 0x8953       # delete ARP table entry
    SIOCGARP = 0x8954       # get ARP table entry
    SIOCSARP = 0x8955       # set ARP table entry

    # RARP cache control calls
    SIOCDRARP = 0x8960      # delete RARP table entry
    SIOCGRARP = 0x8961      # get RARP table entry
    SIOCSRARP = 0x8962      # set RARP table entry

    # Driver configuration calls
    SIOCGIFMAP = 0x8970     # Get device parameters
    SIOCSIFMAP = 0x8971     # Set device parameters

    # DLCI configuration calls
    SIOCADDDLCI = 0x8980   # Create new DLCI device
    SIOCDELDLCI = 0x8981   # Delete DLCI device


#   From <net/if.h>    

    IFF_UP = 0x1           # Interface is up.
    IFF_BROADCAST = 0x2    # Broadcast address valid.
    IFF_DEBUG = 0x4        # Turn on debugging.
    IFF_LOOPBACK = 0x8     # Is a loopback net.
    IFF_POINTOPOINT = 0x10 # Interface is point-to-point link.
    IFF_NOTRAILERS = 0x20  # Avoid use of trailers.
    IFF_RUNNING = 0x40     # Resources allocated.
    IFF_NOARP = 0x80       # No address resolution protocol.
    IFF_PROMISC = 0x100    # Receive all packets.
    IFF_ALLMULTI = 0x200   # Receive all multicast packets.
    IFF_MASTER = 0x400     # Master of a load balancer.
    IFF_SLAVE = 0x800      # Slave of a load balancer.
    IFF_MULTICAST = 0x1000 # Supports multicast.
    IFF_PORTSEL = 0x2000   # Can set media type.
    IFF_AUTOMEDIA = 0x4000 # Auto media select active.


    def __init__(self):
        # create a socket to communicate with system
        self.sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def _ioctl(self, func, args):
        return fcntl.ioctl(self.sockfd.fileno(), func, args)

    def _call(self, ifname, func, ip = None):

        if ip is None:
            data = (ifname + '\0'*32)[:32]
        else:
            ifreq = (ifname + '\0' * self.IFNAMSIZ)[:self.IFNAMSIZ]
            data = struct.pack("16si4s10x", ifreq, socket.AF_INET, socket.inet_aton(ip))

        try:
            result = self._ioctl(func, data)
        except IOError:
            return None

        return result

    def getInterfaceList(self):
        """ Get all interface names in a list """
        # get interface list
        buffer = array.array('c', '\0' * 1024)
        ifconf = struct.pack("iP", buffer.buffer_info()[1], buffer.buffer_info()[0])
        result = self._ioctl(self.SIOCGIFCONF, ifconf)

        # loop over interface names
        iflist = []
        size, ptr = struct.unpack("iP", result)
        for idx in range(0, size, 32):
            ifconf = buffer.tostring()[idx:idx+32]
            name, dummy = struct.unpack("16s16s", ifconf)
            name, dummy = name.split('\0', 1)
            iflist.append(name)

        return iflist

    def getAddr(self, ifname):
        """ Get the inet addr for an interface """
        result = self._call(ifname, self.SIOCGIFADDR)
        return socket.inet_ntoa(result[20:24])

    def getNetmask(self, ifname):
        """ Get the netmask for an interface """
        result = self._call(ifname, self.SIOCGIFNETMASK)
        return socket.inet_ntoa(result[20:24])

    def getBroadcast(self, ifname):
        """ Get the broadcast addr for an interface """
        result = self._call(ifname, self.SIOCGIFBRDADDR)
        return socket.inet_ntoa(result[20:24])

    def getStatus(self, ifname):
        """ Check whether interface is UP """
        result = self._call(ifname, self.SIOCGIFFLAGS)
        flags, = struct.unpack('H', result[16:18])
        return (flags & self.IFF_UP) != 0

    def getMTU(self, ifname):
        """ Get the MTU size of an interface """
        data = self._call(ifname, self.SIOCGIFMTU)
        mtu = struct.unpack("16si12x", data)[1]
        return mtu

    def setAddr(self, ifname, ip):
        """ Set the inet addr for an interface """
        result = self._call(ifname, self.SIOCSIFADDR, ip)

        if socket.inet_ntoa(result[20:24]) is ip:
            return True
        else:
            return None

    def setNetmask(self, ifname, ip):
        """ Set the netmask for an interface """
        result = self._call(ifname, self.SIOCSIFNETMASK, ip)

        if socket.inet_ntoa(result[20:24]) is ip:
            return True
        else:
            return None

    def setBroadcast(self, ifname, ip):
        """ Set the broadcast addr for an interface """
        result = self._call(ifname, self.SIOCSIFBRDADDR, ip)

        if socket.inet_ntoa(result[20:24]) is ip:
            return True
        else:
            return None

    def setStatus(self, ifname, status):
        """ Set interface status (UP/DOWN) """
        ifreq = (ifname + '\0' * self.IFNAMSIZ)[:self.IFNAMSIZ]

        if status is "UP":
            flags = self.IFF_UP
            flags |= self.IFF_RUNNING
            flags |= self.IFF_BROADCAST
            flags |= self.IFF_MULTICAST
            flags &= ~self.IFF_NOARP
            flags &= ~self.IFF_PROMISC
        elif status is "DOWN":
            flags = ~self.IFF_UP
        else:
            return None

        data = struct.pack("16sh", ifreq, flags)
        result = self._ioctl(self.SIOCSIFFLAGS, data)
        return result

    def setMTU(self, ifname, mtu):
        """ Set the MTU size of an interface """
        ifreq = (ifname + '\0' * self.IFNAMSIZ)[:self.IFNAMSIZ]

        data = struct.pack("16si", ifreq, mtu)
        result = self._ioctl(self.SIOCSIFMTU, data)

        if struct.unpack("16si", result)[1] is mtu:
            return True
        else:
            return None


class route:
    """ ioctl stuff """

#   From <bits/ioctls.h>

    # Routing table calls
    SIOCADDRT = 0x890B      # add routing table entry
    SIOCDELRT = 0x890C      # delete routing table entry
    SIOCRTMSG = 0x890D      # call to routing system

#   From <net/route.h>

    RTF_UP = 0x0001         # Route usable
    RTF_GATEWAY = 0x0002    # Destination is a gateway
    RTF_HOST = 0x0004       # Host entry (net otherwise)
    RTF_REINSTATE = 0x0008  # Reinstate route after timeout
    RTF_DYNAMIC = 0x0010    # Created dyn. (by redirect)
    RTF_MODIFIED = 0x0020   # Modified dyn. (by redirect)
    RTF_MTU = 0x0040        # Specific MTU for this route
    RTF_MSS = RTF_MTU       # Compatibility
    RTF_WINDOW = 0x0080     # Per route window clamping
    RTF_IRTT = 0x0100       # Initial round trip time
    RTF_REJECT = 0x0200     # Reject route
    RTF_STATIC = 0x0400     # Manually injected route
    RTF_XRESOLVE = 0x0800   # External resolver
    RTF_NOFORWARD = 0x1000  # Forwarding inhibited
    RTF_THROW = 0x2000      # Go to next class
    RTF_NOPMTUDISC = 0x4000 # Do not send packets with DF

    INADDR_ANY = '\0' * 4   # Any Internet Address

    def __init__(self):
        # create a socket to communicate with system
        self.sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def _ioctl(self, func, args):
        return fcntl.ioctl(self.sockfd.fileno(), func, args)

    def _call(self, func, arg):
        data = struct.pack("Li4s10xi4s10xi4s10xHhL", 0, socket.AF_INET, self.INADDR_ANY, socket.AF_INET, socket.inet_aton(arg), 0, '\0' * 4,
               self.RTF_GATEWAY, 0, 0)

        try:
            result = self._ioctl(func, data)
        except IOError:
            return None

        return result

    def delDefaultRoute(self, ip):
        self._call(self.SIOCDELRT, ip)


class wireless:
    """ ioctl stuff """

#   From </usr/include/wireless.h>
    
    SIOCGIWNAME = 0x8B01    # get name == wireless protocol
    SIOCGIWFREQ = 0x8B05    # get channel/frequency
    SIOCSIWMODE = 0x8B06    # set the operation mode
    SIOCGIWMODE = 0x8B07    # get operation mode
    SIOCGIWSENS = 0x8B09    # get sensitivity
    SIOCGIWAP = 0x8B15      # get AP MAC address
    SIOCGIWRATE = 0x8B21    # get default bit rate
    SIOCGIWRTS = 0x8B23     # get rts/cts threshold
    SIOCGIWFRAG = 0x8B25    # get fragmention thrh
    SIOCGIWTXPOW = 0x8B27   # get transmit power (dBm)
    SIOCGIWRETRY = 0x8B29   # get retry limit
    SIOCGIWRANGE = 0x8B0B   # range
    SIOCGIWSTATS = 0x8B0F   # get wireless statistics
    SIOCSIWESSID = 0x8B1A   # set essid
    SIOCGIWESSID = 0x8B1B   # get essid
    SIOCGIWPOWER = 0x8B2D   # get power managment settings
    SIOCGIWENCODE = 0x8B2B  # get encryption information
    
    SIOCGIWNWID = 0x8B03    # get network id
    SIOCSIWCOMMIT = 0x8B00  # commiting pending changes to driver
    SIOCGIWSCAN = 0x8B19    # get scanning results
   
    modes = ['Auto', 'Ad-Hoc', 'Managed', 'Master', 'Repeat', 'Second', 'Monitor']

    # KILO is not 2^10 in wireless tools, what the...
    KILO = 10**3
    MEGA = 10**6
    GIGA = 10**9

    def __init__(self):
        # create a socket to communicate with system
        self.sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def _ioctl(self, func, args):
        return fcntl.ioctl(self.sockfd.fileno(), func, args)

    def _call(self, ifname, func, arg = None):

        if arg is None:
            data = (ifname + '\0' * 32)[:32]
        else:
            data = (ifname + '\0' * 16)[:16] + arg

        try:
            result = self._ioctl(func, data)
        except IOError:
            return None

        return result

    def getInterfaceList(self):
        """ Find wireless interfaces """
        iflist = []
        path = "/sys/class/net" # FIXME: There may be an ioctl way to do this
        for interface in os.listdir(path):
            if os.path.exists(os.path.join(path, interface, "wireless")):
                iflist.append(interface)
        return iflist

    def getEssid(self, ifname):
        """ Get the ESSID for an interface """
        buffer = array.array('c', '\0' * 16)
        addr, length = buffer.buffer_info()
        arg = struct.pack('Pi', addr, length)

        self._call(ifname, self.SIOCGIWESSID, arg)
        return buffer.tostring().strip('\x00')

    def getMode(self, ifname):
        """ Get the operating mode of an interface """
        result = self._call(ifname, self.SIOCGIWMODE)
        mode = struct.unpack("i", result[16:20])[0]
        return self.modes[mode]

    def getBitrate(self, ifname):
        """ Get the bitrate of an interface """

        result = self._call(ifname, self.SIOCGIWRATE)

        size = struct.calcsize('ihbb')
        m, e, i, pad = struct.unpack('ihbb', result[16:16+size])
        if e == 0:
            bitrate =  m
        else:
            bitrate = float(m) * 10**e

        if bitrate >= self.GIGA:
            return "%i Gb/s" %(bitrate/self.GIGA)

        if bitrate >= self.MEGA:
            return "%i Mb/s" %(bitrate/self.MEGA)

        if bitrate >= self.KILO:
            return "%i Kb/s" %(bitrate/self.KILO)

    def setEssid(self, ifname, essid):
        """ Set the ESSID for an interface """
        if len(essid) > 16:
            return "ESSID should be 16 char or less" # FIXME: How shall we define error messages ?

        arg = struct.pack("iHH", id(essid) + 20, len(essid) + 1, 1)
        self._call(ifname, self.SIOCSIWESSID, arg)

        if self.getEssid is essid:
            return True
        else:
            return None

    def setMode(self, ifname, mode):
        """ Set the operating mode of an interface """
        arg = struct.pack("l", self.modes.index(mode))
        self._call(ifname, self.SIOCSIWMODE, arg)

        if self.getMode is mode:
            return True
        else:
            return None

if __name__ == "__main__":
    ifc = ifconfig()
    ifaces = ifc.getInterfaceList()

    print "Network interfaces found = ", ifaces
    for name in ifaces:
        print " %s is %s ip %s netmask %s broadcast %s mtu %i" % (name, ('DOWN', 'UP')[ifc.getStatus(name)],
            ifc.getAddr(name), ifc.getNetmask(name), ifc.getBroadcast(name), ifc.getMTU(name))
    
    wifi = wireless()
    ifaces_wifi = wifi.getInterfaceList()
    
    print "\nWireless interfaces found = ", ifaces_wifi
    for name in ifaces_wifi:
        print " %s essid %s mode %s bitrate %s" % (name, wifi.getEssid(name), wifi.getMode(name), wifi.getBitrate(name))

