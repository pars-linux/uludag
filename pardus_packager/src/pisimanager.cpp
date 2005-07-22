/*
  Copyright 2005 UEKAE/TUBITAK
  Licensed under GNU GPLv2 or later at your option
*/

#include <qstringlist.h>
#include <kprocess.h>

#include "pisimanager.h"

PisiManager::PisiManager()
{
}

PisiManager::~PisiManager()
{
}

QStringList PisiManager::searchPackage(const QString& /*package*/)
{
  return "";
}

void PisiManager::removePackage(const QString& /*package*/)
{
}

bool PisiManager::isInstalled(const QString& /*package*/)
{
  return false;
}

QString PisiManager::description(const QString& /*package*/)
{
  return "";
}

#include "pisimanager.moc"
