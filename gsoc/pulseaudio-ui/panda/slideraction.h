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
#ifndef PANDA_SLIDERACTION_H
#define PANDA_SLIDERACTION_H
#include<QWidgetAction>
#include<QBoxLayout>

class QSlider;
class QLabel;

class SliderAction: public QWidgetAction
{
    Q_OBJECT
    public:
    SliderAction(QObject* parent);
    void setWidgetToolTip(const QString &);
    void setWidgetIcon(const QIcon &);
    signals:
    void valueChanged(int);
    public slots:
    void setValue(int);
    protected:
    //virtual QWidget* createWidget(QWidget* parent);
    private:
    QSlider *slider;
    QLabel *iconLabel;
    QWidget* widget;
};
#endif