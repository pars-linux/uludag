#ifndef AUTHDIALOG_H
#define AUTHDIALOG_H

#include <polkit/polkit.h>

#include "authdialogui.h"

class AuthDialog : public AuthDialogUI
{
    Q_OBJECT

public:
    AuthDialog( const QString &header = "", const QString& message = "", PolKitResult type = POLKIT_RESULT_ONLY_VIA_ADMIN_AUTH);
    ~AuthDialog();
    const char* getPass();
    void setType(PolKitResult type);
    void setContent(const QString &);
    void setHeader(const QString &);

private:
    void showUsersCombo();
    void hideUsersCombo();
    void setPasswordFor(bool set, const QString& user = NULL);

};

#endif // AUTHDIALOG_H
