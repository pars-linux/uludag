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
#ifndef QTPULSEAUDIOINTEGRATOR_H
#define QTPULSEAUDIOINTEGRATOR_H

#include <QObject>

typedef struct pa_mainloop_api pa_mainloop_api;

namespace QtPulseAudio {

class Integrator: public QObject
{
Q_OBJECT

public:
	Integrator(QObject *parent = NULL);
	~Integrator();

	pa_mainloop_api *api() { return mApi; }

signals:
	void quit(int retval);

public:
	friend class PAIPrivate;

	pa_mainloop_api *mApi;
};

}

#endif
