/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef COMAR_TEST_H
#define COMAR_TEST_H

#include <kcmodule.h>

class KAboutData;
class KLineEdit;
class QLabel;

class ComarTest : public KCModule
{
    Q_OBJECT

public:
    ComarTest( QWidget *parent = 0, const char* name = 0 );
    ~ComarTest() {};

    virtual void load();
    virtual void save();
    virtual void defaults();
    virtual QString quickHelp() const;
    virtual const KAboutData *aboutData () const {
	return ComarTestAbout;
    };

public slots:
    void configChanged();

private:
    KAboutData *ComarTestAbout;

};

#endif // COMAR_TEST_H
