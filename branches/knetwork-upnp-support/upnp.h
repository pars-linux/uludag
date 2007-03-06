#ifndef UPNP_H
#define UPNP_H

#include <miniupnpc/miniupnpc.h>
#include <qstring.h>

class UPnP
{
 public:
  UPnP();
  ~UPnP();

  void addPortRedirection(QString ip, unsigned int port);
  void removePortRedirection(unsigned int port);
  bool isBehindNat();

 private:
  struct UPNPUrls urls;
  struct IGDdatas data;
};

#endif
