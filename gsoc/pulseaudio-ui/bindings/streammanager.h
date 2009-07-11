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
#ifndef QTPULSEAUDIO_STREAMMANAGER_H
#define QTPULSEAUDIO_STREAMMANAGER_H

#include <QObject>

namespace QtPulseAudio
{

class Context;
class Stream;

class StreamManager : public QObject
{
    Q_OBJECT
public:
    Stream *stream(int index);
    Stream *stream(const QString &name);
    virtual Stream *create(int index) = 0;

public slots:
    virtual void update() = 0;

signals:
    void removed(int index);
    void changed(int index);
    void added(int index);
    void unknown(int index);

protected:
    void add(Stream *s);
    void remove(Stream *s);
    void event(int type, uint32_t index);
    
    class Private;
    Private *d;
    friend class Context;
    friend class Private;
    StreamManager(Context *parent = NULL, bool autoUpdate=true);
    ~StreamManager();
};
}
#endif
