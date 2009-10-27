// Based on the xchat patch http://miniupnp.free.fr/files/xchat-upnp20061022.patch

#include <miniupnpc/miniwget.h>
#include <miniupnpc/upnpcommands.h>

#include <cstdlib>
#include <qcstring.h>
#include <qstringlist.h>
#include <kdebug.h>

#include "kupnp.h"
#include "kstreamsocket.h"

namespace KNetwork {

  struct UPNPDev* KUpnp::devlist = NULL;

  KUpnp::KUpnp()
  {
    struct UPNPDev * dev;
    char * descXML;
    int descXMLsize = 0;

    kdDebug() << "KUpnp::KUpnp" << endl;

    memset(&urls, 0, sizeof(struct UPNPUrls));
    memset(&data, 0, sizeof(struct IGDdatas));

    if(!devlist) // It might already be initialized in ::isBehindNat()
      devlist = upnpDiscover(500);

    if (devlist)
      {
        dev = devlist;

        while (dev)
          {
            if (strstr (dev->st, "InternetGatewayDevice"))
              break;
            dev = dev->pNext;
          }

        if (!dev)
          dev = devlist; /* defaulting to first device */

        descXML = (char*)miniwget(dev->descURL, &descXMLsize);

        if (descXML)
          {
            parserootdesc (descXML, descXMLsize, &data);
            free (descXML); descXML = 0;
            GetUPNPUrls (&urls, &data, dev->descURL);
          }
        freeUPNPDevlist(devlist);
      }
  }

  KUpnp::~KUpnp()
  {
  }

  bool KUpnp::isBehindNat()
  {
    devlist = upnpDiscover(500);

    if (!devlist)
      return false;
    else
      return true;
  }

  int KUpnp::addPortRedirection(unsigned int port, const char* protocol)
  {
    return addPortMapping("", 0, port, protocol);
  }

  int  KUpnp::addPortRedirection(QCString addr, unsigned int port, const char* protocol)
  {
    return addPortMapping(addr, 0, port, protocol);
  }

  int KUpnp::addPortMapping(QCString addr, unsigned int externalPort, unsigned int internalPort, const char* protocol)
  {
    int result;
    QCString extPort, intPort;
    KStreamSocket socket;
    QCString modem, modem_port;

    if (externalPort == 0)
      externalPort = internalPort;

    if (addr.isEmpty())
      {
        modem = (QStringList::split('/',urls.controlURL)[1]).section(':',0,0);
        modem_port = (QStringList::split('/',urls.controlURL)[1]).section(':',1,1);

        socket.setBlocking(true);
        socket.connect(modem,modem_port);
        addr = socket.localAddress().nodeName();
      }

    extPort.setNum(externalPort);
    intPort.setNum(internalPort);

    result = UPNP_AddPortMapping(urls.controlURL, data.servicetype, extPort, intPort, addr.data(), 0, protocol);

    if(!result)
      {
        kdDebug() << "AddPortMapping failed" << endl;
        return -1;
      }

    return 0;
  }

  void KUpnp::removePortMapping(unsigned int port, const char* protocol)
  {
    QCString portNumber;
    portNumber.setNum(port);

    kdDebug() << "KUpnp::removePortRedirection " << portNumber << endl;

    UPNP_DeletePortMapping(urls.controlURL, data.servicetype, portNumber, protocol);
  }

  QCString KUpnp::getExternalIpAddress()
  {
    char address[16+1];

    UPNP_GetExternalIPAddress(urls.controlURL, data.servicetype, address);

    return address;
  }

}
