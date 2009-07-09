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

#include "QtPulseAudioSourceManager_p.h"
#include "QtPulseAudioSource_p.h"

using namespace std;

namespace QtPulseAudio {

SourceManager::SourceManager(Context *parent, bool autoUpdate)
	: StreamManager(parent)
{
	d = new Private;
	d->that = this;
	d->mContext = parent;
	d->mAutoUpdate = autoUpdate;
}

SourceManager::Private::Private()
{
}

SourceManager::~SourceManager()
{
	delete d;
}

Stream *SourceManager::stream(int index) {
	return static_cast<Source *>(d->mSources[index]);
}

Source *SourceManager::sink(int index) {
	return d->mSources[index];
}

void SourceManager::update() {
	cout << "SourceManager::update" << endl;
	pa_operation *o;

	if (!(o = pa_context_get_source_info_list(d->mContext->cObject(), SourceManager::Private::source_cb, this))) {
		cout << "pa_context_get_source_info_list() failed" << endl;
		return;
	}
	pa_operation_unref(o);
}

void SourceManager::Private::sourceEvent(int type, uint32_t index) {
	cout << "SourceManager::Private::sourceEvent(" << type << ", " << index << ")" << endl;
	if (type == PA_SUBSCRIPTION_EVENT_REMOVE) {
		emit that->removed(index);
	} else if (type == PA_SUBSCRIPTION_EVENT_CHANGE || type==PA_SUBSCRIPTION_EVENT_NEW) {
		if(mSources[index] == 0)
		{
		    mSources[index] = new Source(index, that);
		    mSources[index]->d->mContext = mContext;
		    emit that->added(index);
		}
		else
		    emit that->changed(index);
	}
}

void SourceManager::Private::source_cb(pa_context *, const pa_source_info *i, int eol, void *userdata) {
	cout << "SourceManager::Private::source_cb(" << i << ", " << eol << ")" << endl;

	if (eol) return;

	if (!i) {
		cout << "Source callback failure" << endl;
		return;
	}

	int index = i->index;
	SourceManager *sm = static_cast<SourceManager *>(userdata);

	if ( !sm->d->mSources.contains(index) ) {
		sm->d->mSources[index] = new Source(index, sm);
		sm->d->mSources[index]->d->mContext = sm->d->mContext;
		emit sm->added(index);
	}

	sm->d->mSources[index]->d->source_cb(sm->d->mContext->cObject(), i, eol, sm->d->mSources[index]->d);
}

}
