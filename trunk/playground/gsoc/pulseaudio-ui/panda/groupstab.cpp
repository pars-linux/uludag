#include "groupstab.h"
#include "groupmanager.h"
#include "groupwidget.h"


GroupsTab::GroupsTab(GroupManager* manager, QWidget* parent): QWidget(parent)
{
    this->manager = manager;
    //scrollArea = new QScrollArea(this);
    //scrollArea->setLayout(scrolledLayout);
    //scrolledWidget = new QWidget(scrollArea);
    //scrolledWidget = scrollArea;
    //scrolledLayout = new QVBoxLayout(scrolledWidget);
    layout = new QVBoxLayout(this);
    foreach(QString name, manager->groupNames())
	createGroup(name);
    //scrollArea->setWidget(scrolledWidget);
    //layout->addWidget(scrollArea);
    QObject::connect(manager, SIGNAL(groupCreated(QString)), this, SLOT(createGroup(QString)));
    QObject::connect(manager, SIGNAL(groupRemoved(QString)), this, SLOT(removeGroup(QString)));
}


void GroupsTab::createGroup(QString name)
{
    Group *g = manager->group(name);
    GroupWidget *gw = new GroupWidget(g, this);
    /*scrolledL*/layout->addWidget(gw);
}

void GroupsTab::removeGroup(QString name)
{
    //TODO
}
