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
#ifndef __QtPulseAudioStreamManager_h__
#define __QtPulseAudioStreamManager_h__

#include <QObject>

namespace QtPulseAudio {

class Context;
class Stream;

class StreamManager : public QObject {
	Q_OBJECT
public:
	virtual Stream *stream(int index) = 0;

public slots:
	virtual void update() = 0;

signals:
	void removed(int index);
	void changed(int index);
	void added(int index);
	void unknow(int index);

protected:
	friend class Context;
	StreamManager(Context *parent = NULL);
	~StreamManager();
};

}

#endif
