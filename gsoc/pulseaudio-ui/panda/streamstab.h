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
#ifndef PANDA_SINKSTAB_H
#define PANDA_SINKSTAB_H
#include <Qt/QtGui>
#include "ui_sinkstab.h"

namespace QtPulseAudio {class StreamManager;}

class VolumeWidget;

class StreamsTab: public QWidget
{
    Q_OBJECT
    public:
    StreamsTab(QtPulseAudio::StreamManager *manager, QWidget *parent = 0);
    public slots:
    void streamSelected(int);
    void streamAdded(int);
    void streamRemoved(int);
    void streamChanged(int);
    private:
    QtPulseAudio::StreamManager *manager;
    QVBoxLayout *layout;
    QLabel *streamLabel;
    QComboBox *streamComboBox;
    QFormLayout* formLayout;
    VolumeWidget* volumeWidget;
    QWidget* formWidget;
};
#endif
