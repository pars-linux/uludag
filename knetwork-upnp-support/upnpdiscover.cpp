#include <qevent.h>
#include <qobject.h>
#include <miniupnpc/miniupnpc.h>
#include "upnpdiscover.h"

UPnpDiscover::UPnpDiscover(QObject* parent)
{
  this->parent = parent;
}

void UPnpDiscover::run()
{
  struct UPNPDev * devlist;
  devlist = upnpDiscover(500);

  // TODO post event here
}
