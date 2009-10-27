/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <iwlib.h> // PROC_NET_DEV, iw*()

#include <kaboutdata.h>
#include <kiconloader.h>
#include <qfile.h>
#include <qtimer.h>
#include <qpair.h>
#include <qptrlist.h>

#include "devicesettings.h"
#include "tasmanetwidget.h"
#include "tasmanetwidget.moc"


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
    QString line;
    QPixmap _icon = DesktopIcon( "network_local", KIcon::SizeLarge );

    if ( !net_file.exists() || !net_file.open( IO_ReadOnly ) )
        return;

    // pass header lines
    net_file.readLine( line, 1024 );
    net_file.readLine( line, 1024 );

    // get the devicenames, also check for wireless extentions.
    int sock = iw_sockets_open();
    struct wireless_info info;
    while ( -1 != net_file.readLine( line, 1024 ) ) {
        QString dev( line.left( line.findRev( ':' ) ).stripWhiteSpace() );
        QString text( dev );
        bool isWifi = false;

        if ( dev == "lo" ) continue;

        if ( iw_get_basic_config( sock, dev.ascii(), &(info.b) ) >= 0 ) {
            // wireless
            text += i18n( " (wireless)" );
            isWifi= true;
        }

        Interface *iface;
        iface = new Interface( this, text, _icon, dev, isWifi );
    }

    net_file.close();
}

void TasmaNetWidget::interfaceSelected( QIconViewItem* item )
{
    Interface *iface = static_cast<Interface*>( item );
    DeviceSettings *settings = new DeviceSettings( this, iface->device(), iface->isWifi() );
    settings->setCaption( item->text() );

    settings->exec();
}

Interface::Interface( KIconView *parent, const QString& text,
                      const QPixmap& icon, const QString& dev, bool wf )
    : KIconViewItem( parent, text, icon ),
      _dev( dev ),
      _wifi( wf )
{

}
