#include <unistd.h>
#include "upnp.h"

int main()
{
  UPnP nat;
  nat.addPortMapping("192.168.1.2",22);
  sleep(15);
  nat.removePortMapping(22);

  return 0;
}
