/*
  Copyright 2005 UEKAE/TUBITAK
  Licensed under GNU GPLv2 or later at your option
*/

#include <kprocess.h>
#include <qstring.h>

#include "threadrunner.h"

ThreadRunner::ThreadRunner()
{
  QObject::connect(&m_process,SIGNAL(processExited(int)),this,SLOT(processExited(int)));
}

ThreadRunner::~ThreadRunner()
{
}

void ThreadRunner::run()
{
  if(m_command.isEmpty() || m_arguments.isEmpty())
    return;
  else
    {
      m_process << m_command;
      m_process << m_arguments;
      m_process.start(KProcess::NotifyOnExit);
    }
}

void ThreadRunner::setCommand(const QString& command)
{
  m_command = command;
}

void ThreadRunner::setArguments(const QString& arguments)
{
  m_arguments = arguments;
}

void ThreadRunner::processExited(int state)
{
  if( state != 0 )
    emit result(false);
  else
    emit result(true);
}
 
#include "threadrunner.moc"
