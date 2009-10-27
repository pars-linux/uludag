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
#include <kpushbutton.h>

#include "welcome.h"
#include "mouse.h"
#include "wallpaper.h"
#include "goodbye.h"

#include "kaptan.h"

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

    locale = new KLocale( "kaptan" );
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
            cancelButton()->hide();
    }

    QWizard::next();
}

void Kaptan::back()
{
  if ( currentPage() == goodbye )
    cancelButton()->show();

  QWizard::back();
}

void Kaptan::accept()
{
    // KDE değişkenlerini ayarlayalım...
    // 	- Düğmeler üzerinde simgeleri görünsün
    // 	- Combo'lar açılırken efektli açılsın
    KGlobal::config()->setGroup("KDE");
    KGlobal::config()->writeEntry("ShowIconsOnPushButtons", true,true, true);
    KGlobal::config()->writeEntry("EffectAnimateCombo", true, true, true);

    KGlobal::config()->sync();

    QWizard::accept();
}

#include "kaptan.moc"
