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

#include <Qt/QtGui>

class StreamsTab;

class MainWindow: public QMainWindow, private Ui::MainWindow
{
    Q_OBJECT
    public:
    MainWindow(QtPulseAudio::Context *context, QMainWindow *parent = 0);
    public slots:
    void contextReady();
    protected:
    QtPulseAudio::Context *context;
    QTabWidget *tabWidget;
    StreamsTab *sinksTab;
    StreamsTab *sourcesTab;
};
#endif
