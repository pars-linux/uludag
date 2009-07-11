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
#ifndef __QtPulseAudioStream_h__
#define __QtPulseAudioStream_h__

#include <QObject>

#include <pulse/pulseaudio.h>

namespace QtPulseAudio {

class StreamManager;

class Stream : public QObject {
	Q_OBJECT
public:
	virtual bool isValid() = 0;

	virtual QString name() = 0;
	virtual uint32_t index() = 0;
	virtual QString description() = 0;
	virtual pa_sample_spec sampleSpec() = 0;
	virtual pa_channel_map channelMap() = 0;
	virtual uint32_t owner() = 0;
	virtual pa_cvolume volume() = 0;
	virtual int muted() = 0;
	//virtual uint32_t monitorSource();
	//virtual const char *monitorSourceName();
	virtual pa_usec_t latency() = 0;
	virtual QString driver() = 0;
	//pa_sink_flags_t flags();

signals:
	/**
	 * Signal send when the server send an update on the stream status, either because,
	 * it is was asked by the user, or because it was subscribe.
	 */
	void updated();

public slots:
	virtual void update() = 0;
    virtual void setVolume(pa_cvolume) = 0;
	
protected:
	friend class StreamManager;
	Stream(StreamManager *parent = NULL);
	~Stream();

	class Private;
	friend class Private;
	Private *d;
};

}

#endif
