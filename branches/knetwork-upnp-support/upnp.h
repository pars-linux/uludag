#ifndef UPNP_H
#define UPNP_H

#include <miniupnpc/miniupnpc.h>
#include <qstring.h>

class UPnP
{
 public:
  UPnP();
  ~UPnP();

  void addPortMapping(QString ip, unsigned int port);
  void removePortMapping(unsigned int port);
  bool isBehindNat();

 private:
  struct UPNPUrls urls;
  struct IGDdatas data;
};

#endif
