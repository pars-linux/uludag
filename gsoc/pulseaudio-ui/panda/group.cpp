#include "group.h"
#include "groupmanager.h"
#include "../bindings/streammanager.h"


Group::Group(GroupData gd, QtPulseAudio::StreamManager* s, GroupManager *parent): QObject(parent), groupData(gd)
{
    manager = s;
}

void Group::addStream(int i)
{
    indexes.insert(i);
    emit streamAdded(i);
}

void Group::removeStream(int i)
{
    emit streamRemoved(i);
    indexes.remove(i);
}

void Group::setVolume(int vol)
{
    _volume = vol;
    foreach(int i, indexes)
    {
	QtPulseAudio::Stream *s = manager->stream(i);
	if(s->isValid())
	{
	    pa_cvolume vol = s->volume();
	    pa_cvolume_scale(&vol, _volume);
	    s->setVolume(vol);
	}
    }
    emit volumeChanged(vol);
}


QString Group::streamTitle(int index)
{
    return manager->stream(index)->getProperty("application.name");
}


QString Group::streamIcon(int index)
{
    return manager->stream(index)->getProperty("application.icon_name");
}


QString Group::streamInfo(int index)
{
    return QString("TODO");
}


QString Group::name()
{
    return groupData.name;
}


QString Group::iconName()
{
    return groupData.icon;
}


int Group::volume()
{
    return _volume;
}