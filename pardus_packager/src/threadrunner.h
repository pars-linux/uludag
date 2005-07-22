/*
  Copyright 2005 UEKAE/TUBITAK
  Licensed under GNU GPLv2 or later at your option
*/

#ifndef THREADRUNNER_H
#define THREADRUNNER_H

#include <qthread.h>

class QString;
class KProcess;

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
  void result(bool success);

 private:
  KProcess m_process;
  QString m_command;
  QString m_arguments;
};

#endif
