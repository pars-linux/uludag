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
#include <pulse/timeval.h>

#include "QtPulseAudioTimeEvent_p.h"

using namespace QtPulseAudio;

TimeEvent::TimeEvent(pa_mainloop_api *a, const struct timeval *tv, pa_time_event_cb_t cb, void *userdata,  QObject *parent)
	: QObject(parent)
{
	mApi = a;

	mTimerCB = cb;
	mDestroyCB = NULL;
	mUserdata = userdata;
	mTimer = new QTimer(this);
	mTimer->setSingleShot(true);
	connect(mTimer, SIGNAL(timeout()), this, SLOT(onTimer()));

	restart(tv);
}


TimeEvent::~TimeEvent()
{
	if ( mDestroyCB != NULL ) {
		pa_time_event *e = reinterpret_cast<pa_time_event *>(this);
		mDestroyCB(mApi, e, mUserdata);
	}
}

void TimeEvent::restart(const struct timeval *tv) {
	mTimer->stop();

	if ( tv != NULL ) {
		mTv = *tv;
		pa_usec_t delay = pa_timeval_age(tv);
		mTimer->start(delay / 1000);
	}
}

void TimeEvent::setDestroy(pa_time_event_destroy_cb_t cb) {
	mDestroyCB = cb;
}

void TimeEvent::deleteLater() {
	mTimer->stop();
	QObject::deleteLater();
}

void TimeEvent::onTimer() {
	pa_time_event *e = reinterpret_cast<pa_time_event *>(this);
	mTimerCB(mApi, e, &mTv, mUserdata);
}
