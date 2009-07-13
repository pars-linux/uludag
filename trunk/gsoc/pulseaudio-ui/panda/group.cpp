#include "group.h"
#include "groupmanager.h"
#include "../bindings/streammanager.h"


Group::Group(QtPulseAudio::StreamManager* s, GroupManager *parent): QObject(parent)
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

void Group::setVolume(int volume)
{
    foreach(int i, indexes)
    {
	QtPulseAudio::Stream *s = manager->stream(i);
	if(s->isValid())
	{
	    pa_cvolume vol = s->volume();
	    pa_cvolume_scale(&vol, volume);
	    s->setVolume(vol);
	}
    }
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
