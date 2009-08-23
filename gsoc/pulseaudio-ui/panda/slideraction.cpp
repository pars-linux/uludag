#include "slideraction.h"
#include <iostream>
#include <kicon.h>
#include <QSlider>
#include <QLabel>


SliderAction::SliderAction(QObject* parent): QWidgetAction(parent)
{
    widget = new QWidget;
    QHBoxLayout *layout = new QHBoxLayout(widget);
    
    iconLabel = new QLabel(widget);
    layout->addWidget(iconLabel);
    slider = new QSlider(Qt::Horizontal, widget);
    slider->setMinimum(0);
    slider->setMaximum(65535);
    layout->addWidget(slider);
    /*QWidget *infoWidget = new QWidget(widget);
    QHBoxLayout *infoLayout = new QHBoxLayout(infoWidget);
    infoLayout->addWidget(new QLabel("Group name"));
    layout->addWidget(infoWidget);*/
    QObject::connect(slider, SIGNAL(valueChanged(int)), this, SIGNAL(valueChanged(int)));
    
    setDefaultWidget(widget);
}


void SliderAction::setWidgetIcon(const QIcon &icon )
{
    iconLabel->setPixmap(icon.pixmap(16, 16));
}


void SliderAction::setWidgetToolTip(const QString &toolTip)
{
    widget->setToolTip(toolTip);
}



void SliderAction::setValue(int v)
{
    slider->setValue(v);
}