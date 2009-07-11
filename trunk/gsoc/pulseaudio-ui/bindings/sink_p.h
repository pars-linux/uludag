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
#ifndef QTPULSEAUDIO_SINK_P_H
#define QTPULSEAUDIO_SINK_P_H

#include <QVector>
#include <QPointer>

#include "sink.h"

namespace QtPulseAudio
{
class Context;
class Sink::Private
{
    public:
    pa_cvolume svolume;
    Context *context;
};
}

#endif