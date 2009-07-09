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
#include <QVector>

#include <iostream>

#include "QtPulseAudioSource.h"
#include "QtPulseAudioSourceManager.h"
#include "QtPulseAudioContext.h"

#include "QtPulseAudioSource_p.h"

using namespace std;

namespace QtPulseAudio {

Source::Source(int index, SourceManager *parent)
	: Stream(parent)
{
	d = new Private;
	d->that = this;
	d->mIsValid = false;
	d->mIndex = index;
}

Source::~Source()
{
	delete d;
}

bool Source::isValid() {
	return d->mIsValid;
}

QString Source::name() {
	return d->name;
}

uint32_t Source::index() {
	return d->mIndex;
}

QString Source::description() {
	return d->description;
}

pa_sample_spec Source::sampleSpec() {
	return d->sampleSpec;
}

pa_channel_map Source::channelMap() {
	return d->channelMap;
}

uint32_t Source::owner() {
	return d->ownerModule;
}

pa_cvolume Source::volume() {
	return d->volume;
}

int Source::mute() {
	return d->mute;
}

uint32_t Source::monitorSink() {
	return d->monitorOfSink;
}

QString Source::monitorSinkName() {
	return d->monitorOfSinkName;
}

pa_usec_t Source::latency() {
	return d->latency;
}

QString Source::driver() {
	return d->driver;
}

pa_source_flags_t Source::flags() {
	return d->flags;
}

void Source::update() {
	pa_operation *o;
	o = pa_context_get_source_info_by_index(d->mContext->cObject(), d->mIndex, Source::Private::source_cb, this->d);
	if ( o == NULL ) return;
	pa_operation_unref(o);
}

void Source::setVolume(pa_cvolume v) {
    pa_operation *o;
    this->d->svolume = v;
    o = pa_context_set_source_volume_by_index(d->mContext->cObject(), d->mIndex, &this->d->svolume, Source::Private::volume_cb, this->d);
    if ( o == NULL ) return;
    pa_operation_unref(o);
}


void Source::Private::source_cb(pa_context *, const pa_source_info *i, int eol, void *userdata) {
	cout << "Source::Private::source_cb" << endl;
    Source::Private *p = static_cast<Source::Private *>(userdata);

	if (eol) { cout << "eol" << endl; return; }

	if (!i) {
		cout << "Source callback failure" << endl;
		return;
	}

	if ( p->mIsValid ) assert ( i->index == p->mIndex );

	//p->mSourceInfo = *i;
    p->name = QString(i->name);
    p->description = QString(i->description);
    p->sampleSpec = i->sample_spec;
    p->channelMap = i->channel_map;
    p->ownerModule = i->owner_module;
    p->volume = i->volume;
    p->mute = i->mute;
    p->monitorOfSink = i->monitor_of_sink;
    p->monitorOfSinkName = QString(i->monitor_of_sink_name);
    p->latency = i->latency;
    p->driver = QString(i->driver);
    p->flags = i->flags;
	p->mIsValid = true;
	emit p->that->updated();
}


void Source::Private::volume_cb(pa_context *, int success, void *userdata) {
    cout << "Source::Private::volume_cb" << endl;
    Source::Private *p = static_cast<Source::Private *>(userdata);

    if (!success) {
        cout << "Volume change failure" << endl;
        return;
    }
    emit p->that->updated();
}

}
