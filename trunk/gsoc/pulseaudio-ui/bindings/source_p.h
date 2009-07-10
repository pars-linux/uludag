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
#ifndef __QtPulseAudioSource_p_h__
#define __QtPulseAudioSource_p_h__

#include <QVector>
#include <QPointer>

#include "source.h"

namespace QtPulseAudio {

class Source::Private {
public:
	static void source_cb(pa_context *, const pa_source_info *i, int eol, void *userdata);
    static void volume_cb(pa_context *, int success, void *userdata);

	void triggerUpdateInfo();
	void updateInfo(const pa_source_info &info);

	Source *that;
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
    uint32_t monitorOfSink;
    QString monitorOfSinkName;
    pa_usec_t latency;
    QString driver;
    pa_source_flags_t flags;
};

}

#endif
