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
#ifndef PANDA_VOLUMEWIDGET_H
#define PANDA_VOLUMEWIDGET_H
#include <Qt/QtGui>

namespace QtPulseAudio {class Stream;}

class VolumeWidget: public QWidget
{
    Q_OBJECT
    public:
    VolumeWidget(QWidget *parent);
    public slots:
    void volumeChanged();
    void sliderMoved(int value);
    void bind(QtPulseAudio::Stream *s);
    void unbind();
    void setup();
    protected:
    void valuesFromStream();
    bool moving();
    QVector<QSlider *> sliders;
    QVBoxLayout *layout;
    QHBoxLayout *slidersLayout;
    QHBoxLayout *configLayout;
    QPushButton *connectedButton;
    QtPulseAudio::Stream *stream;

    private:
    QWidget* slidersWidget;

    QWidget* configWidget;
};
#endif
