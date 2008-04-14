#ifndef AUTHDIALOG_H
#define AUTHDIALOG_H

#include <polkit/polkit.h>

#include "authdialogui.h"

class AuthDialog : public AuthDialogUI
{
    Q_OBJECT

public:
    AuthDialog();
    ~AuthDialog();
    const char* getPass();
    void setType(PolKitResult type);
    void setContent(const QString &);
    void setContent();
    void setHeader(const QString &);

private:
    void showUsersCombo();
    void hideUsersCombo();
    void setPasswordFor(bool set, const QString& user = NULL);
    PolKitResult m_type;
};

#endif // AUTHDIALOG_H
