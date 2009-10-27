
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
#ifndef PANDA_RULESCONFIG_H
#define PANDA_RULESCONFIG_H
#include <QtGui>
#include <kicondialog.h>

#include "rulesdata.h"


class RulesConfigWidget: public QWidget
{
    Q_OBJECT
    public:
    RulesConfigWidget(QWidget* parent = 0);
    public slots:
    void save();
    void load();
    protected slots:
    void createRule();
    void deleteRule();
    void ruleUp();
    void ruleDown();
    void dataToWidget(int i=-1);
    void dataFromWidget(int i=-1);
    protected:
    QListWidget *rulesList;
    QHBoxLayout *layout;
    QWidget *leftWidget;
    QWidget *rightWidget;
    KIconButton *iconButton;
    QFormLayout *rightLayout;
    QVBoxLayout *leftLayout;
    QPushButton *newRuleButton;
    QPushButton *deleteRuleButton;
    QVector<RuleData> rules;
    protected slots:
    void currentItemChanged(QListWidgetItem *,QListWidgetItem *);
    void reconfigureGroups();
    private:
    void configureKeys();
    void swapRules(int, int);
    QLabel* nameLabel;
    QLabel* nameVLabel;
    QComboBox* groupSelect;
    QComboBox* keySelect;
    QLineEdit* valueInput;
};
#endif