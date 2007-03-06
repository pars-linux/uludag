// Based on the xchat patch http://miniupnp.free.fr/files/xchat-upnp20061022.patch

#include <miniupnpc/miniwget.h>
#include <miniupnpc/upnpcommands.h>

#include <iostream>
using namespace std;

#include "upnp.h"

UPnP::UPnP()
{
  struct UPNPDev * devlist;
  struct UPNPDev * dev;
  char * descXML;
  int descXMLsize = 0;

  cout << "UPnP::UPnP" << endl;

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

UPnP::~UPnP()
{
}

bool UPnP::isBehindNat()
{
  struct UPNPDev * devlist;
  devlist = upnpDiscover(2000);

  if (!devlist)
    return false;
  else
    return true;
}

void UPnP::addPortRedirection(QString addr, unsigned int port)
{
  char port_str[16];
  int result;

  cout << "UPnP::addPortRedirection "<< addr << "," << port << endl;

  snprintf(port_str,15,"%d", port);
  result = UPNP_AddPortMapping(urls.controlURL, data.servicetype, port_str, port_str, addr.latin1(), 0, "TCP");

  if(!result)
    cout << "AddPortMapping failed" << endl;
}

void UPnP::removePortRedirection(unsigned int port)
{
  char port_str[16];

  cout << "UPnP::removePortRedirection " << port << endl;

  snprintf(port_str, 15, "%d", port);
  UPNP_DeletePortMapping(urls.controlURL, data.servicetype, port_str, "TCP");
}
