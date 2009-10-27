/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <qfile.h>
#include <qpushbutton.h>
#include <qradiobutton.h>
#include <qcombobox.h>
#include <qlistbox.h>
#include <qlineedit.h>
#include <qtabwidget.h>
#include <qtimer.h>
#include <qregexp.h>
#include <qvalidator.h>

#include <kprocess.h>
#include <klocale.h>
#include <kmessagebox.h>
#include <kinputdialog.h>
#include <kconfig.h>
#include <kdebug.h>

#include "devicesettings.h"
#include "devicesettings.moc"


DeviceSettings::DeviceSettings( QWidget *parent, QString dev, bool wifi )
    : DeviceSettingsDlg( parent ), Device(),
      _dev( dev ),
      _wifi( wifi )
{
    // fill automatic types, for now only DHCP is supported
    automaticCombo->insertItem( "DHCP" );

    if ( wifi ) {
        // fill wireless modes
        wifiModeCombo->insertItem( "Auto" );
        wifiModeCombo->insertItem( "Ad-Hoc" );
        wifiModeCombo->insertItem( "Managed" ); // Infra == Managed

        // get wireless information from kernel
        essid->setText( getESSID( _dev.ascii() ) );
        WIFI_MODE mode = getWirelessMode( _dev.ascii() );
        if ( mode == Auto ) {
            wifiModeCombo->setCurrentItem( 0 );
        }
        else if ( mode == Adhoc ) {
            wifiModeCombo->setCurrentItem( 1 );
        }
        else if ( mode == Infra ) {
            wifiModeCombo->setCurrentItem( 2 );
        }

        slotScanWifi();

        connect( wifiScanBtn, SIGNAL( clicked() ),
                 this, SLOT( slotScanWifi() ) );

        connect( essidList, SIGNAL( selected( int ) ),
                 this, SLOT( slotEssidSelected( int ) ) );
    }
    else {
        // remove Wireless page
        tabWidget->removePage( tabWidget->page( 0 ) );
    }


    connect( automaticButton, SIGNAL( toggled( bool ) ),
             this, SLOT( automaticToggled( bool ) ) );
    connect( manualButton, SIGNAL( toggled( bool ) ),
             this, SLOT( manualToggled( bool ) ) );


    // ip validator
    validator = new QRegExpValidator( getRx(), this );

    ipaddr->setValidator( validator );
    defaultgw->setValidator( validator );
    broadcast->setValidator( validator );
    netmask->setValidator( validator );

    // if ipaddr is changed we should recalculate broadcast and netmask
    // for now we just clear it.
    connect( ipaddr, SIGNAL( textChanged( const QString& ) ),
             this, SLOT( slotIPChanged() ) );

    // get device information from kernel and show them.
    ipaddr->setText( getIP( _dev.ascii() ) );
    broadcast->setText( getBroadcast( _dev.ascii() ) );
    netmask->setText( getNetmask( _dev.ascii() ) );

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

    // read the last configuration
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


    connect( applyButton, SIGNAL( clicked() ),
             this, SLOT( slotApply() ) );
    connect( cancelButton, SIGNAL( clicked() ),
             this, SLOT( slotCancel() ) );
}


void DeviceSettings::slotApply()
{
    bool succeed = true;

    if ( _wifi ) {
        int mode = IW_MODE_INFRA;
        int cur = wifiModeCombo->currentItem();

        if ( cur == 0 ) {
            mode = IW_MODE_AUTO;
        }
        else if ( cur == 1 ) {
            mode = IW_MODE_ADHOC;
        }
        else if ( cur == 2 ) {
            mode = IW_MODE_INFRA;
        }

        setWirelessInterface( _dev.ascii(),
                              mode,
                              essid->text().ascii() );
    }

    /* Manual Settings */
    if ( manualButton->isChecked() ) {
        // SET IP
        int ret = setInterface( _dev.ascii(),
                             ipaddr->text().ascii(),
                             // we can ommit broadcast and netmask.
                             broadcast->text().length() ? broadcast->text().ascii() : 0,
                             netmask->text().length() ? netmask->text().ascii() : 0
            );
        if ( ret < 0 ) {
            succeed = false;
            kdDebug() << "tasmanet: set_iface() failed\n";
        }

        // SET ROUTE
        if ( !defaultgw->text().isEmpty() ) {
            ret =  setDefaultRoute( defaultgw->text().ascii() );
            if ( ret < 0 ) {
                succeed = false;
                kdDebug() << "tasmanet: set_default_route() failed\n";
            }
        }

        // write nameservers...
        QStringList dnsList;
        unsigned int num = dnsListBox->count();
        for ( unsigned int row = 0; row < num; ++row )
            dnsList.append( dnsListBox->text( row ) );

        ret = writeDnsList( dnsList );

        if ( ret < 0 ) {
            succeed = false;
            kdDebug() << "tasmanet: writeDnsList() failed\n";
        }

    }
    /* Automatic (DHCP) */
    else if ( automaticButton->isChecked() ) {
        // I don't like to invoke programs directly
        // but we have no chance for now,
        // this is clearly a bad hack :(.

        QFile pidfile( "/var/run/dhcpcd-" + _dev + ".pid" );
        if ( pidfile.exists() ) {
            if ( killDhcpcd( _dev.ascii() ) < 0 ) {
                succeed = false;
            }
            else {
                // how ugly... wait 2 seconds to dhcpcd to finish its work...
                QTimer::singleShot( 2000, this, SLOT( slotStartDhcpcd() ) );
            }
        }
        else {
            if ( startDhcpcd( _dev.ascii() ) < 0 ) succeed = false;
        }
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

void DeviceSettings::slotStartDhcpcd()
{
    startDhcpcd( _dev.ascii() );
}

void DeviceSettings::slotScanWifi()
{
    essidList->clear();

    // fill wifiNetworks list
    QStringList networks = scanWifiNetwork( _dev.ascii() );
    QStringList::ConstIterator end = networks.end();
    for ( QStringList::ConstIterator it = networks.begin();
          it != end; ++it ) {
        essidList->insertItem( *it );
    }

}

void DeviceSettings::slotEssidSelected( int index )
{
    essid->setText( essidList->text( index ) );
}
