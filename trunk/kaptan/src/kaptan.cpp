/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <kapplication.h>
#include <kstandarddirs.h>
#include <klocale.h>
#include <kconfig.h>
#include <dcopclient.h>

#include <X11/Xlib.h>

#include "welcome.h"
#include "mouse.h"
#include "wallpaper.h"
#include "goodbye.h"

#include "kaptan.h"
#include "kaptan.moc"

Kaptan::Kaptan( QWidget *parent, const char *name )
    : KWizard( parent, name, true)
{
    setCaption( kapp->caption() );

    /* Kaptan sadece ilk açılışta çalışsın */
    KConfig *config = kapp->config();
    config->setGroup("General");
    config->writeEntry("RunOnStart", false);
    config->sync();
    
    welcome = new Welcome( this );
    addPage( welcome, i18n( "Welcome" ) );
    setHelpEnabled( QWizard::page( 0 ), false );

    mouse = new MouseSetup( this );
    addPage( mouse, i18n( "Mouse Setup" ) );
    setHelpEnabled( QWizard::page( 1 ), false );

    wallpaper = new Wallpaper( this );
    addPage( wallpaper, i18n( "Wallpaper Setup" ) );
    setHelpEnabled( QWizard::page( 2 ), false );

    goodbye = new Goodbye( this );
    addPage( goodbye, i18n( "Congratulations" ) );
    setHelpEnabled( QWizard::page( 3 ), false );

    setFinishEnabled( QWizard::page( 3 ), true );

    locale = new KLocale( PACKAGE );
    locale->setLanguage( KLocale::defaultLanguage() );
}

Kaptan::~Kaptan()
{

}

void Kaptan::next()
{
    if ( currentPage() == mouse ) {
        mouse->apply();
        mouse->save();
    }
    else if ( currentPage() == wallpaper ) {
        if ( wallpaper->changeWallpaper() )
            wallpaper->setWallpaper();
    }

    QWizard::next();
}

void Kaptan::back()
{
    QWizard::back();
}

// FINISHED - set defaults...
void Kaptan::accept()
{
    // Kicker değişkenlerini ayarlayalım...
    // 	- İkonların üzerine gelince büyüme efektini aç...
    KConfig kickerconf("kickerrc", false, false);
    kickerconf.setGroup("buttons");
    kickerconf.writeEntry("EnableIconZoom", true);
    kickerconf.sync();

    // Kicker'ı DCOP ile dürtelim ki yeni ayarları yüklesin
    if (!kapp->dcopClient()->isAttached())
        kapp->dcopClient()->attach();

    QByteArray data;
    QCString appname;
    if (DefaultScreen(qt_xdisplay()) == 0)
        appname = "kicker";
    else
        appname.sprintf("kicker-screen-%d", DefaultScreen(qt_xdisplay()));
    kapp->dcopClient()->send( appname, "kicker", "configure()", data );

    // KDE değişkenlerini ayarlayalım...
    // 	- Düğmeler üzerinde simgeleri görünsün
    // 	- Combo'lar açılırken efektli açılsın
    // 	- Renk şeması lipstikwhite olsun
    KGlobal::config()->setGroup("KDE");
    KGlobal::config()->writeEntry("ShowIconsOnPushButtons", true,true, true);
    KGlobal::config()->writeEntry("EffectAnimateCombo", true, true, true);
    KGlobal::config()->writeEntry("colorScheme", "lipstikwhite.kcsrc", true, true, true);

    KGlobal::config()->sync();

    exit(0);
}

// CANCELED
void Kaptan::reject()
{
    exit(0);
}

// WINDOW CLOSED
void Kaptan::closeEvent(QCloseEvent* e)
{
    exit(0);
}
