/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <qlabel.h>
#include <qcheckbox.h>
#include <qstringlist.h>
#include <qpixmap.h>
#include <qimage.h>
#include <qmap.h>
#include <kcombobox.h>
#include <kstandarddirs.h>
#include <kglobal.h>
#include <kstringhandler.h>
#include <kconfig.h>
#include <dcopref.h>

#include "wallpaper.h"

Wallpaper::Wallpaper( QWidget *parent, const char* name )
    : WallpaperDlg( parent, name )
{
    changePaper = true;
    selectedPaper = "";
    mDirs = KGlobal::dirs();

    QStringList lst = mDirs->findAllResources( "wallpaper",  "*",  false,  true );
    int i = 0;
    QStringList::ConstIterator end = lst.end();
    for ( QStringList::ConstIterator it = lst.begin(); it != end; ++it )
    {
        //build fileCaption from filename
        QString fileCaption;
        QString fileName;
        int slash = ( *it ).findRev( '/' ) + 1;
        int endDot = ( *it ).findRev( '.' );

        fileName = ( *it ).mid( slash );

        // strip the extension if it exists
        if ( endDot != -1 && endDot > slash )
            fileCaption = ( *it ).mid( slash,  endDot - slash );
        else
            fileCaption = ( *it ).mid( slash );

        fileCaption.replace( '_',  ' ' );
        fileCaption = KStringHandler::capwords( fileCaption );


        m_urlWallpaperBox->insertItem( fileCaption );
        papers[fileName] = i; i++;

    }

    connect( m_urlWallpaperBox, SIGNAL( activated( int ) ),
             this, SLOT( paperSelected( int ) ) );
    connect( checkChange, SIGNAL( toggled( bool ) ),
             this, SLOT( checkChanged( bool ) ) );


    emit paperSelected( 0 );
}

void Wallpaper::paperSelected( int item )
{
    QMap<QString, int>::ConstIterator end = papers.end();
    for ( QMap<QString, int>::ConstIterator it = papers.begin();
          it != end;
          ++it )
    {
        if ( it.data() == item )
        {
            QImage wp;
            QString file = locate( "wallpaper", it.key() );
            wp.load( file );
            wp = wp.smoothScale( 140, 105 );
            QPixmap pix( wp );
            pix_wallpaper->setPixmap( pix );

            selectedPaper = it.key();
            break;
        }
    }
}

void Wallpaper::setWallpaper()
{
    // KDesktop değişkenlerini ayarlayalım...
    // 	- Masaüstü resmi Kapla kipinde olsun
    // 	- Masaüst resmi default_wallpaper'da ki resim olsun
    // bunları seçimden alacağız...
    KConfig kdesktopconf("kdesktoprc", false, false);
    kdesktopconf.setGroup("Desktop0");
    kdesktopconf.writeEntry("WallpaperMode", "Scaled");
    kdesktopconf.writePathEntry("Wallpaper", selectedPaper);

    // Tüm masaüstlerinde aynı resim/renk kullanılsın
    kdesktopconf.setGroup("Background Common");
    kdesktopconf.writeEntry("CommonDesktop", true);

    // Masaüstü ikon rengi beyaz olsun...
    kdesktopconf.setGroup("FMSettings");
    kdesktopconf.writeEntry("NormalTextColor", QColor("#FFFFFF") );
    kdesktopconf.sync();

    // call dcop
    DCOPRef wall( "kdesktop",  "KBackgroundIface" );
    DCOPReply reply = wall.call(  "setWallpaper", selectedPaper, 6 );

}

void Wallpaper::checkChanged( bool dontChange )
{
    if ( dontChange ) {
        changePaper = false;
        m_urlWallpaperBox->setEnabled( false );
    }
    else {
        changePaper = true;
        m_urlWallpaperBox->setEnabled( true );
    }
}

bool Wallpaper::changeWallpaper()
{
    if ( changePaper )
        return true;
    else
        return false;
}
