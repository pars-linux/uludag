#ifndef KUPNP_H
#define KUPNP_H

#include <miniupnpc/miniupnpc.h>

namespace KNetwork {

class KUpnp
{
 public:
  KUpnp();
  ~KUpnp();


  void addPortMapping(unsigned int externalPort, unsigned int internalPort);
  void addPortMapping(QString addr, unsigned int externalPort, unsigned int internalPort);

  void addPortRedirection(unsigned int port);
  void addPortRedirection(QString addr, unsigned int port);

  void removePortMapping(unsigned int port);

  static bool isBehindNat();

 private:
  struct UPNPUrls urls;
  struct IGDdatas data;
};

}

#endif
