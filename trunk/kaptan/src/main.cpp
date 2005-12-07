/*
  Copyright (c) 2004,2005 TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <kapplication.h>
#include <kcmdlineargs.h>
#include <kaboutdata.h>

#include "kaptan.h"

static const char* const description = I18N_NOOP( "Kaptan Desktop" );

static KCmdLineOptions options[] =
{
    { "h", "yardim...", 0 },
    KCmdLineLastOption
};

int main( int argc, char* argv[] )
{
    KAboutData aboutData( "kaptan", description,
			 "1.0", description, KAboutData::License_GPL,
			 "(c) 2004,2005 TUBİTAK/UEKAE", 0, 0, "ismail@uludag.org.tr" );
    aboutData.addAuthor( "İsmail Dönmez", 0, "ismail@uludag.org.tr" );
    aboutData.addAuthor( "Barış Metin", 0, "baris@uludag.org.tr" );
    KCmdLineArgs::init( argc, argv, &aboutData );
    KCmdLineArgs::addCmdLineOptions( options );
    KApplication app;

    Kaptan *k = new Kaptan();
    k->resize( 490, 400 );
    
    app.setMainWidget(k);
    k->show();

    return app.exec();
}
