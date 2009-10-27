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
#include <iostream>

#include "sink.h"
#include "sinkmanager.h"
#include "context.h"
#include "device_p.h"
#include "sink_p.h"

using namespace std;

namespace QtPulseAudio
{

Sink::Sink(int index, QtPulseAudio::SinkManager* parent, Context *context): Device(index, parent), d(new Private)
{
    d->context = context;
}

Sink::~Sink()
{
    delete d;
}

void Sink::update()
{
    pa_operation *o;
    o = pa_context_get_sink_info_by_index(d->context->cObject(),
			(Device::d)->index, Sink::sink_cb, this);
    pa_operation_unref(o);
}

void Sink::setVolume(pa_cvolume v)
{
    pa_operation *o;
    this->d->svolume = v;
    o = pa_context_set_sink_volume_by_index(d->context->cObject(),
			(Device::d)->index, &d->svolume, Sink::volume_cb, this);
    pa_operation_unref(o);
}

void Sink::setMuted(int muted)
{
    pa_operation *o;
    o = pa_context_set_sink_mute_by_index(d->context->cObject(),
			(Device::d)->index, muted, Sink::volume_cb, this);
    pa_operation_unref(o);
}

void Sink::sink_cb(pa_context *, const pa_sink_info *i, int eol, void *userdata)
{
    cout << "Sink::sink_cb" << endl;
    Sink *p = reinterpret_cast<Sink *>(userdata);
    Device::Private *dd = p->Device::d;

    if (eol) return;

    if (!i) {
	    cout << "Sink callback failure" << endl;
	    return;
    }

    if ( dd->valid ) assert ( i->index == dd->index );

    //p->mSinkInfo = *i;
    cout << i->name << " " << i->description << endl;
    
    dd->name = QString(i->name);
    dd->description = QString(i->description);
    dd->sampleSpec = i->sample_spec;
    dd->channelMap = i->channel_map;
    dd->owner = i->owner_module;
    dd->volume = i->volume;
    dd->muted = i->mute;
    dd->monitor= i->monitor_source;
    dd->monitorName = QString(i->monitor_source_name);
    dd->latency = i->latency;
    dd->driver = QString(i->driver);
    dd->baseVolume = i->base_volume;
    dd->card = i->card;
    dd->configuredLatency = i->configured_latency;
    dd->valid = true;
    if(dd->proplist != 0)
	pa_proplist_free(dd->proplist);
    dd->proplist = pa_proplist_copy(i->proplist);
    emit p->updated();
}

void Sink::volume_cb(pa_context *, int success, void *userdata)
{
    cout << "Sink::volume_cb" << endl;
    Sink *p = reinterpret_cast<Sink *>(userdata);
    /*if(p->(Device::d)->volumeOperation != 0)
    {
	pa_operation_unref(p->(Device::d)->volumeOperation);
	p->(Device::d)->volumeOperation = 0;
    }*/

    if (!success) {
        cout << "Volume/mute change failure" << endl;
        return;
    }
}

}
