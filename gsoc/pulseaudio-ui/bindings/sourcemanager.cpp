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
#include "source.h"
#include "sourcemanager.h"
#include "context.h"

#include "streammanager_p.h"
#include "source_p.h"

using namespace std;

namespace QtPulseAudio {

SourceManager::SourceManager(Context *parent, bool autoUpdate)
	: StreamManager(parent, autoUpdate)
{
}

SourceManager::~SourceManager()
{
}

void SourceManager::update()
{
    cout << "StreamManager::update" << endl;
    pa_operation *o;

    if (!(o = pa_context_get_source_info_list(d->context->cObject(), SourceManager::source_cb, this))) {
	cout << "pa_context_get_source_info_list() failed" << endl;
	return;
    }
    pa_operation_unref(o);
}


void SourceManager::source_cb(pa_context *, const pa_source_info *i, int eol, void *userdata) {
    cout << "SourceManager::Private::source_cb(" << i << ", " << eol << ")" << endl;
    
    if (eol) return;

    if (!i) {
	cout << "Source callback failure" << endl;
	return;
    }
    
    int index = i->index;
    SourceManager *sm = reinterpret_cast<SourceManager *>(userdata);
    
    bool fresh = false;
    if (sm->stream(index) == NULL)
    {
	sm->add(sm->create(index));
	fresh = true;
    }
    
    Source::source_cb(sm->d->context->cObject(), i, eol, static_cast<Source *>(sm->stream(index)));
    if(fresh)
	emit sm->added(index);
    else
	emit sm->changed(index);
}


Stream *SourceManager::create(int index)
{
    return new Source(index, this, d->context);
}


}
