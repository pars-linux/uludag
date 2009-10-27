#include "groupsdata.h"

#include <kconfiggroup.h>

QList<GroupData> load_groups(KConfig* config)
{
    QString gname;
    QList<GroupData> ret;
    foreach(QString gname, config->groupList())
	if(gname.startsWith("Group "))
	{
	    GroupData gd;
	    KConfigGroup cg =  config->group(gname);
	    gd.name = cg.readEntry("name");
	    gd.icon = cg.readEntry("icon");
	    ret.append(gd);
	}
    return ret;
}


void save_groups(const QList< GroupData >& groups, KConfig* config)
{
    foreach(QString gname, config->groupList())
	if(gname.startsWith("Group "))
	    config->deleteGroup(gname);
	
    foreach(const GroupData &gd, groups)
    {
	QString gname = QString("Group ") + gd.name;
	KConfigGroup cg =  config->group(gname);
	cg.writeEntry("name", gd.name);
	cg.writeEntry("icon", gd.icon);
    }
}