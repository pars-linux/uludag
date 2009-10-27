/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <sys/types.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <arpa/inet.h>
#include <net/route.h>
#include <iwlib.h>
#include <wireless.h>

#include <qstringlist.h>
#include <qfile.h>
#include <qregexp.h>
#include <kprocess.h>
#include <kdebug.h>

#include "device.h"

#define RESOLV_CONF "/etc/resolv.conf"

Device::Device()
{
    rx = new QRegExp( "\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}" );
}


Device::~Device()
{
    delete rx;
    rx = 0;
}


/* Stolen from wireless-tools :) */
int Device::sockets_open(void)
{
    static const int families[] = {
        AF_INET, AF_IPX, AF_AX25, AF_APPLETALK
    };
    unsigned int  i;
    int sock;

    for(i = 0; i < sizeof(families)/sizeof(int); ++i)
    {
        sock = socket(families[i], SOCK_DGRAM, 0);
        if(sock >= 0)
            return sock;
    }

    return -1;
}


int Device::setInterface( const char *dev, const char *ip,
                          const char *bc, const char *nm )
{
    struct ifreq ifr;
    struct sockaddr_in sin;
    int skfd;
    int ret = 0;

    skfd = sockets_open();
    if ( skfd < 0 )
        return -1;

    // setup device flags, which also enables (up) device
    strcpy( ifr.ifr_name, dev );
    ifr.ifr_flags = IFF_UP;
    ifr.ifr_flags |= IFF_RUNNING;
    ifr.ifr_flags |= IFF_BROADCAST;
    ifr.ifr_flags |= IFF_MULTICAST;
    ifr.ifr_flags &= ~IFF_NOARP;
    ifr.ifr_flags &= ~IFF_PROMISC;
    if ( ioctl( skfd, SIOCSIFFLAGS, &ifr ) < 0 ) {
        ret = -1;
    }

    memset( &sin, 0, sizeof( struct sockaddr ) );
    sin.sin_family = AF_INET;

    inet_aton( ip, &(sin.sin_addr) );
    memcpy( &ifr.ifr_addr, &sin, sizeof( struct sockaddr ));
    if ( ioctl( skfd, SIOCSIFADDR, &ifr ) < 0 ) {
        ret = -1;
    }

    if ( bc ) {
        inet_aton( bc, &(sin.sin_addr) );
        memcpy( &ifr.ifr_addr, &sin, sizeof(struct sockaddr) );
        if ( ioctl( skfd, SIOCSIFBRDADDR, &ifr ) ) {
            ret = -1;
        }
    }

    if ( nm ) {
        inet_aton( nm, &(sin.sin_addr) );
        memcpy( &ifr.ifr_addr, &sin, sizeof(struct sockaddr) );
        if ( ioctl( skfd, SIOCSIFNETMASK, &ifr ) ) {
            ret = -1;
        }
    }

    close( skfd );
    return ret;
}


int Device::setDefaultRoute( const char *ip )
{
    struct rtentry route;
    struct sockaddr_in singw, sindst;
    int skfd;
    int ret = 0;

    skfd = sockets_open();
    if ( skfd < 0 )
        return -1;

    memset( &singw, 0, sizeof( struct sockaddr ) );
    memset( &sindst, 0, sizeof( struct sockaddr ) );
    singw.sin_family = AF_INET;
    sindst.sin_family = AF_INET;

    sindst.sin_addr.s_addr = INADDR_ANY;
    singw.sin_addr.s_addr = inet_addr( ip );

    memset( &route, 0, sizeof( struct rtentry ) );
    route.rt_dst = *(struct sockaddr *)&sindst;
    route.rt_gateway = *(struct sockaddr *)&singw;
    route.rt_flags = RTF_GATEWAY;

    /* del the route if its set before */
    ioctl( skfd, SIOCDELRT, &route );
    if( ioctl( skfd, SIOCADDRT, &route ) < 0) {
        ret = -1;
    }

    close( skfd );
    return ret;
}


QStringList Device::getDnsList()
{
    QStringList dnsList;

    QFile res_file( RESOLV_CONF ); // resolv.conf
    QString line;

    if (  !res_file.exists() || !res_file.open(  IO_ReadOnly ) )
        return QStringList();

    while ( -1 != res_file.readLine( line, 1024 ) ) {
        line = line.stripWhiteSpace();
        if ( line.startsWith( "nameserver" ) ) {
            int index = rx->search( line );
            if ( index >= 0 ) {
                dnsList.append( rx->cap() );
            }
        }
    }

    res_file.close();
    return dnsList;
}


int Device::writeDnsList( const QStringList& dnsList )
{
    QFile res_file( RESOLV_CONF ); // resolv.conf

    if (  !res_file.exists() || !res_file.open(  IO_WriteOnly|IO_Truncate ) )
        return -1;

    QTextStream str( &res_file );
    QStringList::ConstIterator end = dnsList.end();
    for ( QStringList::ConstIterator it = dnsList.begin();
          it != end; ++it ) {
        str << "nameserver " + *it + "\n";
    }

    res_file.close();

    return 0;
}

