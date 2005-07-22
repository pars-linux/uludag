/*
  Copyright 2005 UEKAE/TUBITAK
  Licensed under GNU GPLv2 or later at your option
*/

#ifndef PISI_H
#define PISI_H

#include <qobject.h>

class QStringList;
class KProcess;

class PisiManager : public QObject
{
  Q_OBJECT

 public:
  PisiManager();
  ~PisiManager();

  QStringList searchPackage(const QString& package);
  void removePackage(const QString& package);
  bool isInstalled(const QString& package);
  
  QString description(const QString& package);

 private:
  KProcess* m_pisiProcess;
};

#endif
