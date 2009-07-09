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

#include "QtPulseAudioSink.h"
#include "QtPulseAudioSinkManager.h"
#include "QtPulseAudioContext.h"

#include "QtPulseAudioSinkManager_p.h"
#include "QtPulseAudioSink_p.h"

using namespace std;

namespace QtPulseAudio {

SinkManager::SinkManager(Context *parent, bool autoUpdate)
	: StreamManager(parent)
{
	d = new Private;
	d->that = this;
	d->mContext = parent;
	d->mAutoUpdate = autoUpdate;
}

SinkManager::Private::Private()
{
}

SinkManager::~SinkManager()
{
	delete d;
}

Stream *SinkManager::stream(int index) {
	return static_cast<Stream *>(d->mSinks[index]);
}

Sink *SinkManager::sink(int index) {
	return d->mSinks[index];
}

void SinkManager::update() {
	cout << "StreamManager::update" << endl;
	pa_operation *o;

	if (!(o = pa_context_get_sink_info_list(d->mContext->cObject(), SinkManager::Private::sink_cb, this))) {
		cout << "pa_context_get_sink_info_list() failed" << endl;
		return;
	}
	pa_operation_unref(o);
}

void SinkManager::Private::sinkEvent(int type, uint32_t index) {
	cout << "StreamManager::Private::streamEvent(" << type << ", " << index << ")" << endl;
	if (type == PA_SUBSCRIPTION_EVENT_REMOVE) {
		that->removed(index);
	} else if (type == PA_SUBSCRIPTION_EVENT_CHANGE || type==PA_SUBSCRIPTION_EVENT_NEW) {
		if(mSinks[index] == 0)
		{
		    mSinks[index] = new Sink(index, that);
		    mSinks[index]->d->mContext = mContext;
		    emit that->added(index);
		}
		else
		    emit that->changed(index);
		that->changed(index);
		if (mAutoUpdate) mSinks[index]->update();
	}
}

void SinkManager::Private::sink_cb(pa_context *, const pa_sink_info *i, int eol, void *userdata) {
	cout << "StreamManager::Private::sink_cb(" << i << ", " << eol << ")" << endl;

	if (eol) return;

	if (!i) {
		cout << "Sink callback failure" << endl;
		return;
	}

	int index = i->index;
	SinkManager *sm = static_cast<SinkManager *>(userdata);

    bool fresh = false;
	if ( sm->d->mSinks[index] == NULL ) {
		sm->d->mSinks[index] = new Sink(index, sm);
		sm->d->mSinks[index]->d->mContext = sm->d->mContext;
        fresh = true;
	}

	sm->d->mSinks[index]->d->sink_cb(sm->d->mContext->cObject(), i, eol, sm->d->mSinks[index]->d);
    if(fresh)
        emit sm->added(index);
}

}
