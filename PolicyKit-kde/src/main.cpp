/*
  Copyright (c) 2007,2008 TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <qstring.h>

#include <kcmdlineargs.h>
#include <kaboutdata.h>
#include <kapplication.h>
#include <klocale.h>

#include "authdialog.h"
#include "policykitkde.h"
#include "debug.h"

int main (int argc, char *argv[])
{
    KAboutData aboutData( "policykit-kde", I18N_NOOP( "PolicyKit-kde" ), "0.1",
                        I18N_NOOP( "PolicyKit-kde" ), KAboutData::License_GPL_V2,
                        I18N_NOOP( "(c) 2007,2008 TUBITAK - UEKAE" ) );
    aboutData.addAuthor( "Gökçen Eraslan", I18N_NOOP( "Author" ), "gokcen@pardus.org.tr" );
    KCmdLineArgs::init( argc, argv, &aboutData );

    //set options
    KCmdLineOptions options[]= {
                                {"no-exit", I18N_NOOP("Do not exit automatically. This is used for debugging purposes."), 0},
                                KCmdLineLastOption
    };

    KCmdLineArgs::addCmdLineOptions(options);

    KApplication app;

    try {
        PolicyKitKDE *pkKDE = new PolicyKitKDE();
    }
    catch (QString exc)
    {
        return 0;
    }

    return app.exec();
}
