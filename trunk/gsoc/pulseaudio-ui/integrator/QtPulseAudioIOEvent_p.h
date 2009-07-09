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
#ifndef __QtPulseAudioIOEvent_h__
#define __QtPulseAudioIOEvent_h__

#include <QObject>
#include <QSocketNotifier>

#include <pulse/mainloop-api.h>

namespace QtPulseAudio
{

class IOEvent : public QObject
{
Q_OBJECT

public:
	IOEvent (pa_mainloop_api *a, int fd, pa_io_event_flags_t events, pa_io_event_cb_t cb, void *userdata, QObject *parent = NULL);
	~IOEvent();

	void enable(pa_io_event_flags_t f);
	void setDestroy(pa_io_event_destroy_cb_t cb);
	
	void deleteLater();

private slots:
	void onRead();
	void onWrite();
	void onException();

private:
	pa_mainloop_api *mApi;
	QSocketNotifier *mNotifier[3];
	int mFD;
	pa_io_event_cb_t mEventCB;
	pa_io_event_destroy_cb_t mDestroyCB;
	void *mUserdata;
};

}

#endif
