/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <iwlib.h>

class QStringList;
class QRegExp;

/* Modes of operation */
#define IW_MODE_AUTO    0       /* Let the driver decides */
#define IW_MODE_ADHOC   1       /* Single cell network */
#define IW_MODE_INFRA   2       /* Multi cell network, roaming, ... (aka. Managed) */
#define IW_MODE_MASTER  3       /* Synchronisation master or Access Point */
#define IW_MODE_REPEAT  4       /* Wireless Repeater (forwarder) */
#define IW_MODE_SECOND  5       /* Secondary master/repeater (backup) */
#define IW_MODE_MONITOR 6       /* Passive monitor (listen only) */


enum WIFI_MODE {
    Auto = 0,
    Adhoc,
    Infra
};

class Device
{

public:
    Device();
    virtual ~Device();

    /**
     * Configures the interface (dev), with ip (and if provided)
     * broadcast (bc) and netmask (nm).
     */
    int setInterface( const char *dev, const char *ip,
		      const char *bc, const char *nm );

    /**
     * Adds a default route to the routing table
     */
    int setDefaultRoute( const char *ip );

    /**
     * Get IP address for device from kernel
     */
    const char *getIP( const char *dev );

    /**
     * Get Netmask for device from kernel
     */
    const char *getNetmask( const char *dev );

    /**
     * Get broadcast for device from kernel
     */
    const char *getBroadcast( const char *dev );


    /**
     * scan for wireless networks
     */
    QStringList scanWifiNetwork( const char *dev );

    /**
     * Get ESSID for device if it's set
     */
    const char *getESSID( const char *dev );

    /**
     * Get mode for wireless device.
     */
    WIFI_MODE getWirelessMode( const char *dev );

    /**
     * Set wireless interface.
     */
    int setWirelessInterface( const char *dev, int mode, const char *essid );

    /**
     * Read resolv.conf and return the nameserver list
     */
    QStringList getDnsList();

    /**
     * Write nameservers to resolv.conf
     */
    int writeDnsList( const QStringList& dnsList );

    /**
     * Start dhcpcd for device (dev)
     */
    int startDhcpcd( const char *dev );

    /**
     * Send a SIGHUP signal to the dhcpcd process
     */
    int killDhcpcd( const char *dev );

    /**
     * return the regexp object used for IP validation
     */
    const QRegExp getRx() const;


private:
    /**
     * Open a socket for us to communicate with kernel
     */
    int sockets_open();
    void free_scan_results( wireless_scan *results );

    QRegExp *rx;
};


