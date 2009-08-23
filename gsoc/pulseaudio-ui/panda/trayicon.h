/*
    Copyright (c) 2009      by Marcin Kurczych          <tharkang@gmail.com>

    *************************************************************************
    *                                                                       *
    * This program is free software; you can redistribute it and/or modify  *
    * it under the terms of the GNU General Public License as published by  *
    * the Free Software Foundation; either version 2 of the License, or     *
    * (at your option) any later version.                                   *
    *                                                                       *
    *************************************************************************
*/
#ifndef PANDA_TRAYICON_H
#define PANDA_TRAYICON_H
#include "../bindings/context.h"

#include <Qt/QtGui>
#include <ksystemtrayicon.h>

class MainWindow;

class PandaTrayIcon: public KSystemTrayIcon
{
    Q_OBJECT
    public:
    PandaTrayIcon(MainWindow *parent);
    void createActions();
    
    private slots:
    void trayActivated(QSystemTrayIcon::ActivationReason);
    private:
    MainWindow* mainWindow;
};

#endif