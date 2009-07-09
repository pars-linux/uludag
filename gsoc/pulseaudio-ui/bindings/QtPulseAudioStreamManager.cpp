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

#include "QtPulseAudioStream.h"
#include "QtPulseAudioStreamManager.h"
#include "QtPulseAudioContext.h"

#include "QtPulseAudioStreamManager_p.h"
#include "QtPulseAudioStream_p.h"

using namespace std;

namespace QtPulseAudio {

StreamManager::StreamManager(Context *parent)
	: QObject(parent)
{
}

StreamManager::~StreamManager()
{
}

#if 0
void StreamManager::update() {
	cout << "StreamManager::update" << endl;
	pa_operation *o;

	if (!(o = pa_context_get_sink_info_list(d->mContext->cObject(), StreamManager::Private::sink_cb, this))) {
		cout << "pa_context_get_sink_info_list() failed" << endl;
		return;
	}
	pa_operation_unref(o);
}

void StreamManager::Private::streamEvent(int type, uint32_t index) {
	cout << "StreamManager::Private::streamEvent(" << type << ", " << index << ")" << endl;
	if (type == PA_SUBSCRIPTION_EVENT_REMOVE) {
		that->removed(index);
	} else if (type == PA_SUBSCRIPTION_EVENT_CHANGE) {
		that->changed(index);
		if (mAutoUpdate) mStreams[index]->update();
	} else if (type == PA_SUBSCRIPTION_EVENT_NEW) {
		mStreams[index] = new Stream(that);
		mStreams[index]->d->mContext = mContext;
		that->added(index);
	} else {
		that->unknow(index);
	}
}

void StreamManager::Private::sink_cb(pa_context *, const pa_sink_info *i, int eol, void *userdata) {
	cout << "StreamManager::Private::sink_cb(" << i << ", " << eol << ")" << endl;

	if (eol) return;

	if (!i) {
		cout << "Sink callback failure" << endl;
		return;
	}

	int index = i->index;
	StreamManager *sm = static_cast<StreamManager *>(userdata);

	if ( sm->d->mStreams[index] == NULL ) {
		sm->d->mStreams[index] = new Stream(sm);
		sm->d->mStreams[index]->d->mContext = sm->d->mContext;
		emit sm->added(index);
	}

	sm->d->mStreams[index]->d->sink_cb(sm->d->mContext->cObject(), i, eol, sm->d->mStreams[index]->d);
}
#endif
}
