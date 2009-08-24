#include <iostream>
#include "groupsdata.h"
#include "rulesconfig.h"
#include <kinputdialog.h>
#include <ksharedconfig.h>
#include <klocalizedstring.h>
#include <pulse/proplist.h>


RulesConfigWidget::RulesConfigWidget(QWidget* parent): QWidget(parent)
{
    layout = new QHBoxLayout(this);
    
    leftWidget = new QWidget(this);
    leftLayout = new QVBoxLayout(leftWidget);
    rulesList = new QListWidget(this);
    leftLayout->addWidget(rulesList);
    QPushButton* upButton = new QPushButton(i18n("Up"), leftWidget);
    leftLayout->addWidget(upButton);
    QPushButton* downButton = new QPushButton(i18n("Down"), leftWidget);
    leftLayout->addWidget(downButton);
    newRuleButton = new QPushButton(i18n("New"));
    leftLayout->addWidget(newRuleButton);
    deleteRuleButton = new QPushButton(i18n("Delete"));
    leftLayout->addWidget(deleteRuleButton);
    layout->addWidget(leftWidget);
    
    rightWidget = new QWidget(this);
    rightLayout = new QFormLayout(rightWidget);
    QLabel *groupLabel = new QLabel(i18n("Group"));
    groupSelect = new QComboBox(rightWidget);
    rightLayout->addRow(groupLabel, groupSelect);
    QLabel *keyLabel = new QLabel(i18n("Key"));
    keySelect = new QComboBox;
    rightLayout->addRow(keyLabel, keySelect);
    QLabel *valueLabel = new QLabel(i18n("Value"));
    valueInput = new QLineEdit;
    rightLayout->addRow(valueLabel, valueInput);
    layout->addWidget(rightWidget);
    
    QObject::connect(rulesList, SIGNAL(currentItemChanged(QListWidgetItem*,QListWidgetItem*)),
		     this, SLOT(currentItemChanged(QListWidgetItem*,QListWidgetItem*)));
    QObject::connect(newRuleButton, SIGNAL(clicked()), this, SLOT(createRule()));
    QObject::connect(deleteRuleButton, SIGNAL(clicked()), this, SLOT(deleteRule()));
    QObject::connect(upButton, SIGNAL(clicked()), this, SLOT(ruleUp()));
    QObject::connect(downButton, SIGNAL(clicked()), this, SLOT(ruleDown()));
    load();
    configureKeys();
}

void RulesConfigWidget::reconfigureGroups()
{
    groupSelect->clear();
    const QList<GroupData> &gl = load_groups(KGlobal::config().data());
    foreach(GroupData gd, gl)
    {
	groupSelect->addItem(gd.name, gd.name);
    }
}

void RulesConfigWidget::configureKeys()
{
    keySelect->addItem(QString(i18n("Application name")), QString(PA_PROP_APPLICATION_NAME));
    keySelect->addItem(QString(i18n("Application binary")), QString(PA_PROP_APPLICATION_PROCESS_BINARY));
    keySelect->addItem(QString(i18n("Process user")), QString(PA_PROP_APPLICATION_PROCESS_USER));
}


void RulesConfigWidget::createRule()
{
    QString name = KInputDialog::getText(i18n("Rule name"), i18n("Rule name"));
    RuleData rd;
    rd.name = name;
    rd.group = QString("default");
    rd.key = QString(PA_PROP_APPLICATION_NAME);
    rd.value = QString();
    rules.append(rd);
    rulesList->addItem(rd.name);
}

void RulesConfigWidget::deleteRule()
{
    int i = rulesList->currentRow();
    rulesList->takeItem(i);
    rules.remove(i);
}

void RulesConfigWidget::dataFromWidget(int i)
{
    std::cout << "data from widget " << i << std::endl;
    if(i == -1)
	i = rulesList->currentRow();
    RuleData &rd = rules[i];
    rd.group = groupSelect->itemData(groupSelect->currentIndex()).toString();
    rd.key = keySelect->itemData(keySelect->currentIndex()).toString();
    rd.value = valueInput->text();
}

void RulesConfigWidget::dataToWidget(int i)
{
    std::cout << "data to widget " << i << std::endl;
    if(i == -1)
	i = rulesList->currentRow();
    const RuleData &rd = rules[i];
    int j = groupSelect->findData(rd.group);
    groupSelect->setCurrentIndex(j);
    j = keySelect->findData(rd.key);
    keySelect->setCurrentIndex(j);
    valueInput->setText(rd.value);
}

void RulesConfigWidget::currentItemChanged(QListWidgetItem *current, QListWidgetItem *prev)
{
    if(prev)
	dataFromWidget(rulesList->row(prev));
    if(current)
	dataToWidget(rulesList->row(current));
}


void RulesConfigWidget::load()
{
    rules.clear();
    rulesList->clear();
    reconfigureGroups();
    QList<RuleData> rl = load_rules(KGlobal::config().data());
    foreach(RuleData rd, rl)
    {
	rules.append(rd);
	rulesList->addItem(rd.name);
    }
    //dataToWidget();
}

void RulesConfigWidget::save()
{
    save_rules(rules.toList(), KGlobal::config().data());
    KGlobal::config()->sync();
}

void RulesConfigWidget::swapRules(int i, int j)
//i must be current item
{
    dataFromWidget(i);
    RuleData tmp = rules[j];
    rules[j] = rules[i];
    rules[i] = tmp;
    rulesList->item(i)->setText(rules[i].name);
    rulesList->item(j)->setText(rules[j].name);
    dataToWidget(i);
}

void RulesConfigWidget::ruleUp()
{
    int i = rulesList->currentRow();
    if(i == 0)
	return;
    swapRules(i, i-1);
}

void RulesConfigWidget::ruleDown()
{
    int i = rulesList->currentRow();
    if(i+1 == rules.size())
	return;
    swapRules(i, i+1);
}
