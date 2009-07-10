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
#ifndef __QtPulseAudioSink_p_h__
#define __QtPulseAudioSink_p_h__

#include <QVector>
#include <QPointer>

#include "sink.h"

namespace QtPulseAudio {

class Sink::Private {
public:
	static void sink_cb(pa_context *, const pa_sink_info *i, int eol, void *userdata);
    static void volume_cb(pa_context *, int success, void *userdata);

	void triggerUpdateInfo();
	void updateInfo(const pa_sink_info &info);

	Sink *that;
	Context *mContext;
	uint32_t mIndex;
	bool mIsValid;
    
    QString name;
    QString description;
    pa_sample_spec sampleSpec;
    pa_channel_map channelMap;
    uint32_t ownerModule;
    pa_cvolume volume;
    pa_cvolume svolume;
    int mute;
    uint32_t monitorSource;
    QString monitorSourceName;
    pa_usec_t latency;
    QString driver;
    pa_sink_flags_t flags;
    pa_operation *volumeOperation;
};

}

#endif