const char* Device::getIP( const char *dev )
{
    struct sockaddr_in *sin;
    struct ifreq ifr;
    int skfd = sockets_open();

    if ( skfd < 0 )
        return "";

    strcpy( ifr.ifr_name, dev );

    ioctl( skfd, SIOCGIFADDR, &ifr );
    sin = (struct sockaddr_in *)&ifr.ifr_addr;
    close( skfd );
    return inet_ntoa( sin->sin_addr );

}


const char* Device::getNetmask( const char *dev )
{
    struct sockaddr_in *sin;
    struct ifreq ifr;
    int skfd = sockets_open();

    if ( skfd < 0 )
        return "";

    strcpy( ifr.ifr_name, dev );

    ioctl( skfd, SIOCGIFNETMASK, &ifr );
    sin = (struct sockaddr_in *)&ifr.ifr_addr;
    close( skfd );
    return inet_ntoa( sin->sin_addr );

}


const char* Device::getBroadcast( const char *dev )
{
    struct sockaddr_in *sin;
    struct ifreq ifr;
    int skfd = sockets_open();

    if ( skfd < 0 )
        return "";

    strcpy( ifr.ifr_name, dev );

    ioctl( skfd, SIOCGIFBRDADDR, &ifr );
    sin = (struct sockaddr_in *)&ifr.ifr_addr;
    close( skfd );
    return inet_ntoa( sin->sin_addr );

}

int Device::startDhcpcd( const char *dev )
{
    KProcess startdhcpcd;
    startdhcpcd << "/sbin/dhcpcd" << dev;
    startdhcpcd.start();
    startdhcpcd.wait();

    if ( !startdhcpcd.normalExit() ) {
        kdDebug() << "tasmanet: startdhcpd failed.\n";
        return -1;
    }

    return 0;
}


int Device::killDhcpcd( const char *dev )
{
    KProcess killdhcpcd;
    killdhcpcd << "/sbin/dhcpcd" << "-k" << dev;
    killdhcpcd.start();
    killdhcpcd.wait();

     if ( !killdhcpcd.normalExit() ) {
        kdDebug() << "tasmanet: killdhcpd failed.\n";
        return -1;
    }

    return 0;
}


const QRegExp Device::getRx() const
{
    return *rx;
}

const char * Device::getESSID( const char *dev )
{
    int skfd = sockets_open();

    if ( skfd < 0 )
        return "";

    wireless_config *config = new wireless_config;

    if ( iw_get_basic_config( skfd, dev, config ) != -1 ) {
        if ( config->essid_on ) {
            return config->essid;
        }
    }

    close( skfd );
    return "";
}

WIFI_MODE Device::getWirelessMode( const char *dev )
{
    WIFI_MODE _mode = Auto;
    int skfd = sockets_open();

    if ( skfd < 0 )
        return _mode;

    wireless_config *config = new wireless_config;

    if ( iw_get_basic_config( skfd, dev, config ) != -1 ) {
        if ( config->has_mode == 1 ) {
            switch( config->mode ) {
            case IW_MODE_ADHOC:
                _mode = Adhoc;
                break;
            case IW_MODE_AUTO:
                _mode = Auto;
                break;
            case IW_MODE_INFRA:
                _mode = Infra;
                break;
            default:
                _mode = Infra;
            }
        }
        else {
            _mode = Infra;
        }
    }

    close( skfd );
    return _mode;
}


int Device::setWirelessInterface( const char *dev, int mode, const char *essid )
{
    int skfd = sockets_open();

    if ( skfd < 0 )
        return -1;

    wireless_config *config = new wireless_config;

    strncpy( config->name, dev, sizeof(config->name) );


    // no key for now :)
    config->has_key = 0;


    config->has_mode = 1;
    switch( mode ) {
    case Auto:
        config->mode = IW_MODE_AUTO;
        break;
    case Adhoc:
        config->mode = IW_MODE_ADHOC;
        break;
    case Infra:
        config->mode = IW_MODE_INFRA;
        break;
    default:
        config->mode = IW_MODE_INFRA;
    }

    strncpy(config->essid, essid, sizeof(config->essid)/sizeof(char) );
    config->has_essid = 1;
    config->essid_on = 1;


    if(iw_set_basic_config( skfd, dev, config ) < 0) {
        return -1;
    }

    return 0;
}

void Device::free_scan_results( wireless_scan *results )
{
    wireless_scan *ws = results;

    while (ws) {
        wireless_scan *d = ws;
        ws = ws->next;
        free (d);
    }
}

QStringList Device::scanWifiNetwork( const char *dev )
{
    wireless_scan_head wsh;
    wireless_scan *ws;
    int skfd = sockets_open();

    int ret = iw_scan( skfd, ( char* )dev, WIRELESS_EXT, &wsh );
    if ( ( ret == -1 ) && ( errno == ENODATA ) ) {
        // wait for device for one more second :).
        sleep( 1 );

        ret = iw_scan ( skfd, ( char* )dev, WIRELESS_EXT, &wsh );

        if ( ret == -1 ) {
            close ( skfd );
            return QStringList();
        }
    }

    // iterate over results
    QStringList networks;
    ws = wsh.result;
    while( ws ) {
        networks.append( ws->b.essid );
        ws = ws->next;
    }
    free_scan_results(wsh.result);

    return networks;
}
