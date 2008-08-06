/*
  Copyright (c) TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

/*
  tasma - main.cpp
  Create a TasmaApp and run main loop.
*/

#include <kcmdlineargs.h>
#include <kaboutdata.h>
#include <kglobalsettings.h>
#include <kconfig.h>

#include "tasmamainwin.h"
#include "main.h"

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

  delete tasmawin;
}

int main( int argc, char *argv[] )
{
  KLocale::setMainCatalogue( "tasma" );
  KAboutData aboutData( "tasma", I18N_NOOP( "TASMA - Pardus Configuration Center" ), "1.3",
                        I18N_NOOP( "Pardus Configuration Center" ), KAboutData::License_GPL,
                        I18N_NOOP( "(c) TUBITAK - UEKAE" ) );
  aboutData.addAuthor( "Pınar Yanardağ", I18N_NOOP( "Current Maintainer" ), "pinar@pardus.org.tr" );
  aboutData.addAuthor( "İsmail Dönmez", I18N_NOOP( "Developer" ), "ismail@pardus.org.tr" );
  aboutData.addAuthor( "Barış Metin", I18N_NOOP( "Old Maintainer & Original Author" ), "baris@pardus.org.tr" );
  aboutData.addCredit(I18N_NOOP("Bahadır Kandemir"), I18N_NOOP("Module Developers"), "bahadir@pardus.org.tr");
  aboutData.addCredit(I18N_NOOP("Faik Uygur"), I18N_NOOP("TV Module Maintainer"), "faik@pardus.org.tr");
  aboutData.addCredit(I18N_NOOP("Fatih Aşıcı"), I18N_NOOP("Module Developers"), "fatih@pardus.org.tr");
  aboutData.addCredit(I18N_NOOP("Gökmen Göksel"), I18N_NOOP("Module Developers"), "gokmen@pardus.org.tr");
  aboutData.addCredit(I18N_NOOP("İşbaran Akçayır"), I18N_NOOP("Module Developers"), "isbaran@gmail.com");
  aboutData.addCredit(I18N_NOOP("KDE"), I18N_NOOP("Module Developers"), "kde-devel@kde.org");
  aboutData.setTranslator( "Barış Metin", "baris@pardus.org.tr" );

  KCmdLineArgs::init( argc, argv, &aboutData );

  TasmaApp app;
  app.mainWidget()->show();

  return app.exec();
}

#include "main.moc"
