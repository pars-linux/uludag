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
#include "streamstab.h"
#include "volumewidget.h"
#include "../bindings/streammanager.h"
#include "../bindings/stream.h"
#include <iostream>

StreamsTab::StreamsTab(QtPulseAudio::StreamManager *manager, QWidget *parent):QWidget(parent)
{
    formWidget = new QWidget(this);
    formLayout = new QFormLayout(formWidget);
    streamLabel = new QLabel("Card", formWidget);
    streamComboBox = new QComboBox(formWidget); 
    formLayout->addRow(streamLabel, streamComboBox);
    volumeWidget = new VolumeWidget(this);
    layout = new QVBoxLayout(this);
    layout->addWidget(formWidget);
    layout->addWidget(volumeWidget);
    this->manager = manager;
    QtPulseAudio::Stream *s;
    QObject::connect(this->manager, SIGNAL(added(int)), this, SLOT(streamAdded(int)));
    QObject::connect(this->manager, SIGNAL(removed(int)), this, SLOT(streamRemoved(int)));
    QObject::connect(this->manager, SIGNAL(changed(int)), this, SLOT(streamChanged(int)));
    QObject::connect(this->streamComboBox, SIGNAL(currentIndexChanged(int)), this, SLOT(streamSelected(int)));
    manager->update();
}

void StreamsTab::streamSelected(int combo_index)
{
    int stream_index = streamComboBox->itemData(combo_index).toInt();
    volumeWidget->bind(manager->stream(stream_index));
    std::cout << "Stream selected" << std::endl;
}

void StreamsTab::streamAdded(int stream_index)
{
    QtPulseAudio::Stream *s = manager->stream(stream_index);
    bool first = streamComboBox->count() == 0;
    std::cout << s->name().toStdString() << std::endl;
    std::cout << s->description().toStdString() << std::endl;
    streamComboBox->addItem(s->name(), stream_index);
    if(first)
	streamSelected(0);
    std::cout << "Stream added" << std::endl;
}

void StreamsTab::streamRemoved(int stream_index)
{
    //what if removed item is current one?
    int combo_index = streamComboBox->findData(stream_index);
    streamComboBox->removeItem(combo_index);
}

void StreamsTab::streamChanged(int stream_index)
{
}