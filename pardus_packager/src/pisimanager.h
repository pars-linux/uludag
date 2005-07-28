/*
  Copyright 2005 UEKAE/TUBITAK
  Licensed under GNU GPLv2 or later at your option
*/

#ifndef PISI_H
#define PISI_H

#include <qobject.h>

#include "threadrunner.h"

class QStringList;
class KProcess;

class PisiManager : public QObject
{
  Q_OBJECT

 public:
  PisiManager();
  ~PisiManager();

  void searchPackage(const QString& package);
  void removePackage(const QString& package);
  bool isInstalled(const QString& package);
  
  QString description(const QString& package);

 protected slots:
  void searchFinished(bool success, const QStringList& results);

 signals:
  void searchResults(bool success, const QStringList& packageList);
  
 private:
  ThreadRunner threadRunner;
};

#endif
