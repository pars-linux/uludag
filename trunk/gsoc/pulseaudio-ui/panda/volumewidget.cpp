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
#include <iostream>
#include "../bindings/stream.h"
#include "volumewidget.h"

VolumeWidget::VolumeWidget(QWidget *parent):QWidget(parent)
{
    slidersWidget = new QWidget(this);
    slidersLayout = new QHBoxLayout(slidersWidget);
    configWidget = new QWidget(this);
    configLayout = new QHBoxLayout(configWidget);
    connectedButton = new QPushButton("joined", configWidget);
    connectedButton->setCheckable(true);
    configLayout->addWidget(connectedButton);
    layout = new QVBoxLayout(this);
    layout->addWidget(slidersWidget);
    layout->addWidget(configWidget);
}

void VolumeWidget::bind(QtPulseAudio::Stream *s)
{
    std::cout << "binding" << std::endl;
    stream = s;
    if(s->isValid())
        setup();
    else
        QObject::connect(s, SIGNAL(updated()), this, SLOT(setup()));
}

void VolumeWidget::unbind()
{
    if(stream == 0)
        return;
    QObject::disconnect(0, 0, this, SLOT(setup()));
    stream = 0;
    foreach(QSlider *s, sliders)
    {
        slidersLayout->removeWidget(s);
        delete s;
    }
}

void VolumeWidget::setup()
{
    std::cout << "setting" << endl;
    if(!stream || !stream->isValid())
        return;
    //once we're set up, there's no need do do it again
    QObject::disconnect(0, 0, this, SLOT(setup()));
    int n = stream->volume().channels;
    connectedButton->setChecked(true);
    pa_volume_t v = stream->volume().values[0];
    for(int i=0;i<n;++i)
    {
        QSlider *s = new QSlider(this);
        s->setMinimum(0);
        s->setMaximum(65536); //FIXME: maybe there's a constant for this
        s->setValue(stream->volume().values[i]);
	s->setTracking(true);
        if(stream->volume().values[i])
            connectedButton->setChecked(false);
        sliders.push_back(s);
        slidersLayout->addWidget(s);
	QObject::connect(s, SIGNAL(sliderMoved(int)), this, SLOT(sliderMoved(int)));
    }
    QObject::connect(stream, SIGNAL(updated()), this, SLOT(volumeChanged()));
    setLayout(layout);
}

void VolumeWidget::valuesFromStream()
{
    int n = stream->volume().channels;
    Q_ASSERT(n == sliders.size());
    for(int i=0;i<n;++i)
        sliders[i]->setValue(stream->volume().values[i]);
}

bool VolumeWidget::moving()
{
    foreach(QSlider *s, sliders)
        if(s->isSliderDown())
            return true;
    return false;
}

void VolumeWidget::volumeChanged()
{
    std::cerr << "VolumeWidget::volumeChanged()" << std::endl;
    if(!moving())
    {
	std::cerr << "updating" << std::endl;
        valuesFromStream();
    }
}

void VolumeWidget::sliderMoved(int value)
{
    QSlider *slider = qobject_cast<QSlider *>(sender());
    Q_ASSERT(slider != 0);
    pa_cvolume v;
    v.channels = sliders.size();
    if(connectedButton->isChecked())
        foreach(QSlider *s, sliders)
            if(s != slider)
               s->setValue(slider->value());
    for(int i=0;i<sliders.size();++i)
        v.values[i] = sliders[i]->value();
    stream->setVolume(v);
}
