/*
  Copyright (c) 2004,2005 TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <qfile.h>
#include <qlabel.h>
#include <qcheckbox.h>
#include <qpushbutton.h>
#include <qstringlist.h>
#include <qpixmap.h>
#include <qimage.h>
#include <qmap.h>
#include <qtextstream.h>

#include <dcopref.h>
#include <kcombobox.h>
#include <kdebug.h>
#include <kstandarddirs.h>
#include <kglobal.h>
#include <kstringhandler.h>
#include <kconfig.h>


#include "wallpaper.h"

Wallpaper::Wallpaper( QWidget *parent, const char* name )
    : WallpaperDlg( parent, name )
{
    changePaper = true;
    selectedPaper = "";
    
    QStringList lst = KGlobal::dirs()->findAllResources( "wallpaper",  "*.desktop",  false /* no recursion */,  true /* unique files */ );
    QString line,lname,lang,langCode;

    lang = QString(getenv("LC_ALL"));
    if (lang == "tr_TR.UTF-8")
      langCode="Name[tr]";
    else
      langCode="Name";

    for(QStringList::Iterator it = lst.begin(); it != lst.end(); ++it)
      {
	if((*it).endsWith(".svgz.desktop"))
	  {
	    // We can't show SVG
	  }
	else
	  {
	    QFile desktopFile(*it);
	    QTextStream stream(&desktopFile);
	    desktopFile.open(IO_ReadOnly);

            bool foundName = false;
            while(!foundName && (line = stream.readLine()))
              {
                if (line.startsWith(langCode))
                  {
                    lname = line.section("=",1,1);
                    foundName=true;
                  }
              }
	    
	    papers.insert(lname, (*it).remove(".desktop"));
	    desktopFile.close();
	  }
      }

    QMap<QString, QString>::ConstIterator it = papers.begin();
    for(; it != papers.constEnd(); ++it)
      m_urlWallpaperBox->insertItem(it.key());

    connect( testWallpaper, SIGNAL( clicked() ), this , SLOT( setWallpaper() ) );
    connect( m_urlWallpaperBox, SIGNAL( activated( int ) ), this, SLOT( paperSelected( int ) ) );
    connect( checkChange, SIGNAL( toggled( bool ) ), this, SLOT( checkChanged( bool ) ) );


    emit paperSelected(0);
}

void Wallpaper::paperSelected( int item )
{
  QString file = papers[m_urlWallpaperBox->text(item)];
  QImage wp(file);
  wp = wp.smoothScale( 140, 105 );
  QPixmap pix( wp );
  pix_wallpaper->setPixmap( pix );
  selectedPaper = file;
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

#include "wallpaper.moc"
