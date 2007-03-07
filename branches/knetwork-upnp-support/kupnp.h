#ifndef KUPNP_H
#define KUPNP_H

#include <miniupnpc/miniupnpc.h>

namespace KNetwork {

  class KUpnp
  {
  public:
    KUpnp();
    ~KUpnp();


    int addPortMapping(unsigned int externalPort, unsigned int internalPort);
    int addPortMapping(QString addr, unsigned int externalPort, unsigned int internalPort);

    int addPortRedirection(unsigned int port);
    int addPortRedirection(QString addr, unsigned int port);

    void removePortMapping(unsigned int port);

    static bool isBehindNat();

  private:
    struct UPNPUrls urls;
    struct IGDdatas data;
  };

}

#endif
