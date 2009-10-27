
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

#ifndef QTPULSEAUDIO_SINPUT_H
#define QTPULSEAUDIO_SINPUT_H
#include <QString>
#include "stream.h"


namespace QtPulseAudio
{
class Context;
class SinkInputManager;
class SinkInput : public Stream
{
    Q_OBJECT
    public:
    ~SinkInput();
   
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
    virtual void update();
    virtual void setVolume(pa_cvolume volume);
    virtual void setMuted(int muted);
    
    protected:
    friend class SinkInputManager;
    SinkInput(int index, StreamManager *parent, Context *context);
    class Private;
    Private *d;
    static void sink_input_cb(pa_context *, const pa_sink_input_info *i, int eol, void *userdata);
    static void volume_cb(pa_context *, int success, void *userdata);
};
}
#endif
