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
#ifndef __QtPulseAudioSinkManager_h__
#define __QtPulseAudioSinkManager_h__

#include <QObject>

#include <pulse/pulseaudio.h>

#include "streammanager.h"

namespace QtPulseAudio {

class Context;
class Sink;

class SinkManager : public StreamManager {
	Q_OBJECT
public:
	virtual Stream *stream(int index);
	virtual Sink *sink(int index);

public slots:
	virtual void update();

protected:
	friend class Context;
	SinkManager(Context *parent, bool autoUpdate = true);
	~SinkManager();

	class Private;
	friend class Private;
	Private *d;
};

}

#endif
