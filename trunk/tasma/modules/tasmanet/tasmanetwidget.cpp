/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <kaboutdata.h>
#include <kiconloader.h>
#include <qfile.h>
#include <qtimer.h>

#include "devicesettings.h"
#include "tasmanetwidget.h"
#include "tasmanetwidget.moc"

const QCString TasmaNetWidget::PROC_NET_DEV( "/proc/net/dev" );
const QCString TasmaNetWidget::PROC_NET_WIRELESS( "/proc/net/wireless" );

TasmaNetWidget::TasmaNetWidget( QWidget *parent, const char *name )
    : KIconView( parent, name )
{
    _aboutData = new KAboutData( I18N_NOOP( "tasmanet" ),
                                 I18N_NOOP( "TASMA Network Devices Module" ),
                                 0, 0, KAboutData::License_GPL,
                                 I18N_NOOP( "(c) 2005 TUBITAK/UEKAE" ) );
    _aboutData->addAuthor( "Baris Metin", I18N_NOOP( "Current Maintainer" ),
                           "baris@uludag.org.tr" );
    _aboutData->setTranslator( "Baris Metin", "baris@uludag.org.tr" );

    setSpacing( 15 );

    _timer = new QTimer( this );
    _timer->start( 10000 ); // 10 seconds timer
    connect( _timer, SIGNAL( timeout() ),
             this, SLOT( updateInterfaces() ) );

    connect( this, SIGNAL( executed( QIconViewItem* ) ),
             this, SLOT( interfaceSelected( QIconViewItem* ) ) );

    updateInterfaces();
}

void TasmaNetWidget::updateInterfaces()
{
    clear();

    QFile net_file( PROC_NET_DEV );
    QFile wifi_file( PROC_NET_WIRELESS );
    QString line;
    QStringList devices;

    if ( !net_file.exists() || !net_file.open( IO_ReadOnly ) )
        return;

    // pass header lines
    net_file.readLine( line, 1024 );
    net_file.readLine( line, 1024 );

    while ( -1 != net_file.readLine( line, 1024 ) ) {
        QString dev( line.left( line.findRev( ':' ) ).stripWhiteSpace() );
        if ( dev == "lo" ) continue;

        devices.push_back( dev );
    }

    net_file.close();

    if ( wifi_file.exists() && wifi_file.open( IO_ReadOnly ) ) {
        // pass header lines
        wifi_file.readLine( line, 1024 );
        wifi_file.readLine( line, 1024 );

        while ( -1 != wifi_file.readLine( line, 1024 ) ) {
            QString dev( line.left( line.findRev( ':' ) ).stripWhiteSpace() );

            QStringList::iterator it;
            for ( it = devices.begin(); it != devices.end(); ++it ) {
                if ( *it == dev )
                    *it = dev + i18n( " (wireless)" );
            }
        }

        wifi_file.close();
    }

    QPixmap _icon = DesktopIcon( "network_local", KIcon::SizeMedium );
    QStringList::iterator it;
    for ( it = devices.begin(); it != devices.end(); ++it ) {
        Interface *iface;
        iface = new Interface( this, *it, _icon );
    }

}

void TasmaNetWidget::interfaceSelected( QIconViewItem* item )
{
    DeviceSettings *settings = new DeviceSettings( this );
    settings->setCaption( item->text() );

    settings->show();
}

Interface::Interface( KIconView *parent, const QString& text,
                      const QPixmap& icon )
    : KIconViewItem( parent, text, icon )
{

}
