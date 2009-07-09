/*
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
#include <assert.h>

#include <iostream>

#include <pulse/mainloop-api.h>

#include "QtPulseAudioIntegrator.h"

#include "QtPulseAudioIOEvent_p.h"
#include "QtPulseAudioTimeEvent_p.h"
#include "QtPulseAudioDeferEvent_p.h"

namespace QtPulseAudio
{

class PAIPrivate
{
public:
	static const pa_mainloop_api vtable;

	static pa_io_event *io_new (pa_mainloop_api *a, int fd, pa_io_event_flags_t events, pa_io_event_cb_t cb, void *userdata);
	static void io_free (pa_io_event *e);
	static void io_enable (pa_io_event *e, pa_io_event_flags_t f);
	static void io_set_destroy (pa_io_event *e, pa_io_event_destroy_cb_t cb);

	static pa_time_event *time_new (pa_mainloop_api *a, const struct timeval *tv, pa_time_event_cb_t cb, void *userdata);
	static void time_restart (pa_time_event *e, const struct timeval *tv);
	static void time_free (pa_time_event *e);
	static void time_set_destroy (pa_time_event *e, pa_time_event_destroy_cb_t cb);

	static pa_defer_event *defer_new (pa_mainloop_api *a, pa_defer_event_cb_t cb, void *userdata);
	static void defer_enable (pa_defer_event *e, int b);
	static void defer_free (pa_defer_event *e);
	static void defer_set_destroy (pa_defer_event *e, pa_defer_event_destroy_cb_t cb);

	static void quit(pa_mainloop_api *a, int retval);
};

}

using namespace std;
using namespace QtPulseAudio;

Integrator::Integrator(QObject *parent)
	: QObject(parent)
{
	mApi = new pa_mainloop_api;
	*mApi = PAIPrivate::vtable;
	mApi->userdata = this;
}


Integrator::~Integrator()
{
	delete mApi;
}

pa_io_event *PAIPrivate::io_new (pa_mainloop_api *a, int fd, pa_io_event_flags_t events, pa_io_event_cb_t cb, void *userdata) {
	Q_ASSERT(a != NULL);
	Q_ASSERT(a->userdata != NULL);
	Q_ASSERT(fd >= 0);
	Q_ASSERT(cb != NULL);

	Integrator *pai = static_cast<Integrator *>(a->userdata);
	pa_io_event *io_event = reinterpret_cast<pa_io_event *>(new IOEvent(a, fd, events, cb, userdata, pai));

	return io_event;
}

void PAIPrivate::io_free (pa_io_event *e) {
	Q_ASSERT(e != NULL);

	IOEvent *qe = reinterpret_cast<IOEvent *> (e);
	qe->deleteLater();
}

void PAIPrivate::io_enable (pa_io_event *e, pa_io_event_flags_t f) {
	Q_ASSERT(e != NULL);
	
	IOEvent *qe = reinterpret_cast<IOEvent *> (e);
	qe->enable(f);
}

void PAIPrivate::io_set_destroy (pa_io_event *e, pa_io_event_destroy_cb_t cb) {
	Q_ASSERT(e != NULL);
	
	IOEvent *qe = reinterpret_cast<IOEvent *> (e);
	qe->setDestroy(cb);
}

pa_time_event *PAIPrivate::time_new (pa_mainloop_api *a, const struct timeval *tv, pa_time_event_cb_t cb, void *userdata) {
	Q_ASSERT(a != NULL);
	Q_ASSERT(a->userdata != NULL);
	Q_ASSERT(cb != NULL);

	Integrator *pai = static_cast<Integrator *>(a->userdata);
	
	return reinterpret_cast<pa_time_event *>(new TimeEvent(a, tv, cb, userdata, pai));
}

void PAIPrivate::time_restart (pa_time_event *e, const struct timeval *tv) {
	Q_ASSERT(e != NULL);

	TimeEvent *qe = reinterpret_cast<TimeEvent *>(e);
	qe->restart(tv);
}

void PAIPrivate::time_free (pa_time_event *e) {
	Q_ASSERT(e != NULL);
	
	TimeEvent *qe = reinterpret_cast<TimeEvent *>(e);
	qe->deleteLater();
}

void PAIPrivate::time_set_destroy (pa_time_event *e, pa_time_event_destroy_cb_t cb) {
	Q_ASSERT(e != NULL);
	
	TimeEvent *qe = reinterpret_cast<TimeEvent *>(e);
	qe->setDestroy(cb);
}

pa_defer_event *PAIPrivate::defer_new (pa_mainloop_api *a, pa_defer_event_cb_t cb, void *userdata) {
	Q_ASSERT(a != NULL);
	Q_ASSERT(a->userdata != NULL);
	Q_ASSERT(cb != NULL);

	Integrator *pai = static_cast<Integrator *>(a->userdata);

	return reinterpret_cast<pa_defer_event *>(new DeferEvent(a, cb, userdata, pai));
}

void PAIPrivate::defer_enable (pa_defer_event *e, int b) {
	Q_ASSERT(e != NULL);
	
	DeferEvent *qe = reinterpret_cast<DeferEvent *>(e);
	qe->enable(b);
}

void PAIPrivate::defer_free (pa_defer_event *e) {
	Q_ASSERT(e != NULL);
	
	DeferEvent *qe = reinterpret_cast<DeferEvent *>(e);
	qe->deleteLater();
}

void PAIPrivate::defer_set_destroy (pa_defer_event *e, pa_defer_event_destroy_cb_t cb) {
	Q_ASSERT(e != NULL);
	
	DeferEvent *qe = reinterpret_cast<DeferEvent *>(e);
	qe->setDestroy(cb);
}

void PAIPrivate::quit(pa_mainloop_api *a, int retval) {
	Q_ASSERT(a->userdata != NULL);
	
	Integrator *pai = static_cast<Integrator *>(a->userdata);
	emit pai->quit(retval);
}

const pa_mainloop_api PAIPrivate::vtable = {
    NULL,

    PAIPrivate::io_new,
    PAIPrivate::io_enable,
    PAIPrivate::io_free,
    PAIPrivate::io_set_destroy,

    PAIPrivate::time_new,
    PAIPrivate::time_restart,
    PAIPrivate::time_free,
    PAIPrivate::time_set_destroy,

    PAIPrivate::defer_new,
    PAIPrivate::defer_enable,
    PAIPrivate::defer_free,
    PAIPrivate::defer_set_destroy,

    PAIPrivate::quit,
};
