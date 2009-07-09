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
#ifndef __QtPulseAudioDeferEvent_h__
#define __QtPulseAudioDeferEvent_h__

#include <QObject>
#include <QTimer>

#include <pulse/mainloop-api.h>

namespace QtPulseAudio
{

class DeferEvent : public QObject
{
Q_OBJECT

public:
	DeferEvent (pa_mainloop_api *a, pa_defer_event_cb_t cb, void *userdata,  QObject *parent = NULL);
	~DeferEvent ();

	void enable(int b);
	void setDestroy(pa_defer_event_destroy_cb_t cb);

	void deleteLater();

private slots:
	void onExec();

private:
	pa_mainloop_api *mApi;
	QTimer *mTimer;
	pa_defer_event_cb_t mEventCB;
	pa_defer_event_destroy_cb_t mDestroyCB;
	void *mUserdata;
};

}

#endif
