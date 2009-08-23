#include "groupsconfig.h"
#include <kinputdialog.h>
#include <ksharedconfig.h>

GroupsConfigWidget::GroupsConfigWidget(QWidget* parent): QWidget(parent)
{
    leftWidget = new QWidget(this);
    leftLayout = new QVBoxLayout(leftWidget);
    layout = new QHBoxLayout(this);
    groupsList = new QListWidget(leftWidget);
    leftLayout->addWidget(groupsList);
    newGroupButton = new QPushButton("New", leftWidget);
    deleteGroupButton = new QPushButton("Remove", leftWidget);
    leftLayout->addWidget(newGroupButton);
    leftLayout->addWidget(deleteGroupButton);
    rightWidget = new QWidget(this);
    QFormLayout *rightLayout = new QFormLayout(rightWidget);
    QLabel *iconLabel = new QLabel("Icon", rightWidget);
    iconButton = new KIconButton(rightWidget);
    iconButton->setIconType(KIconLoader::Desktop, KIconLoader::Any);
    nameLabel = new QLabel("Name", rightWidget);
    nameVLabel = new QLabel("", rightWidget);
    rightLayout->addRow(nameLabel, nameVLabel);
    rightLayout->addRow(iconLabel, iconButton);
    layout->addWidget(leftWidget);
    layout->addWidget(rightWidget);
    QObject::connect(newGroupButton, SIGNAL(pressed()), this, SLOT(createGroup()));
    QObject::connect(deleteGroupButton, SIGNAL(pressed()), this, SLOT(deleteGroup()));
    
    QObject::connect(groupsList, SIGNAL(currentItemChanged(QListWidgetItem*,QListWidgetItem*)),
		     this, SLOT(currentItemChanged(QListWidgetItem*,QListWidgetItem*)));
    load();
}


void GroupsConfigWidget::currentItemChanged(QListWidgetItem *current , QListWidgetItem *prev)
{
    if(prev)
	dataFromWidget(prev->text());
    if(current)
	dataToWidget(current->text());
}

void GroupsConfigWidget::dataFromWidget(QString name)
{
    GroupData &gd = groups[name];
    gd.icon = iconButton->icon();
}

void GroupsConfigWidget::dataToWidget(QString name)
{
    GroupData &gd = groups[name];
    iconButton->setIcon(gd.icon);
    nameVLabel->setText(gd.name);
}

void GroupsConfigWidget::createGroup()
{
    //TODO: create validator
    QString name = KInputDialog::getText("Group name", "Group name");
    groupsList->addItem(name);
    GroupData gd;
    gd.name = name;
    gd.icon = "";
    groups[name] = gd;
}

void GroupsConfigWidget::deleteGroup()
{
    QString name = groupsList->currentItem()->text();
    //groupsList->removeItemWidget(wi);
    groupsList->takeItem(groupsList->currentRow());
    groups.remove(name);
}


void GroupsConfigWidget::load()
{
    groups.clear();
    const QList<GroupData> &gl = load_groups(KGlobal::config().data());
    foreach(GroupData gd, gl)
    {
	groupsList->addItem(gd.name);
	groups[gd.name] = gd;
    }
}

void GroupsConfigWidget::save()
{
    dataFromWidget(groupsList->currentItem()->text());
    save_groups(groups.values(), KGlobal::config().data());
    KGlobal::config()->sync();
}