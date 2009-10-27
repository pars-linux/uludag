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

#ifndef QTPULSEAUDIO_DEVICE_H
#define QTPULSEAUDIO_DEVICE_H
#include <QString>
#include "stream.h"


namespace QtPulseAudio
{

class Device : public Stream
{
    Q_OBJECT
    public:
    ~Device();
    QString description();
    pa_usec_t latency();
    pa_usec_t configuredLatency();
    uint32_t monitor();
    QString monitorName();
    pa_volume_t baseVolume();
    uint32_t card();
   
    bool isValid();

    uint32_t index();
    QString name();
    pa_sample_spec sampleSpec();
    pa_channel_map channelMap();
    uint32_t owner();
    pa_cvolume volume();
    int muted();
    QString driver();
    QString getProperty(QString key);
    
    signals:
    void updated();
    
    public slots:
    virtual void update() = 0;
    virtual void setVolume(pa_cvolume volume) = 0;
    virtual void setMuted(int muted) = 0;
    
    protected:
    Device(int index, StreamManager *parent);
    class Private;
    Private *d;
};
}
#endif
