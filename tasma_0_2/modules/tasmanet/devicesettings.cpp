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
#include <net/route.h>

#include <qfile.h>
#include <qpushbutton.h>
#include <qradiobutton.h>
#include <qcombobox.h>
#include <qlistbox.h>
#include <qlineedit.h>
#include <qtimer.h>
#include <qregexp.h>
#include <qvalidator.h>

#include <kprocess.h>
#include <klocale.h>
#include <kmessagebox.h>
#include <kinputdialog.h>
#include <kconfig.h>

#include "devicesettings.h"
#include "devicesettings.moc"

#define RESOLV_CONF "/etc/resolv.conf"

DeviceSettings::DeviceSettings( QWidget *parent, QString dev, bool wifi )
    : DeviceSettingsDlg( parent ),
      _dev( dev ),
      _wifi( wifi )
{
    // ip validator
    rx = new QRegExp( "\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}" );
    validator = new QRegExpValidator( *rx, this );

    ipaddr->setValidator( validator );
    defaultgw->setValidator( validator );
    broadcast->setValidator( validator );
    netmask->setValidator( validator );

    // if ipaddr is changed we should recalculate broadcast and netmask
    // for now we just clear it.
    connect( ipaddr, SIGNAL( textChanged( const QString& ) ),
             this, SLOT( slotIPChanged() ) );

    // fill automatic types, for now only DHCP is supported
    automaticCombo->insertItem( "DHCP" );

    // fill dnsListBox
    dnsListBox->clear();
    QStringList dnsList = getDnsList();
    QStringList::ConstIterator end = dnsList.end();
    for ( QStringList::ConstIterator it = dnsList.begin();
          it != end; ++it ) {
        dnsListBox->insertItem( *it );
    }

    connect( addDnsButton, SIGNAL( clicked() ),
             this, SLOT( addDns() ) );
    connect( removeDnsButton, SIGNAL( clicked() ),
             this, SLOT( removeDns() ) );


    // get device information from kernel.
    struct sockaddr_in *sin;
    struct ifreq ifr;
    int skfd = sockets_open();
    strcpy( ifr.ifr_name, _dev.ascii() );
    // IP
    ioctl( skfd, SIOCGIFADDR, &ifr );
    sin = (struct sockaddr_in *)&ifr.ifr_addr;
    ipaddr->setText( inet_ntoa( sin->sin_addr ) );
    // Broadcast
    ioctl( skfd, SIOCGIFBRDADDR, &ifr );
    sin = (struct sockaddr_in *)&ifr.ifr_addr;
    broadcast->setText( inet_ntoa( sin->sin_addr ) );
    // Netmask
    ioctl( skfd, SIOCGIFNETMASK, &ifr );
    sin = (struct sockaddr_in *)&ifr.ifr_addr;
    netmask->setText( inet_ntoa( sin->sin_addr ) );


    connect( automaticButton, SIGNAL( toggled( bool ) ),
             this, SLOT( automaticToggled( bool ) ) );
    connect( manualButton, SIGNAL( toggled( bool ) ),
             this, SLOT( manualToggled( bool ) ) );

    connect( applyButton, SIGNAL( clicked() ),
             this, SLOT( slotApply() ) );
    connect( cancelButton, SIGNAL( clicked() ),
             this, SLOT( slotCancel() ) );

    KConfig *config = new KConfig( "tasmanetrc" );
    config->setGroup( _dev );
    QString _connType = config->readEntry( "ConnectionType", "Automatic" );
    defaultgw->setText( config->readEntry( "DefaultGateway", "" ) );
    if ( _connType == "Automatic" ) {
        automaticButton->setChecked( true );
    }
    else if ( _connType == "Manual" ) {
        manualButton->setChecked( true );
    }

    delete config;
}

