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
#ifndef __QtPulseAudioSourceManager_h__
#define __QtPulseAudioSourceManager_h__

#include <QObject>

#include <pulse/pulseaudio.h>

#include "QtPulseAudioStreamManager.h"

namespace QtPulseAudio {

class Context;
class Source;

class SourceManager : public StreamManager {
	Q_OBJECT
public:
	virtual Stream *stream(int index);
	virtual Source *sink(int index);

public slots:
	virtual void update();

protected:
	friend class Context;
	SourceManager(Context *parent, bool autoUpdate = true);
	~SourceManager();

	class Private;
	friend class Private;
	Private *d;
};

}

#endif
