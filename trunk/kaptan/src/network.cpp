/*
  Copyright (c) 2004,2006 TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/
#include <qvbox.h>
#include <qlayout.h>

#include <qxembed.h>

#include <kprocess.h>
#include <klocale.h>
#include <kglobal.h>
#include <kcmodule.h>
#include <qframe.h>

#include <X11/Xlib.h>
#include <fixx11h.h>

#include "network.h"

Network::Network(QWidget *parent, const char* name)
    : NetworkDlg(parent, name)
{
    embed = new QXEmbed(networkFrame);
    embed->initialize();

    // FIXME: networkFrame->widht() || networkFrame->height() returns wrong value?
    embed->resize(606, 390);

    // embed buttonless network-manager into Kaptan
    proc = new KProcess(this);
    *proc << "kcmshell";
    *proc << "--embed-proxy";
    *proc << QString::number(embed->winId());
    *proc << "network-manager";

    // if process exits kill kcmshell
    connect(proc, SIGNAL(processExited(KProcess*)), this, SLOT(killProcess()));

    if (!proc->start(KProcess::NotifyOnExit))
    {
        delete proc;
        proc = 0L;
    }
}

Network::~Network()
{
    killProcess();
}

void Network::killProcess()
{
    if (embed && embed->embeddedWinId())
        XKillClient(qt_xdisplay(), embed->embeddedWinId());

    delete embed;
    embed = 0;

    delete proc;
    proc = 0;
}

#include "network.moc"
