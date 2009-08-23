#include "rulesdata.h"

#include <kconfiggroup.h>

QList< RuleData > load_rules(KConfig* config)
{
    QString gname;
    QList<RuleData> ret;
    int n = config->group("General").readEntry("rules_count", 0);
    for(int i=0;i<n;++i)
    {
	gname = QString("Rule %1").arg(i+1);
	RuleData rd;
	KConfigGroup cg =  config->group(gname);
	rd.key = cg.readEntry("key");
	rd.value = cg.readEntry("value");
	rd.group = cg.readEntry("group");
	rd.name = cg.readEntry("name");
	ret.append(rd);
    }
    return ret;
}



void save_rules(const QList< RuleData >& rules, KConfig* config)
{
    foreach(QString gname, config->groupList())
	if(gname.startsWith("Rule "))
	    config->deleteGroup(gname);
    
    config->group("General").writeEntry("rules_count", rules.size());
    int i = 1;
	
    foreach(const RuleData &rd, rules)
    {
	QString gname = QString("Rule %1").arg(i);
	KConfigGroup cg =  config->group(gname);
	cg.writeEntry("key", rd.key);
	cg.writeEntry("value", rd.value);
	cg.writeEntry("group", rd.group);
	cg.writeEntry("name", rd.name);
	++i;
    }
}