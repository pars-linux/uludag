
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
#ifndef QTPULSEAUDIO_STREAMMANAGER_P_H
#define QTPULSEAUDIO_STREAMMANAGER_P_H

#include <QString>
#include <QHash>

#include "streammanager.h"

namespace QtPulseAudio
{

class Context;
class Stream;

class StreamManager::Private
{
public:
    QHash<int, Stream *> streamsById;
    QHash<QString, Stream *> streamsByName;
    Context *context;
    StreamManager *q;
    bool autoUpdate;
};
}
#endif