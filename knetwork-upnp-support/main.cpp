#include <unistd.h>
#include <kapplication.h>
#include <kcmdlineargs.h>
#include <kaboutdata.h>
#include <kdebug.h>
#include "kupnp.h"

#include <iostream>
using namespace std;

using namespace KNetwork;

int
main(int argc, char *argv[])
{
  KAboutData about("upnp_test", "upnp_test", "0.0.1");
  KCmdLineArgs::init(argc, argv, &about);
  KApplication a;

  KUpnp nat;

  nat.addPortRedirection(22);
  sleep(10);
  nat.removePortMapping(22);

  cout << "External ip adress is " << nat.getExternalIpAddress() << endl;

  return 0;
}
