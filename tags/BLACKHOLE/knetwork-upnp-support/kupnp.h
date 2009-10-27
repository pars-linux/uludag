#ifndef KUPNP_H
#define KUPNP_H

#include <miniupnpc/miniupnpc.h>

namespace KNetwork {

  class KUpnp
  {
  public:
    KUpnp();
    ~KUpnp();

    int addPortMapping(unsigned int externalPort, unsigned int internalPort, const char* protocol="TCP");
    int addPortMapping(QCString addr, unsigned int externalPort, unsigned int internalPort, const char* protocol="TCP");

    int addPortRedirection(unsigned int port, const char* protocol="TCP");
    int addPortRedirection(QCString addr, unsigned int port, const char* protocol="TCP");

    void removePortMapping(unsigned int port, const char* protocol="TCP");

    QCString getExternalIpAddress();

    static bool isBehindNat();

  private:
    struct UPNPUrls urls;
    struct IGDdatas data;
    static struct UPNPDev * devlist;
  };

}

#endif
