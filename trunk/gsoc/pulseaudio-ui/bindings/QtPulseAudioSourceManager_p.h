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
#ifndef __QtPulseAudioSourceManager_p_h__
#define __QtPulseAudioSourceManager_p_h__

#include <QHash>
#include <QPointer>

#include "QtPulseAudioSourceManager.h"

#include <pulse/pulseaudio.h>

namespace QtPulseAudio {

class Source;

class SourceManager::Private {
public:
	static void source_cb(pa_context *, const pa_source_info *i, int eol, void *userdata);

	Private();

	void sourceEvent(int type, uint32_t index);

	SourceManager *that;
	Context *mContext;
	bool mAutoUpdate;
	QHash<int, Source *> mSources;
};

}

#endif
