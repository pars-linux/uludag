/*
  Copyright 2005 UEKAE/TUBITAK
  Licensed under GNU GPLv2 or later at your option
*/

#include <kapplication.h>
#include <kcmdlineargs.h>
#include <klocale.h>
#include <kaboutdata.h>

#include "packagerui.h"

static const KCmdLineOptions options[] = 
  {
    KCmdLineLastOption
  };

int main(int argc, char** argv)
{

  KAboutData aboutData(
		       "packager",
		       I18N_NOOP("Pardus Package Manager Frontend"),
		       "0.0.1",
		       I18N_NOOP("Package Manager frontend for Pardus Linux"),
		       KAboutData::License_GPL,
		       I18N_NOOP("(C) 2005 UEKAE/TUBITAK"),
		       I18N_NOOP("A KDE frontend to PiSi"),
		       "http://www.uludag.org.tr"
		       );

  aboutData.addAuthor("İsmail Dönmez", I18N_NOOP("Main Author"), "ismail@uludag.org.tr");
  
  KCmdLineArgs::init(argc, argv, &aboutData);
  KCmdLineArgs::addCmdLineOptions(options);
  //KCmdLineArgs::addCmdLineOptions();

  KApplication app(argc,argv);
  PackagerUI pack(0L,"");

  app.setMainWidget(&pack);
  pack.show();

  return app.exec();
}
