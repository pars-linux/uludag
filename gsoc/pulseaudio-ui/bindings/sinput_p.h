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
#ifndef QTPULSEAUDIO_SINPUT_P_H
#define QTPULSEAUDIO_SINPUT_P_H

#include <QString>
#include "sinput.h"

namespace QtPulseAudio
{
class SinkInput::Private
{
    public:
    bool valid;
    
    uint32_t index;
    QString name;
    pa_sample_spec sampleSpec;
    pa_channel_map channelMap;
    uint32_t owner;
    pa_cvolume volume;
    int muted;
    QString driver;
    pa_proplist *proplist;
    pa_cvolume svolume;

    StreamManager* manager;
    Context *context;
};
}
#endif