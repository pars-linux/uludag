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
#ifndef __QtPulseAudioSinkManager_p_h__
#define __QtPulseAudioSinkManager_p_h__

#include <QHash>
#include <QPointer>

#include "sinkmanager.h"

#include <pulse/pulseaudio.h>

namespace QtPulseAudio {

class Sink;

class SinkManager::Private {
public:
	static void sink_cb(pa_context *, const pa_sink_info *i, int eol, void *userdata);

	Private();

	void sinkEvent(int type, uint32_t index);

	SinkManager *that;
	Context *mContext;
	bool mAutoUpdate;
	QHash<int, Sink *> mSinks;
};

}

#endif
