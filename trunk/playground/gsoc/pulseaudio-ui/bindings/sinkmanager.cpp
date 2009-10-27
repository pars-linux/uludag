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
#include <QVector>

#include <iostream>

#include "stream.h"
#include "device.h"
#include "sink.h"
#include "sinkmanager.h"
#include "context.h"

#include "streammanager_p.h"
#include "sink_p.h"

using namespace std;

namespace QtPulseAudio {

SinkManager::SinkManager(Context *parent, bool autoUpdate)
	: StreamManager(parent, autoUpdate)
{
}

SinkManager::~SinkManager()
{
}

void SinkManager::update()
{
    cout << "StreamManager::update" << endl;
    pa_operation *o;

    if (!(o = pa_context_get_sink_info_list(d->context->cObject(), SinkManager::sink_cb, this))) {
	cout << "pa_context_get_sink_info_list() failed" << endl;
	return;
    }
    pa_operation_unref(o);
}


void SinkManager::sink_cb(pa_context *, const pa_sink_info *i, int eol, void *userdata) {
    cout << "SinkManager::Private::sink_cb(" << i << ", " << eol << ")" << endl;
    
    if (eol) return;

    if (!i) {
	cout << "Sink callback failure" << endl;
	return;
    }
    
    int index = i->index;
    SinkManager *sm = reinterpret_cast<SinkManager *>(userdata);
    
    bool fresh = false;
    if (sm->stream(index) == NULL)
    {
	sm->add(sm->create(index));
	fresh = true;
    }
    
    Sink::sink_cb(sm->d->context->cObject(), i, eol, static_cast<Sink *>(sm->stream(index)));
    if(fresh)
	emit sm->added(index);
    else
	emit sm->changed(index);
}


Stream *SinkManager::create(int index)
{
    return new Sink(index, this, d->context);
}


}
