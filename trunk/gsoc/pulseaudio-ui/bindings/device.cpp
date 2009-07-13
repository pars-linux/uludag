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

#include "device.h"
#include "device_p.h"

namespace QtPulseAudio
{

Device::Device(int index, QtPulseAudio::StreamManager* parent): Stream(parent), d(new Private)
{
    d->index = index;
    d->manager = parent;
    d->proplist = 0;
}

Device::~Device()
{
    delete d;
}

uint32_t Device::index()
{
    return d->index;
}

QString Device::name()
{
    return d->name;
}

QString Device::description()
{
    return d->description;
}

bool Device::isValid()
{
    return d->valid;
}


int Device::muted()
{
    return d->muted;
}

pa_cvolume Device::volume()
{
    return d->volume;
}

uint32_t Device::card()
{
    return d->card;
}

pa_usec_t Device::latency()
{
    return d->latency;
}

pa_usec_t Device::configuredLatency()
{
    return d->configuredLatency;
}

pa_volume_t Device::baseVolume()
{
    return d->baseVolume;
}


uint32_t Device::owner()
{
    return d->owner;
}

QString Device::driver()
{
    return d->driver;
}

uint32_t Device::monitor()
{
    return d->monitor;
}

QString Device::monitorName()
{
    return d->monitorName;
}

pa_channel_map Device::channelMap()
{
    return d->channelMap;
}


pa_sample_spec Device::sampleSpec()
{
    return d->sampleSpec;
}


QString Device::getProperty(QString key)
{
    return QString(pa_proplist_gets(d->proplist, key.toUtf8().data()));
}

}
