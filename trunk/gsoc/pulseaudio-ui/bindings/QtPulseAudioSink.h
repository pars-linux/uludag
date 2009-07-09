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
#ifndef __QtPulseAudioSink_h__
#define __QtPulseAudioSink_h__

#include <QObject>

#include <pulse/pulseaudio.h>

#include "QtPulseAudioStream.h"

namespace QtPulseAudio {

class SinkManager;

class Sink : public Stream {
	Q_OBJECT
public:
	bool isValid();

	QString name();
	uint32_t index();
	QString description();
	pa_sample_spec sampleSpec();
	pa_channel_map channelMap();
	uint32_t owner();
	pa_cvolume volume();
	int mute();
	uint32_t monitorSource();
	QString monitorSourceName();
	pa_usec_t latency();
	QString driver();
	pa_sink_flags_t flags();

signals:
	/**
	 * Signal send when the server send an update on the stream status, either because,
	 * it is was asked by the user, or because it was subscribe.
	 */
	void updated();

public slots:
	void update();
    void setVolume(pa_cvolume);
	
protected:
	friend class SinkManager;
	Sink(int index, SinkManager *parent = NULL);
	~Sink();

	class Private;
	friend class Private;
	Private *d;
};

}

#endif
