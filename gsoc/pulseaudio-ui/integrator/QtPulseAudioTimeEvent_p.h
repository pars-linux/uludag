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
#ifndef __QtPulseAudioTimeEvent_h__
#define __QtPulseAudioTimeEvent_h__

#include <iostream>

#include <QObject>
#include <QTimer>

#include <pulse/mainloop-api.h>

using namespace std;

namespace QtPulseAudio {

class TimeEvent : public QObject {
Q_OBJECT
public:
	TimeEvent(pa_mainloop_api *a, const struct timeval *tv, pa_time_event_cb_t cb, void *userdata,  QObject *parent = NULL);
	~TimeEvent();

	void restart(const struct timeval *tv);
	void setDestroy(pa_time_event_destroy_cb_t cb);

	void deleteLater();

private slots:
	void onTimer();

private:
	pa_mainloop_api *mApi;
	pa_time_event_cb_t mTimerCB;
	pa_time_event_destroy_cb_t mDestroyCB;
	void *mUserdata;
	struct timeval mTv;
	QTimer *mTimer;
};

}

#endif
