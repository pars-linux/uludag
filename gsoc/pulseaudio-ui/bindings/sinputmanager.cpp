
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

#include "sinputmanager.h"
#include "stream.h"
#include "device.h"
#include "sinput.h"

#include "context.h"

#include "streammanager_p.h"
#include "streammanager.h"
#include "sinput_p.h"

using namespace std;

namespace QtPulseAudio {

SinkInputManager::SinkInputManager(Context *parent, bool autoUpdate)
	: StreamManager(parent, autoUpdate)
{
}

SinkInputManager::~SinkInputManager()
{
}

void SinkInputManager::update()
{
    cout << "StreamManager::update" << endl;
    pa_operation *o;

    if (!(o = pa_context_get_sink_input_info_list(d->context->cObject(), SinkInputManager::sink_input_cb, this))) {
	cout << "pa_context_get_sink_input_info_list() failed" << endl;
	return;
    }
    pa_operation_unref(o);
}

void SinkInputManager::sink_input_cb(pa_context *, const pa_sink_input_info *i, int eol, void *userdata) {
    cout << "SinkInputManager::Private::sinkInput_cb(" << i << ", " << eol << ")" << endl;
    
    if (eol) return;

    if (!i) {
	cout << "SinkInput callback failure" << endl;
	return;
    }
    
    int index = i->index;
    SinkInputManager *sm = reinterpret_cast<SinkInputManager *>(userdata);
    
    bool fresh = false;
    if (sm->stream(index) == NULL)
    {
	sm->add(sm->create(index));
	fresh = true;
    }
    
    SinkInputManager::sink_input_cb(sm->d->context->cObject(), i, eol, static_cast<SinkInput *>(sm->stream(index)));
    if(fresh)
	emit sm->added(index);
    else
	emit sm->changed(index);
}


Stream *SinkInputManager::create(int index)
{
    return new SinkInput(index, this, d->context);
}


}
