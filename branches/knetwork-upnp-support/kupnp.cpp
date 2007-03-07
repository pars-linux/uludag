// Based on the xchat patch http://miniupnp.free.fr/files/xchat-upnp20061022.patch

#include <miniupnpc/miniwget.h>
#include <miniupnpc/upnpcommands.h>

#include <cstdlib>
#include <qstring.h>
#include <qstringlist.h>
#include <kdebug.h>

#include "kupnp.h"
#include "kstreamsocket.h"

namespace KNetwork {

  KUpnp::KUpnp()
  {
    struct UPNPDev * devlist;
    struct UPNPDev * dev;
    char * descXML;
    int descXMLsize = 0;

    kdDebug() << "KUpnp::KUpnp" << endl;

    memset(&urls, 0, sizeof(struct UPNPUrls));
    memset(&data, 0, sizeof(struct IGDdatas));

    devlist = upnpDiscover(2000);
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
    struct UPNPDev * devlist;
    devlist = upnpDiscover(2000);

    if (!devlist)
      return false;
    else
      return true;
  }

  int KUpnp::addPortRedirection(unsigned int port)
  {
    return addPortMapping("", 0, port);
  }

  int  KUpnp::addPortRedirection(QString addr, unsigned int port)
  {
    return addPortMapping(addr, 0, port);
  }

  int KUpnp::addPortMapping(QString addr, unsigned int externalPort, unsigned int internalPort)
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

    result = UPNP_AddPortMapping(urls.controlURL, data.servicetype, extPort, intPort, addr.latin1(), 0, "TCP");

    if(!result)
      {
        kdDebug() << "AddPortMapping failed" << endl;
        return -1;
      }

    return 0;
  }

  void KUpnp::removePortMapping(unsigned int port)
  {
    QCString portNumber;
    portNumber.setNum(port);

    kdDebug() << "KUpnp::removePortRedirection " << portNumber << endl;

    UPNP_DeletePortMapping(urls.controlURL, data.servicetype, portNumber, "TCP");
  }

}
