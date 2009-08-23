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
#ifndef PANDA_GROUPSCONFIG_H
#define PANDA_GROUPSCONFIG_H
#include <QtGui>
#include <kicondialog.h>

#include "groupsdata.h"


class GroupsConfigWidget: public QWidget
{
    Q_OBJECT
    public:
    GroupsConfigWidget(QWidget* parent = 0);
    public slots:
    void save();
    void load();
    protected slots:
    void createGroup();
    void deleteGroup();
    void dataToWidget(QString name);
    void dataFromWidget(QString name);
    protected:
    QListWidget *groupsList;
    QHBoxLayout *layout;
    QWidget *leftWidget;
    QWidget *rightWidget;
    KIconButton *iconButton;
    QFormLayout *rightLayout;
    QVBoxLayout *leftLayout;
    QPushButton *newGroupButton;
    QPushButton *deleteGroupButton;
    QHash<QString, GroupData> groups;
    protected slots:
    void currentItemChanged(QListWidgetItem *,QListWidgetItem *);
    private:
    QLabel* nameLabel;
    QLabel* nameVLabel;
};
#endif
