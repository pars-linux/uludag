/*
  Copyright 2005 UEKAE/TUBITAK
  Licensed under GNU GPLv2 or later at your option
*/

#include <qstringlist.h>

#include "pisimanager.h"

PisiManager::PisiManager()
{
  connect(&threadRunner,SIGNAL(searchResult(bool,const QStringList&)),this,SLOT(searchFinished(bool,const QStringList&)));
}

PisiManager::~PisiManager()
{
}

void PisiManager::searchPackage(const QString& package)
{
  QString command = "pisi-cli --search "+package;
  threadRunner.setCommand(command);
  threadRunner.run();
}

void PisiManager::searchFinished(bool success, const QStringList& results)
{
  emit searchResults(success,results);
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
