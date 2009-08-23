#include <iostream>
#include <ksharedconfig.h>
#include "kglobal.h"

#include "groupmanager.h"
#include "group.h"
#include "groupsdata.h"
#include "../bindings/streammanager.h"

using namespace std;

GroupManager::GroupManager(QtPulseAudio::StreamManager* manager, QObject* parent): QObject(parent)
{
    this->manager = manager;
    QObject::connect(manager, SIGNAL(added(int)), this, SLOT(addStream(int)));
    QObject::connect(manager, SIGNAL(removed(int)), this, SLOT(removeStream(int)));
    reloadConfig();
    manager->update();
}

void GroupManager::reloadConfig()
{
    foreach(Group *g, groups.values())
	delete g;
    groups.clear();
    QList<GroupData> gl = load_groups(KGlobal::config().data());
    foreach(GroupData gd, gl)
	groups[gd.name] = new Group(gd, manager, this);
    
    rules = load_rules(KGlobal::config().data()).toVector();
    foreach(QtPulseAudio::Stream *s, streams)
	dispatchStream(s);
}

void GroupManager::addStream(int index)
{
    cerr << "GroupManager::addStream " << index << endl;
    QtPulseAudio::Stream *s = manager->stream(index);
    if(s->isValid())
    {
	dispatchStream(s);
	streams.insert(s);
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
	streams.insert(s);
    }
}

void GroupManager::dispatchStream(QtPulseAudio::Stream *s)
{
    int index = s->index();
    QString group;
    foreach(RuleData rd, rules)
    {
	if(s->getProperty(rd.key) == rd.value)
	{
	    group = rd.group;
	    break;
	}
    }
    
    if(!groups.contains(group))
	group = "default";
    
    streamGroup[index] = group;
    groups[group]->addStream(index);
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