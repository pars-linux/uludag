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
#ifndef QTPULSEAUDIO_SINPUTMANAGER_H
#define QTPULSEAUDIO_SINPUTMANAGER_H

#include <QObject>

#include <pulse/pulseaudio.h>

#include "streammanager.h"

namespace QtPulseAudio
{
class Context;
class SinkInput;

class SinkInputManager : public StreamManager
{
    Q_OBJECT
    public:
    virtual Stream *create(int index);
    static void sink_input_cb(pa_context *, const pa_sink_input_info *i, int eol, void *userdata);

    public slots:
    virtual void update();

    protected:
    friend class Context;
    SinkInputManager(Context *parent, bool autoUpdate = true);
    ~SinkInputManager();
};
}

#endif