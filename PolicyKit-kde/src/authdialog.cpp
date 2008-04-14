#include "authdialog.h"
#include "authdialog.moc"

#include <qlabel.h>
#include <qstring.h>
#include <qnamespace.h>
#include <qcheckbox.h>

#include <kglobal.h>
#include <klocale.h>
#include <kiconloader.h>
#include <kcombobox.h>
#include <kpushbutton.h>
#include <klineedit.h>

#include "debug.h"

/* 
 *  Constructs a AuthDialog which is a child of 'parent', with the 
 *  name 'name' and widget flags set to 'f' 
 *
 *  The dialog will by default be modeless, unless you set 'modal' to
 *  TRUE to construct a modal dialog.
 */
AuthDialog::AuthDialog()
    : AuthDialogUI( NULL, NULL, true, Qt::WStyle_StaysOnTop)
{
    KIconLoader* iconloader = KGlobal::iconLoader();
    lblPixmap->setPixmap(iconloader->loadIcon("lock", KIcon::Desktop));
    pbOK->setIconSet(iconloader->loadIconSet("ok", KIcon::Small, 0, false));
    pbCancel->setIconSet(iconloader->loadIconSet("cancel", KIcon::Small, 0, false));

    cbUsers->hide();
}

AuthDialog::~AuthDialog()
{
}

void AuthDialog::setHeader(const QString &header)
{
    lblHeader->setText("<h3>" + header + "</h3>");
}

void AuthDialog::setContent(const QString &msg)
{
    lblContent->setText(msg);
}

void AuthDialog::setAdminUsers(const QStringList &users)
{
    m_users = users;
    //QString selected = cbUsers->currentText();

    if (m_users.empty())
    {
        hideUsersCombo();
        return;
    }

    cbUsers->clear();
    cbUsers->insertStringList(m_users);
    showUsersCombo();
}

// set content according to m_type, that is a PolKitResult 
void AuthDialog::setContent()
{
    QString msg;
    switch(m_type)
    {
        //TODO: Authentication as one of the users below...
        case POLKIT_RESULT_ONLY_VIA_ADMIN_AUTH:
        case POLKIT_RESULT_ONLY_VIA_ADMIN_AUTH_KEEP_SESSION:
        case POLKIT_RESULT_ONLY_VIA_ADMIN_AUTH_KEEP_ALWAYS:
            msg = i18n("An application is attempting to perform an action that requires privileges."
                    " Authentication as the super user is required to perform this action.");
            break;
        default:
            msg = i18n("An application is attempting to perform an action that requires privileges."
                    " Authentication is required to perform this action.");

    }
    lblContent->setText(msg);
}


void AuthDialog::showUsersCombo()
{
    cbUsers->show();
}

void AuthDialog::hideUsersCombo()
{
    cbUsers->hide();
}

void AuthDialog::setPasswordFor(bool set, const QString& user)
{
    if (set)
        lblPassword->setText(i18n("Password for root") + ":");
    else if (user)
        lblPassword->setText(i18n("Password for user(%1)").arg(user) + ":");
    else
        lblPassword->setText(i18n("Password") + ":");
}

const char* AuthDialog::getPass()
{
    return lePassword->text();
}

void AuthDialog::setType(PolKitResult res)
{
    if (res == POLKIT_RESULT_UNKNOWN || \
            res == POLKIT_RESULT_NO || \
            res == POLKIT_RESULT_YES || \
            res == POLKIT_RESULT_N_RESULTS )
    {
        QString msg = QString("Unexpected PolkitResult type sent: '%1'. Ignoring.").arg(polkit_result_to_string_representation(res));
        //TODO: Create exception classes
        throw msg;
    }

    if (res == POLKIT_RESULT_ONLY_VIA_ADMIN_AUTH || \
            res == POLKIT_RESULT_ONLY_VIA_ADMIN_AUTH_KEEP_SESSION || \
            res == POLKIT_RESULT_ONLY_VIA_ADMIN_AUTH_KEEP_ALWAYS)
        setPasswordFor(true);

    if (res == POLKIT_RESULT_ONLY_VIA_SELF_AUTH || \
            res == POLKIT_RESULT_ONLY_VIA_SELF_AUTH_KEEP_SESSION || \
            res == POLKIT_RESULT_ONLY_VIA_SELF_AUTH_KEEP_ALWAYS)
        setPasswordFor(false);

    if (res == POLKIT_RESULT_ONLY_VIA_ADMIN_AUTH || res == POLKIT_RESULT_ONLY_VIA_SELF_AUTH)
    {
        cbRemember->hide();
        cbSession->hide();
    }

    if (res == POLKIT_RESULT_ONLY_VIA_ADMIN_AUTH_KEEP_SESSION || res == POLKIT_RESULT_ONLY_VIA_SELF_AUTH_KEEP_SESSION)
        cbRemember->hide();

    m_type = res;
}
