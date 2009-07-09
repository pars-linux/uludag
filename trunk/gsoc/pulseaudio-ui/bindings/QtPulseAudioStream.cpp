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

#include "QtPulseAudioStream.h"
#include "QtPulseAudioStreamManager.h"
#include "QtPulseAudioContext.h"

#include "QtPulseAudioStream_p.h"

using namespace std;

namespace QtPulseAudio {

Stream::Stream(StreamManager *parent)
	: QObject(parent)
{
}

Stream::~Stream()
{
}

}
