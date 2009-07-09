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
#ifndef __QtPulseAudioContext_p_h__
#define __QtPulseAudioContext_p_h__

#include "QtPulseAudioContext.h"

namespace QtPulseAudio
{

class Context::Private
{
public:
	static void state_callback(pa_context *c, void *userdata);
	static void subscribe_cb(pa_context *c, pa_subscription_event_type_t t, uint32_t index, void *userdata);

	pa_context *mContext;
	SinkManager *mSinks;
	SourceManager *mSources;
};

}

#endif
