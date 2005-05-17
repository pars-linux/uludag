/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef GOZLUK_SETTINGS_H
#define GOZLUK_SETTINGS_H

#include <qdialog.h>
#include <qpushbutton.h>
#include <qlineedit.h>

class GozlukSettings : public QDialog
{
    Q_OBJECT

public:
    GozlukSettings( QWidget *parent = 0, const char *name = 0 );
    ~GozlukSettings(){};

protected slots:
    void slotApply();
    void slotCancel();
	 void slotDir();
private:
    QLineEdit *sozlukPath;
    QPushButton *dirButton;
    QPushButton *applyButton;
    QPushButton *cancelButton;
};

#endif // GOZLUK_SETTINGS_H
