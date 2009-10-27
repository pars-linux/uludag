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
#ifndef __QtPulseAudioContext_h__
#define __QtPulseAudioContext_h__

#include <QObject>

#include <pulse/pulseaudio.h>

/**
 * @todo Add support for implicit sharing througth pa_context_ref and pa_context_unref
 */
namespace QtPulseAudio
{

class Integrator;
class SinkManager;
class SourceManager;
class SinkInputManager;

class Context : public QObject {
	Q_OBJECT

public:
	Context(Integrator *parent, const char *name);
	~Context();

	int connectToPulse(const char *server, pa_context_flags_t flags, const pa_spawn_api *api);

	pa_operation *subscribe (pa_subscription_mask_t mask);

	SinkManager *sinks();
	SourceManager *sources();
	SinkInputManager *sinkInputs();

	pa_context *cObject();

signals:
	void unconnected();
	void connecting();
	void authorizing();
	void settingName();
	void ready();
	void failed();
	void terminated();
	void unknown();

private:
	class Private;
	friend class Private;

	Private *d;
};

}

#endif
