/*
  Copyright (c) 2004,2006 TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef NETWORK_H
#define NETWORK_H

#include "networkdlg.h"

class QXEmbed;
class KProcess;

class Network:public NetworkDlg
{
    Q_OBJECT

public:
    Network(QWidget *parent = 0, const char* name = 0);
    ~Network();

    void embedManager();

protected slots:
    void killProcess();

private:
    QXEmbed *embed;
    KProcess *proc;
};

#endif // NETWORK_H
