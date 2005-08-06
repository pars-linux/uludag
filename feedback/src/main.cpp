/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <kapplication.h>
#include <kcmdlineargs.h>
#include <kaboutdata.h>

#include "feedback.h"

/* Any better name? */
static const char* const description = I18N_NOOP( "Feedback" );

static KCmdLineOptions options[] =
{
	{ "h", "help", 0 },
	KCmdLineLastOption
};

int main( int argc, char* argv[] )
{

	/* Initialize */
	KAboutData aboutData( PACKAGE, description,
		VERSION, description, KAboutData::License_GPL,
		"(c) 2004 TUBITAK/UEKAE", 0, 0, "caglar@uludag.org.tr" );
	aboutData.addAuthor( "S.Çağlar Onur", 0, "caglar@uludag.org.tr" );

	KCmdLineArgs::init( argc, argv, &aboutData );
	KCmdLineArgs::addCmdLineOptions( options );
	KApplication app;

	Feedback *k = new Feedback();
	k->setFixedSize( 650, 350 );
	k->show();

	/* Enter Main Loop */
	return app.exec();
}
