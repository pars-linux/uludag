#include <kapplication.h>
#include <kcmdlineargs.h>
#include <kaboutdata.h>
#include "kupnp.h"

using namespace KNetwork;

int
main(int argc, char *argv[])
{
   KAboutData about("kapptest", "kapptest", "version");
   KCmdLineArgs::init(argc, argv, &about);

   KApplication a;

    KUpnp nat;
    nat.addPortRedirection(22);

    return 0;
}

