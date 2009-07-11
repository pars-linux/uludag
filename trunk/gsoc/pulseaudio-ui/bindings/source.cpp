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

#include "source.h"
#include "sourcemanager.h"
#include "context.h"
#include "device_p.h"
#include "source_p.h"

using namespace std;

namespace QtPulseAudio
{

Source::Source(int index, QtPulseAudio::SourceManager* parent, Context *context): Device(index, parent), d(new Private)
{
    d->context = context;
}

Source::~Source()
{
    delete d;
}

void Source::update()
{
    pa_operation *o;
    o = pa_context_get_source_info_by_index(d->context->cObject(),
			(Device::d)->index, Source::source_cb, this);
    pa_operation_unref(o);
}

void Source::setVolume(pa_cvolume v)
{
    pa_operation *o;
    this->d->svolume = v;
    o = pa_context_set_source_volume_by_index(d->context->cObject(),
			(Device::d)->index, &d->svolume, Source::volume_cb, this);
    pa_operation_unref(o);
}

void Source::setMuted(int muted)
{
    pa_operation *o;
    o = pa_context_set_source_mute_by_index(d->context->cObject(),
			(Device::d)->index, muted, Source::volume_cb, this);
    pa_operation_unref(o);
}

void Source::source_cb(pa_context *, const pa_source_info *i, int eol, void *userdata)
{
    cout << "Source::source_cb" << endl;
    Source *p = reinterpret_cast<Source *>(userdata);
    Device::Private *dd = p->Device::d;

    if (eol) return;

    if (!i) {
	    cout << "Source callback failure" << endl;
	    return;
    }

    if ( dd->valid ) assert ( i->index == dd->index );

    //p->mSourceInfo = *i;
    cout << i->name << " " << i->description << endl;
    
    dd->name = QString(i->name);
    dd->description = QString(i->description);
    dd->sampleSpec = i->sample_spec;
    dd->channelMap = i->channel_map;
    dd->owner = i->owner_module;
    dd->volume = i->volume;
    dd->muted = i->mute;
    dd->monitor= i->monitor_of_sink;
    dd->monitorName = QString(i->monitor_of_sink_name);
    dd->latency = i->latency;
    dd->driver = QString(i->driver);
    dd->baseVolume = i->base_volume;
    dd->card = i->card;
    dd->configuredLatency = i->configured_latency;
    dd->valid = true;
    emit p->updated();
}

void Source::volume_cb(pa_context *, int success, void *userdata)
{
    cout << "Source::volume_cb" << endl;
    Source *p = reinterpret_cast<Source *>(userdata);
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
