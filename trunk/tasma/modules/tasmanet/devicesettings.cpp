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
#include <net/if.h>

#include <qpushbutton.h>
#include <qlineedit.h>

#include <klocale.h>
#include <kmessagebox.h>

#include "devicesettings.h"
#include "devicesettings.moc"

DeviceSettings::DeviceSettings( QWidget *parent, QString dev, bool wifi )
    : DeviceSettingsDlg( parent ),
      _dev( dev ),
      _wifi( wifi )
{
    connect( applyButton, SIGNAL( clicked() ),
             this, SLOT( slotApply() ) );
    connect( cancelButton, SIGNAL( clicked() ),
             this, SLOT( slotCancel() ) );
}

void DeviceSettings::slotApply()
{
    int ret = set_iface( _dev.ascii(),
                         ipaddr->text().ascii(),
                         // we can ommit broadcast and netmask.
                         broadcast->text().length() ? broadcast->text().ascii() : 0,
                         netmask->text().length() ? netmask->text().ascii() : 0
        );

    if ( ret < 0 ) {
        QString err = i18n( "Failed to configure device: " ) + _dev;
        KMessageBox::error( this, err, i18n( "Error!" ) );
    }

    done( 0 );
}

void DeviceSettings::slotCancel()
{
    reject();
}

/* Stolen from wireless-tools :) */
int DeviceSettings::sockets_open(void)
{
    static const int families[] = {
        AF_INET, AF_IPX, AF_AX25, AF_APPLETALK
    };
    unsigned int  i;
    int           sock;

    for(i = 0; i < sizeof(families)/sizeof(int); ++i)
    {
        sock = socket(families[i], SOCK_DGRAM, 0);
        if(sock >= 0)
            return sock;
    }

    return -1;
}

int DeviceSettings::set_iface( const char *dev, const char *ip,
                               const char *bc, const char *nm )
{
    struct ifreq ifr;
    struct sockaddr_in sin;
    int skfd;

    skfd = sockets_open();
    if ( skfd < 0 )
        return -1;

    // enable (up) device
    strcpy( ifr.ifr_name, dev );
    ifr.ifr_flags |= IFF_UP | IFF_RUNNING;
    if ( ioctl( skfd, SIOCSIFFLAGS, &ifr ) < 0 ) {
        return -1;
    }

    memset( &sin, 0, sizeof( struct sockaddr ) );
    sin.sin_family = AF_INET;

    inet_aton( ip, &(sin.sin_addr) );
    memcpy( &ifr.ifr_addr, &sin, sizeof( struct sockaddr ));
    if ( ioctl( skfd, SIOCSIFADDR, &ifr ) < 0 ) {
        return -1;
    }

    if ( bc ) {
        inet_aton( bc, &(sin.sin_addr) );
        memcpy( &ifr.ifr_addr, &sin, sizeof(struct sockaddr) );
        if ( ioctl( skfd, SIOCSIFBRDADDR, &ifr ) ) {
            return -1;
        }
    }

    if ( nm ) {
        inet_aton( nm, &(sin.sin_addr) );
        memcpy( &ifr.ifr_addr, &sin, sizeof(struct sockaddr) );
        if ( ioctl( skfd, SIOCSIFNETMASK, &ifr ) ) {
            return -1;
        }
    }

    return 0;
}
