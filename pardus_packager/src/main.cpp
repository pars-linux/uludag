/*
  Copyright 2005 UEKAE/TUBITAK
  Licensed under GNU GPLv2 or later at your option
*/

#include <kapplication.h>
#include <kcmdlineargs.h>
#include <klocale.h>
#include <kaboutdata.h>

#include "packager_ui.h"

static const KCmdLineOptions options[] = 
  {
    KCmdLineLastOption
  };

int main(int argc, char** argv)
{

  KAboutData aboutData(
		       "packager",
		       I18N_NOOP("Pardus Paket Yoneticisi"),
		       "0.0.1",
		       "Pardus Linux için paket yoneticisi",
		       KAboutData::License_GPL,
		       I18N_NOOP("(C) 2005 UEKAE/TUBITAK"),
		       I18N_NOOP("Pardus paket yoneticisiyle paketleriniz nazara gelmez!"),
		       "http://www.uludag.org.tr"
		       );

  aboutData.addAuthor("İsmail Dönmez", I18N_NOOP("Kodu ilk yazan insan evladı"), "ismail@uludag.org.tr");
  
  KCmdLineArgs::init(argc, argv, &aboutData);
  KCmdLineArgs::addCmdLineOptions(options);
  //KCmdLineArgs::addCmdLineOptions();

  KApplication app(argc,argv);
  Packager_UI pack(0L,"");

  app.setMainWidget(&pack);
  pack.show();

  return app.exec();
}
