/*
    Copyright (c) 2009      by Marcin Kurczych          <tharkang@gmail.com>

    *************************************************************************
    *                                                                       *
    * This program is free software; you can redistribute it and/or modify  *
    * it under the terms of the GNU General Public License as published by  *
    * the Free Software Foundation; either version 2 of the License, or     *
    * (at your option) any later version.                                   *
    *                                                                       *
    *************************************************************************
*/
#ifndef PANDA_GROUP_H
#define PANDA_GROUP_H
#include <QObject>
#include <QSet>

#include "groupsdata.h"
#include "../bindings/stream.h"

class GroupManager;

class Group: public QObject
{
    Q_OBJECT
    public:
    Group(GroupData gd, QtPulseAudio::StreamManager *s, GroupManager *parent);
    QString streamTitle(int index);
    QString streamIcon(int index);
    QString streamInfo(int index);
    QString name();
    QString iconName();
    int volume();
    
    public slots:
    void addStream(int index);
    void removeStream(int index);
    //void streamChanged();
    void setVolume(int volume);
    signals:
    void streamAdded(int index);
    void streamRemoved(int index);
    void volumeChanged(int volume);
    protected:
    GroupData groupData;
    QSet<int> indexes;
    QtPulseAudio::StreamManager *manager;
    int _volume;
};
#endif