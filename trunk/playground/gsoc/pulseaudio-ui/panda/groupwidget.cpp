#include <KDE/KIcon>

#include "groupwidget.h"
#include "group.h"

GroupWidget::GroupWidget(Group* g, QWidget *parent):QWidget(parent)
{
    group = g;
    listWidget = new QListWidget(this);
    listWidget->setViewMode(QListView::IconMode);
    listWidget->setIconSize(QSize(16, 16));
    listWidget->setSortingEnabled(true);
    listWidget->setMaximumHeight(40);
    listWidget->setGridSize(QSize(60, 40));
    listWidget->setMovement(QListView::Snap);
    listWidget->setDragEnabled(true);
    listWidget->setAcceptDrops(true);
    volumeSlider = new QSlider(this);
    volumeSlider->setOrientation(Qt::Horizontal);
    volumeSlider->setMinimum(0);
    volumeSlider->setMaximum(65535);
    layout = new QVBoxLayout(this);
    layout->addWidget(volumeSlider);
    layout->addWidget(listWidget);
    //setMinimumHeight(60);
    QObject::connect(group, SIGNAL(streamAdded(int)), this, SLOT(streamAdded(int)));
    QObject::connect(group, SIGNAL(streamRemoved(int)), this, SLOT(streamRemoved(int)));
    QObject::connect(volumeSlider, SIGNAL(sliderMoved(int)), group, SLOT(setVolume(int)));
    QObject::connect(group, SIGNAL(volumeChanged(int)), volumeSlider, SLOT(setValue(int)));
    
}


void GroupWidget::streamAdded(int index)
{
    KIcon icon(group->streamIcon(index));
    QString name(group->streamTitle(index));
    QListWidgetItem *item = new QListWidgetItem(icon, name, listWidget);
    itemMap[index] = item;
}

void GroupWidget::streamRemoved(int index)
{
    listWidget->removeItemWidget(itemMap[index]);
    itemMap.remove(index);
}
