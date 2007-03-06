#include <unistd.h>
#include "upnp.h"

int main()
{
  UPnP nat;
  nat.addPortRedirection("192.168.1.2",22);
  sleep(15);
  nat.removePortRedirection(22);

  return 0;
}
