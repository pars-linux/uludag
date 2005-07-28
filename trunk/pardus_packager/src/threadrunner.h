/*
  Copyright 2005 UEKAE/TUBITAK
  Licensed under GNU GPLv2 or later at your option
*/

#ifndef THREADRUNNER_H
#define THREADRUNNER_H

#include <qthread.h>
#include <qstringlist.h>
#include <kprocess.h>

class QString;

class ThreadRunner : public QObject, public QThread
{
  Q_OBJECT;

 public:
  ThreadRunner();
  ~ThreadRunner();

  virtual void run();
  void setCommand(const QString& command);
  void setArguments(const QString& arguments);

 protected slots:
  void processExited(int state);

 signals:
  void searchResults(bool success, const QStringList& results);

 private:
  void parseOutput(KProcess* proc,char * buffer, int len);

  KProcess m_process;
  QString m_command;
  QString m_arguments;
  QStringList m_output;
};

#endif
