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
    void setAdminUsers(const QStringList &);
    void setHeader(const QString &);
    void setPrompt(const QString &);

private:
    void showUsersCombo();
    void hideUsersCombo();
    void setPasswordFor(bool set, const QString& user = NULL);
    PolKitResult m_type;
    QStringList m_users;
};

#endif // AUTHDIALOG_H
