/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

/*
  tasma - main.cpp
  Create a TasmaApp and run mainloop.
*/

#include <kcmdlineargs.h>
#include <kaboutdata.h>
#include <kglobalsettings.h>
#include <kconfig.h>

//splash
//#include <kstandarddirs.h>
//#include <qsplashscreen.h>

#include "tasmamainwin.h"
#include "main.h"
#include "main.moc"

TasmaApp::TasmaApp()
    : KUniqueApplication(), tasmawin( 0 )
{
    tasmawin = new TasmaMainWin ();

    setMainWidget( tasmawin );
    KGlobal::setActiveInstance( this );

    QRect desk = KGlobalSettings::desktopGeometry( tasmawin );

    KConfig *config = KGlobal::config();
    config->setGroup( "MainWin" );
    int x = config->readNumEntry( "Width",
                                  QMIN( ( desk.width() * 4/5 ), 900 ) );
    int y = config->readNumEntry( "Height",
                                  QMIN( ( desk.height() * 4/5 ), 600 ) );

    tasmawin->resize( x, y );

}

TasmaApp::~TasmaApp()
{
    if ( tasmawin ) {
        KConfig *config = KGlobal::config();
        config->setGroup( "MainWin" );
        config->writeEntry( "Width", tasmawin->width() );
        config->writeEntry( "Height", tasmawin->height() );
        config->sync();
    }
}

int main( int argc, char *argv[] )
{
    KLocale::setMainCatalogue( "tasma" );
    KAboutData aboutData( "tasma", I18N_NOOP( "TASMA - Pardus Configuration Center" ), VERSION,
                          I18N_NOOP( "Pardus Configuration Center" ), KAboutData::License_GPL,
                          I18N_NOOP( "(c) 2005, TUBITAK - UEKAE" ) );
    aboutData.addAuthor( "Barış Metin", I18N_NOOP( "Current Maintainer" ), "baris@uludag.org.tr" );
    aboutData.addAuthor( I18N_NOOP( "KDE Developers" ), I18N_NOOP( "Module Developers" ) );
    aboutData.setTranslator( "Barış Metin", "baris@uludag.org.tr" );
    KCmdLineArgs::init( argc, argv, &aboutData );

    TasmaApp app;

/*
    // Create and initialize splash screen
    QSplashScreen * splash = new QSplashScreen(
        QPixmap( locate( "data", "tasma/splash.png" )));
    splash->message( I18N_NOOP( "TASMA - Uludag Configuration Center" ),
                     Qt::AlignCenter | Qt::AlignBottom );
    splash->show();
    // Show splash screen
    sleep(2);
    // delete splash screen
    delete splash;
*/

    app.mainWidget()->show();

    return app.exec();
}
