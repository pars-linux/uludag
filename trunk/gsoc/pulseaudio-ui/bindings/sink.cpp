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
#include "sink_p.h"

using namespace std;

namespace QtPulseAudio {

Sink::Sink(int index, SinkManager *parent)
	: Stream(parent)
{
	d = new Private;
	d->that = this;
	d->mIsValid = false;
	d->mIndex = index;
	d->volumeOperation = 0;
}

Sink::~Sink()
{
	delete d;
}

bool Sink::isValid() {
	return d->mIsValid;
}

QString Sink::name() {
	return d->name;
}

uint32_t Sink::index() {
	return d->mIndex;
}

QString Sink::description() {
	return d->description;
}

pa_sample_spec Sink::sampleSpec() {
	return d->sampleSpec;
}

pa_channel_map Sink::channelMap() {
	return d->channelMap;
}

uint32_t Sink::owner() {
	return d->ownerModule;
}

pa_cvolume Sink::volume() {
	return d->volume;
}

int Sink::mute() {
	return d->mute;
}

uint32_t Sink::monitorSource() {
	return d->monitorSource;
}

QString Sink::monitorSourceName() {
	return d->monitorSourceName;
}

pa_usec_t Sink::latency() {
	return d->latency;
}

QString Sink::driver() {
	return d->driver;
}

pa_sink_flags_t Sink::flags() {
	return d->flags;
}

void Sink::update() {
	pa_operation *o;
	o = pa_context_get_sink_info_by_index(d->mContext->cObject(), d->mIndex, Sink::Private::sink_cb, this->d);
	if ( o == NULL ) return;
	pa_operation_unref(o);
}

void Sink::setVolume(pa_cvolume v) {
    pa_operation *o;
    this->d->svolume = v;
    if(this->d->volumeOperation != 0)
    {
	if(pa_operation_get_state(this->d->volumeOperation) == PA_OPERATION_RUNNING)
	    return;
	else
	    pa_operation_unref(this->d->volumeOperation);
    }
    d->volumeOperation = pa_context_set_sink_volume_by_index(d->mContext->cObject(),
			    d->mIndex, &this->d->svolume, Sink::Private::volume_cb, this->d);
}


void Sink::Private::sink_cb(pa_context *, const pa_sink_info *i, int eol, void *userdata) {
	cout << "Sink::Private::sink_cb" << endl;
    Sink::Private *p = static_cast<Sink::Private *>(userdata);

	if (eol) return;

	if (!i) {
		cout << "Sink callback failure" << endl;
		return;
	}

	if ( p->mIsValid ) assert ( i->index == p->mIndex );

	//p->mSinkInfo = *i;
    cout << i->name << " " << i->description << endl;
    p->name = QString(i->name);
    p->description = QString(i->description);
    p->sampleSpec = i->sample_spec;
    p->channelMap = i->channel_map;
    p->ownerModule = i->owner_module;
    p->volume = i->volume;
    p->mute = i->mute;
    p->monitorSource = i->monitor_source;
    p->monitorSourceName = QString(i->monitor_source_name);
    p->latency = i->latency;
    p->driver = QString(i->driver);
    p->flags = i->flags;
    
    
	p->mIsValid = true;
	emit p->that->updated();
}

void Sink::Private::volume_cb(pa_context *, int success, void *userdata) {
    cout << "Sink::Private::volume_cb" << endl;
    Sink::Private *p = static_cast<Sink::Private *>(userdata);
    if(p->volumeOperation != 0)
	pa_operation_unref(p->volumeOperation);
    p->volumeOperation = 0;

    if (!success) {
        cout << "Volume change failure" << endl;
        return;
    }
}

}
