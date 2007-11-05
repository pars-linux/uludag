#include <qstring.h>

#include <kcmdlineargs.h>
#include <kaboutdata.h>
#include <kapplication.h>

#include "authdialog.h"
#include "policykitkde.h"

int main (int argc, char *argv[])
{
    KAboutData aboutData( "policykit-kde", I18N_NOOP( "PolicyKit-kde" ), "0.1",
                        I18N_NOOP( "PolicyKit-kde" ), KAboutData::License_GPL,
                        I18N_NOOP( "(c) 2005-2007, TUBITAK - UEKAE" ) );
    aboutData.addAuthor( "Gökçen Eraslan", I18N_NOOP( "Current Maintainer" ), "gokcen@pardus.org.tr" );
    KCmdLineArgs::init( argc, argv, &aboutData );

    KApplication app;

    PolicyKitKDE pkKDE;
    return app.exec();
}
