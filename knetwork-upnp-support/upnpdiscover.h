#ifndef UPNPDISCOVER_H
#define UPNPDISCOVER_H

#include <qthread.h>

class QObject;

class UPnpDiscover : QThread
{

 public:
  UPnpDiscover(QObject*);

  virtual void run();

 private:
  QObject* parent;

};

#endif
