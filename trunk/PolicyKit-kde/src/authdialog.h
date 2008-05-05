/*
  Copyright (c) 2007,2008 TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef AUTHDIALOG_H
#define AUTHDIALOG_H

#include <qdatetime.h>
#include <qimage.h>
#include <qpixmap.h>

#include <polkit/polkit.h>

#include "authdialogui.h"

class AuthDialog : public AuthDialogUI
{
    Q_OBJECT

public:
    AuthDialog(QString &header);
    ~AuthDialog();
    const char* getPass();
    void setType(PolKitResult type);
    void setContent(const QString &);
    void setContent();
    void setAdminUsers(const QStringList &);
    void setHeader(const QString &);
    void setPrompt(const QString &);

protected:
    virtual void keyPressEvent(QKeyEvent*);
    virtual bool focusNextPrevChild (bool);

private slots:
    void slotPaintEffect();
    void slotGrab();

private:
    void showUsersCombo();
    void hideUsersCombo();
    void setPasswordFor(bool set, const QString& user = NULL);
    PolKitResult m_type;
    QStringList m_users;

    int m_currentY;
    QImage m_grabbed;
    QPixmap m_root;
    QTime m_passed;
};

#endif // AUTHDIALOG_H
