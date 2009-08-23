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
#ifndef PANDA_MAINWINDOW_H
#define PANDA_MAINWINDOW_H
#include "ui_mainwindow.h"
#include "../bindings/context.h"

#include <kpagedialog.h>
#include <Qt/QtGui>

class StreamsTab;
class GroupsTab;
class GroupManager;
class PandaTrayIcon;

class MainWindow: public QMainWindow, private Ui::MainWindow
{
    Q_OBJECT
    public:
    MainWindow(QtPulseAudio::Context *context, QMainWindow *parent = 0);
    void toggleVisibility();
    public slots:
    void contextReady();
    void showSettings(bool val);
    void settingsPageChanged(KPageWidgetItem *,KPageWidgetItem *);
    
    protected:
    QtPulseAudio::Context *context;
    QTabWidget *tabWidget;
    StreamsTab *sinksTab;
    StreamsTab *sourcesTab;

    private:
    GroupsTab* groupsTab;

    private:
    GroupManager *groupManager;
    KIcon *icon;
    KPageDialog *settingsDialog;
    PandaTrayIcon *trayIcon;
    void createTray();
    friend class PandaTrayIcon;
};
#endif