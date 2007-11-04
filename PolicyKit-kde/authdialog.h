#ifndef AUTHDIALOG_H
#define AUTHDIALOG_H
#include "authdialogui.h"

class AuthDialog : public AuthDialogUI
{
    Q_OBJECT

public:
    AuthDialog( QWidget* parent = 0, const char* name = 0, bool modal = FALSE, WFlags fl = 0 );
    ~AuthDialog();

    void setContent(const QString &);
    void setHeader(const QString &);
    void showUsersCombo();
    void hideUsersCombo();

};

#endif // AUTHDIALOG_H
