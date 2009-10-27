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
#ifndef QTPULSEAUDIO_SOURCE_P_H
#define QTPULSEAUDIO_SOURCE_P_H

#include <QVector>
#include <QPointer>

#include "source.h"

namespace QtPulseAudio
{
class Context;
class Source::Private
{
    public:
    pa_cvolume svolume;
    Context *context;
};
}

#endif