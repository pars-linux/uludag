/*
    Copyright (c) 2009      by Marcin Kurczych          <tharkang@gmail.com>
    Copyright (c) 2007      by Nicolas Peyron

    *************************************************************************
    *                                                                       *
    * This library is free software; you can redistribute it and/or         *
    * modify it under the terms of the GNU Lesser General Public            *
    * License as published by the Free Software Foundation; either          *
    * version 2 of the License, or (at your option) any later version.      *
    *                                                                       *
    *************************************************************************
*/
#ifndef QTPULSEAUDIO_DEVICE_P_H
#define QTPULSEAUDIO_DEVICE_P_H

#include <QString>
#include "device.h"

namespace QtPulseAudio
{
class Sink;
class Source;
class Device::Private
{
    public:
    bool valid;
    
    QString description;
    pa_usec_t latency;
    pa_usec_t configuredLatency;
    uint32_t monitor;
    QString monitorName;
    pa_volume_t baseVolume;
    uint32_t card;
    uint32_t index;
    QString name;
    pa_sample_spec sampleSpec;
    pa_channel_map channelMap;
    uint32_t owner;
    pa_cvolume volume;
    int muted;
    QString driver;
    pa_proplist *proplist;
    friend class Sink;
    friend class Source;

    StreamManager* manager;
};
}
#endif