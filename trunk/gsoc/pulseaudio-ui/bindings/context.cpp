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
#include "assert.h"

#include <iostream>

#include <pulse/pulseaudio.h>

#include "../integrator/QtPulseAudioIntegrator.h"

#include "context.h"
#include "context_p.h"
#include "streammanager.h"
#include "sinkmanager.h"
#include "sourcemanager.h"
#include "streammanager_p.h"

using namespace std;
using namespace QtPulseAudio;

Context::Context(Integrator *parent, const char *name)
	:QObject(parent)
{
	d = new Private;
	///@todo check for null return
	d->mContext = pa_context_new(parent->api(), name);
	d->mSinks = new SinkManager(this);
	d->mSources = new SourceManager(this);
	pa_context_set_state_callback(d->mContext, Context::Private::state_callback, this);
}


Context::~Context()
{
	pa_context_unref(d->mContext);
	delete d;
}

int Context::connectToPulse(const char *server, pa_context_flags_t flags, const pa_spawn_api *api) {
	return pa_context_connect(d->mContext, server, flags, api);
}

pa_operation *Context::subscribe (pa_subscription_mask_t mask) {
	cout << "Context::subscribe" << endl;
	pa_context_set_subscribe_callback(d->mContext, Context::Private::subscribe_cb, this);

	pa_operation *o;
	o = pa_context_subscribe(d->mContext, mask, NULL, NULL);

	return o;
}

SinkManager *Context::sinks() {
	return d->mSinks;
}

SourceManager *Context::sources() {
	return d->mSources;
}


pa_context *Context::cObject() {
	return d->mContext;
}

void Context::Private::state_callback(pa_context *c, void *userdata) {
	assert(c != NULL);
	assert(userdata != NULL);

	Context *qc = static_cast<Context *>(userdata);

	switch (pa_context_get_state(c)) {
		case PA_CONTEXT_UNCONNECTED:
			qc->unconnected();
			break;
		case PA_CONTEXT_CONNECTING:
			qc->connecting();
			break;
		case PA_CONTEXT_AUTHORIZING:
			qc->authorizing();
			break;
		case PA_CONTEXT_SETTING_NAME:
			qc->settingName();
			break;
		case PA_CONTEXT_READY:
            cout << "Ready" << endl;
			qc->ready();
			break;
		case PA_CONTEXT_FAILED:
            cout << "Failed" << endl;
			qc->failed();
			break;
		case PA_CONTEXT_TERMINATED:
            cout << "Terminated" << endl;
			qc->terminated();
			break;
		default:
			qc->unknown();
			break;
	}
}

void Context::Private::subscribe_cb(pa_context *c, pa_subscription_event_type_t t, uint32_t index, void *userdata) {
	cout << "Context::Private::subscribe_cb" << endl;
	Context *qc = static_cast<Context *>(userdata);
	int facility = t & PA_SUBSCRIPTION_EVENT_FACILITY_MASK;
	int type = t & PA_SUBSCRIPTION_EVENT_TYPE_MASK;

	switch (facility) {
		case PA_SUBSCRIPTION_EVENT_SINK:
			qc->d->mSinks->event(type, index);
			break;
		case PA_SUBSCRIPTION_EVENT_SOURCE:
			qc->d->mSources->event(type, index);
			break;
		case PA_SUBSCRIPTION_EVENT_SINK_INPUT:
			//qc->d->mSinkInput->d->streamEvent(type, index);
			break;
	}
}
