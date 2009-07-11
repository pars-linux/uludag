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
#include <iostream>

#include "stream.h"
#include "streammanager.h"
#include "context.h"

#include "streammanager_p.h"

using namespace std;

namespace QtPulseAudio
{
StreamManager::StreamManager(Context *parent, bool autoUpdate)
	: QObject(parent), d(new Private)
{
    d->q = this;
    d->autoUpdate = autoUpdate;
    d->context = parent;
}

StreamManager::~StreamManager()
{
    delete d;
}

void StreamManager::add(Stream *s)
{
    d->streamsById.insert(s->index(), s);
    if(s->isValid())
	d->streamsByName.insert(s->name(), s);
}

void StreamManager::remove(Stream *s)
{
    d->streamsById.remove(s->index());
    d->streamsByName.remove(s->name());
}

Stream *StreamManager::stream(int id)
{
    return d->streamsById[id];
}

Stream *StreamManager::stream(const QString &name)
{
    return d->streamsByName[name];
}

void StreamManager::event(int type, uint32_t index)
{
    cout << "StreamManager::event(" << type << ", " << index << ")" << endl;
    Stream *s;
    if (type == PA_SUBSCRIPTION_EVENT_REMOVE)
    {
	s = stream(index);
	if(s != NULL)
	{
	    emit removed(index);
	    remove(s);
	}
    }
    else if (type == PA_SUBSCRIPTION_EVENT_CHANGE || type==PA_SUBSCRIPTION_EVENT_NEW) {
	if((s = stream(index)) == 0)
	{
	    s = create(index);
	    add(s);
	    emit added(index);
	}
	else
	{
	    emit changed(index);
	    if (d->autoUpdate)
		s->update();
	}
    }
}
}