void DeviceSettings::slotApply()
{
    bool succeed = true;

    /* Manual Settings */
    if ( manualButton->isChecked() ) {
        // SET IP
        int ret = set_iface( _dev.ascii(),
                             ipaddr->text().ascii(),
                             // we can ommit broadcast and netmask.
                             broadcast->text().length() ? broadcast->text().ascii() : 0,
                             netmask->text().length() ? netmask->text().ascii() : 0
            );
        if ( ret < 0 ) succeed = false;

        // SET ROUTE
        if ( !defaultgw->text().isEmpty() ) {
            ret =  set_default_route( defaultgw->text().ascii() );
            if ( ret < 0 ) succeed = false;
        }

        ret = writeDnsList();
        if ( ret < 0 ) succeed = false;

    }
    /* Automatic (DHCP) */
    else if ( automaticButton->isChecked() ) {
        // I don't like to invoke programs directly
        // but we have no chance for now,
        // this is clearly a bad hack :(.

        QFile pidfile( "/var/run/dhcpcd-" + _dev + ".pid" );
        if ( pidfile.exists() ) {
            KProcess killdhcpcd;
            killdhcpcd << "/sbin/dhcpcd" << "-k" << _dev;
            killdhcpcd.start();
            killdhcpcd.wait();

            // how ugly... wait 2 seconds to dhcpcd to finish its work...
            if ( killdhcpcd.normalExit() )
                QTimer::singleShot( 2000, this, SLOT( startDhcpcd() ) );
            else
                printf( "failed (kill)\n" );
        }
        else
            startDhcpcd();
    }

    writeSettings();

    if ( succeed ) {
        QString msg = i18n( "Successfully configured device: " ) + _dev;
        KMessageBox::information( this, msg, i18n( "Done!" ) );
    }
    else {
        QString msg = i18n( "Failed to configure device: " ) + _dev;
        KMessageBox::error( this, msg, i18n( "Error!" ) );
    }

    done( 0 );
}

void DeviceSettings::startDhcpcd() {
    KProcess startdhcpcd;
    startdhcpcd << "/sbin/dhcpcd" << _dev;
    startdhcpcd.start();
    startdhcpcd.wait();

    if ( !startdhcpcd.normalExit() )
        printf( "failed (start)\n" );
}


void DeviceSettings::writeSettings()
{
    KConfig *config = new KConfig( "tasmanetrc" );
    config->setGroup( _dev );

    if ( manualButton->isChecked() ) {
        config->writeEntry( "ConnectionType", "Manual" );
        if ( defaultgw->isModified() )
            config->writeEntry( "DefaultGateway", defaultgw->text() );
    }
    else if ( automaticButton->isChecked() ) {
        config->writeEntry( "ConnectionType", "Automatic" );
    }

    delete config;
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
    ifr.ifr_flags = IFF_UP | IFF_RUNNING | ~IFF_NOARP | IFF_MULTICAST | IFF_BROADCAST;
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

int DeviceSettings::set_default_route( const char *ip )
{
    struct rtentry route;
    struct sockaddr_in singw, sindst;
    int skfd;

    skfd = sockets_open();

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
    if( ioctl( skfd, SIOCADDRT, &route ) < 0) {
        return -1;
    }

    return 0;
}


void DeviceSettings::automaticToggled( bool on )
{
    if ( on ) {
        // automatic choosen, disable manual settings...
        manualButton->setChecked( false );
        ipaddr->setEnabled( false );
        broadcast->setEnabled( false );
        netmask->setEnabled( false );
        defaultgw->setEnabled( false );
        dnsListBox->setEnabled( false );
        addDnsButton->setEnabled( false );
        removeDnsButton->setEnabled( false );

        automaticCombo->setEnabled( true );
    }
}

void DeviceSettings::manualToggled( bool on )
{
    if ( on ) {
        automaticButton->setChecked( false );
        automaticCombo->setEnabled( false );

        ipaddr->setEnabled( true );
        broadcast->setEnabled( true );
        netmask->setEnabled( true );
        defaultgw->setEnabled( true );
        dnsListBox->setEnabled( true );
        addDnsButton->setEnabled( true );
        removeDnsButton->setEnabled( true );
    }
}

QStringList DeviceSettings::getDnsList()
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

int DeviceSettings::writeDnsList()
{
    QFile res_file( RESOLV_CONF ); // resolv.conf

    if (  !res_file.exists() || !res_file.open(  IO_WriteOnly|IO_Truncate ) )
        return -1;

    QTextStream str( &res_file );
    unsigned int num = dnsListBox->count();
    for ( unsigned int row = 0; row < num; ++row ) {
        QString line = "nameserver " + dnsListBox->text( row );
        str << "nameserver " + dnsListBox->text( row ) + "\n";
    }

    res_file.close();

    return 0;
}

void DeviceSettings::removeDns()
{
    dnsListBox->removeItem(
        dnsListBox->currentItem() );
}

void DeviceSettings::addDns()
{
    QString newdns = KInputDialog::getText( i18n( "Add new nameserver" ),
                                            i18n( "Add a new name server." ),
                                            QString::null,
                                            0,
                                            this,
                                            "getDNSdialog",
                                            validator );

    dnsListBox->insertItem( newdns );
}

DeviceSettings::~DeviceSettings()
{
    delete rx;
    delete validator;
}

void DeviceSettings::slotIPChanged()
{
    // if broadcast and netmask is modified, user knows what he/she is doing
    if ( !broadcast->isModified() )
        broadcast->clear();
    if ( !netmask->isModified() )
        netmask->clear();
}
