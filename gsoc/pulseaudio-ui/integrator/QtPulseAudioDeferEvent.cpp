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
#include "QtPulseAudioDeferEvent_p.h"

using namespace QtPulseAudio;

DeferEvent::DeferEvent(pa_mainloop_api *a, pa_defer_event_cb_t cb, void *userdata,  QObject *parent)
	: QObject(parent)
{
	mApi = a;

	mEventCB = cb;
	mDestroyCB = NULL;
	mUserdata = userdata;

	mTimer = new QTimer(this);
	mTimer->setSingleShot(true);
	connect(mTimer, SIGNAL(timeout()), this, SLOT(onExec()));
	mTimer->start();
}


DeferEvent::~DeferEvent() {
	if ( mDestroyCB != NULL ) {
		pa_defer_event *e = reinterpret_cast<pa_defer_event *>(this);
		mDestroyCB(mApi, e, mUserdata);
	}
}

void DeferEvent::enable(int b) {
	if (b && !mTimer->isActive()) mTimer->start();
	else if ( !b && mTimer->isActive()) mTimer->stop();
}

void DeferEvent::setDestroy(pa_defer_event_destroy_cb_t cb) {
	mDestroyCB = cb;
}

void DeferEvent::deleteLater() {
	mTimer->stop();
	QObject::deleteLater();
}

void DeferEvent::onExec() {
	pa_defer_event *e = reinterpret_cast<pa_defer_event *>(this);
	mEventCB(mApi, e, mUserdata);
}
