/*
  Copyright (c) 2005-2006, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef __TASMATV_H__
#define __TASMATV_H__

#include <QWidget>
 #include <KCModule>
#include "tvconfig.h"

#define AUTO_CARD 0
#define AUTO_TUNER 4

class KAboutData;
class TvConfigUI;

class TasmaTv :  public KCModule
{
   Q_OBJECT

    public:
        TasmaTv(QWidget *parent = 0, const QStringList &lst = QStringList());
        //TasmaTv(QWidget *parent = 0, const QStringList &lst = QStringList());
        ~TasmaTv() {}

        virtual void load();
        virtual void save();
        virtual void defaults();
        virtual QString quickHelp() const;

    public slots:
        void configChanged();
        void cardManListChanged();
        void tunerManListChanged();

    private:
        TvConfig *mainWidget;
        KAboutData *TasmaTvAbout;

};

#endif  //__TASMATV_H__
