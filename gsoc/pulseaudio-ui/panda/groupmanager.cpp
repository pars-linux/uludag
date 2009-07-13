#include <iostream>
#include "groupmanager.h"
#include "group.h"
#include "../bindings/streammanager.h"

using namespace std;

GroupManager::GroupManager(QtPulseAudio::StreamManager* manager, QObject* parent): QObject(parent)
{
    this->manager = manager;
    createGroup("");
    createGroup("video");
    createGroup("music");
    //createGroup("game");
    createGroup("event");
    //createGroup("phone");
    //createGroup("animation");
    //createGroup("production");
    createGroup("a11y");
    QObject::connect(manager, SIGNAL(added(int)), this, SLOT(addStream(int)));
    QObject::connect(manager, SIGNAL(removed(int)), this, SLOT(removeStream(int)));
    manager->update();
}

void GroupManager::addStream(int index)
{
    cerr << "GroupManager::addStream " << index << endl;
    QtPulseAudio::Stream *s = manager->stream(index);
    if(s->isValid())
    {
	dispatchStream(s);
    }
    else
    {
	QObject::connect(s, SIGNAL(updated()), this, SLOT(streamReady()));
	s->update();
    }
}

void GroupManager::streamReady()
{
    cerr << "----------------- stream ready now" << endl;
    QtPulseAudio::Stream *s = qobject_cast<QtPulseAudio::Stream *>(sender());
    if(s->isValid())
    {
	dispatchStream(s);
    }
}

void GroupManager::dispatchStream(QtPulseAudio::Stream *s)
{
    QString gname = s->getProperty("media.role");
    QString aname = s->getProperty("application.name");
    
    /* rather dirty */
    if(aname == "amarok")
	gname = "music";
    else if(aname == "kaffeine" || aname == "dragon")
	gname = "video";
    
    int index = s->index();
    streamGroup[index] = gname;
    groups[gname]->addStream(index);
    QObject::disconnect(s, SIGNAL(updated()), this, SLOT(streamReady()));
}

void GroupManager::removeStream(int index)
{
    QString gname = streamGroup[index];
    groups[gname]->removeStream(index);
    streamGroup.remove(index);
}

QList< QString > GroupManager::groupNames()
{
    return groups.keys();
}

Group *GroupManager::group(const QString &name)
{
    return groups[name];
}


void GroupManager::createGroup(const QString &name)
{
    groups[name] = new Group(manager, this);
}
