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
#include "QtPulseAudioIOEvent_p.h"

using namespace QtPulseAudio;

IOEvent::IOEvent (pa_mainloop_api *a, int fd, pa_io_event_flags_t f, pa_io_event_cb_t cb, void *userdata, QObject *parent)
	: QObject(parent)
{
	mApi = a;

	mNotifier[0] = mNotifier[1] = mNotifier[2] = NULL;

	mFD = fd;
	mEventCB = cb;
	mDestroyCB = NULL;
	mUserdata = userdata;

	mNotifier[0] = new QSocketNotifier(mFD, QSocketNotifier::Read, this);
	connect(mNotifier[0], SIGNAL(activated(int)), this, SLOT(onRead()));
	mNotifier[0]->setEnabled(false);

	mNotifier[1] = new QSocketNotifier(mFD, QSocketNotifier::Write, this);
	connect(mNotifier[1], SIGNAL(activated(int)), this, SLOT(onWrite()));
	mNotifier[1]->setEnabled(false);

	mNotifier[2] = new QSocketNotifier(mFD, QSocketNotifier::Exception, this);
	connect(mNotifier[2], SIGNAL(activated(int)), this, SLOT(onException()));
	mNotifier[2]->setEnabled(false);

	enable(f);
}

IOEvent::~IOEvent() {
	if ( mDestroyCB != NULL ) {
		mDestroyCB(mApi, reinterpret_cast<pa_io_event *>(this), mUserdata);
	}
}

void IOEvent::enable(pa_io_event_flags_t f) {
	if ( (f & PA_IO_EVENT_INPUT) ) {
		mNotifier[0]->setEnabled(true);
	} else {
		mNotifier[0]->setEnabled(false);
	}

	if ( (f & PA_IO_EVENT_OUTPUT)  ) {
		mNotifier[1]->setEnabled(true);
	} else {
		mNotifier[1]->setEnabled(false);
	}

	if ( ((f & PA_IO_EVENT_ERROR) || (f & PA_IO_EVENT_HANGUP)) ) {
		mNotifier[2]->setEnabled(true);
	} else {
		mNotifier[2]->setEnabled(false);
	}
}

void IOEvent::setDestroy(pa_io_event_destroy_cb_t cb) {
	mDestroyCB = cb;
}

void IOEvent::deleteLater() {
	mEventCB = NULL;
}

void IOEvent::onRead () {
	pa_io_event *e = reinterpret_cast<pa_io_event *>(this);
	mEventCB(mApi, e, mNotifier[0]->socket(), PA_IO_EVENT_INPUT, mUserdata);
}

void IOEvent::onWrite () {
	pa_io_event *e = reinterpret_cast<pa_io_event *>(this);
	mEventCB(mApi, e, mNotifier[1]->socket(), PA_IO_EVENT_OUTPUT, mUserdata);
}

void IOEvent::onException () {
	pa_io_event *e = reinterpret_cast<pa_io_event *>(this);
	
	if ( mEventCB != NULL)
		mEventCB(mApi, e, mNotifier[2]->socket(), PA_IO_EVENT_HANGUP, mUserdata);
		
	if ( mEventCB != NULL)
		mEventCB(mApi, e, mNotifier[2]->socket(), PA_IO_EVENT_ERROR, mUserdata);
}
