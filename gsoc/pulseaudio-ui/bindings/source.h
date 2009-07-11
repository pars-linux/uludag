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
#ifndef QTPULSEAUDIO_SOURCE_H
#define QTPULSEAUDIO_SOURCE_H

#include <QObject>

#include <pulse/pulseaudio.h>

#include "device.h"

namespace QtPulseAudio {

class SourceManager;
class Context;

class Source: public Device
{
    Q_OBJECT
    signals:
    void updated();
    
    public slots:
    virtual void update();
    virtual void setVolume(pa_cvolume volume);
    virtual void setMuted(int muted);
    
    protected:
    class Private;
    friend class Private;
    Private *d;
    friend class SourceManager;
    Source(int index, SourceManager *parent = NULL, Context *context = NULL);
    ~Source();
    static void source_cb(pa_context *, const pa_source_info *i, int eol, void *userdata);
    static void volume_cb(pa_context *, int success, void *userdata);
};

}

#endif
