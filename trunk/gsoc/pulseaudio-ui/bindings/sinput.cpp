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

#include "sinput.h"
#include "context.h"
#include "sinput_p.h"

using namespace std;

namespace QtPulseAudio
{

SinkInput::SinkInput(int index, StreamManager* parent, Context *context): Stream(parent), d(new Private)
{
    d->index = index;
    d->manager = parent;
    d->context = context;
    d->valid = false;
    d->proplist = 0;
}

SinkInput::~SinkInput()
{
    delete d;
}

uint32_t SinkInput::index()
{
    return d->index;
}

QString SinkInput::name()
{
    return d->name;
}

bool SinkInput::isValid()
{
    return d->valid;
}


int SinkInput::muted()
{
    return d->muted;
}

pa_cvolume SinkInput::volume()
{
    return d->volume;
}


uint32_t SinkInput::owner()
{
    return d->owner;
}

QString SinkInput::driver()
{
    return d->driver;
}

pa_channel_map SinkInput::channelMap()
{
    return d->channelMap;
}


pa_sample_spec SinkInput::sampleSpec()
{
    return d->sampleSpec;
}


QString SinkInput::getProperty(QString key)
{
    cerr << "getProperty " << key.toStdString() << endl;
    cerr << " in stream " << index() << " valid " << isValid() << endl;
    return QString(pa_proplist_gets(d->proplist, key.toUtf8().data()));
}

void SinkInput::update()
{
    pa_operation *o;
    o = pa_context_get_sink_input_info(d->context->cObject(),
			d->index, SinkInput::sink_input_cb, this);
    pa_operation_unref(o);
}

void SinkInput::setVolume(pa_cvolume v)
{
    pa_operation *o;
    this->d->svolume = v;
    o = pa_context_set_sink_input_volume(d->context->cObject(),
			d->index, &d->svolume, SinkInput::volume_cb, this);
    pa_operation_unref(o);
}

void SinkInput::setMuted(int muted)
{
    pa_operation *o;
    o = pa_context_set_sink_input_mute(d->context->cObject(),
			d->index, muted, SinkInput::volume_cb, this);
    pa_operation_unref(o);
}

void SinkInput::sink_input_cb(pa_context *, const pa_sink_input_info *i, int eol, void *userdata)
{
    cout << "SinkInput::sink_cb" << endl;
    SinkInput *p = reinterpret_cast<SinkInput *>(userdata);
    SinkInput::Private *dd = p->d;

    if (eol) return;

    if (!i) {
	    cout << "Sink callback failure" << endl;
	    return;
    }

    if ( dd->valid ) assert ( i->index == dd->index );

    //p->mSinkInfo = *i;
    
    dd->name = QString(i->name);
    dd->sampleSpec = i->sample_spec;
    dd->channelMap = i->channel_map;
    dd->owner = i->owner_module;
    dd->volume = i->volume;
    dd->muted = i->mute;
    dd->driver = QString(i->driver);
    dd->valid = true;
    if(dd->proplist != 0)
	pa_proplist_free(dd->proplist);
    dd->proplist = pa_proplist_copy(i->proplist);
    emit p->updated();
}

void SinkInput::volume_cb(pa_context *, int success, void *userdata)
{
    cout << "Sink::volume_cb" << endl;
    SinkInput *p = reinterpret_cast<SinkInput *>(userdata);
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
