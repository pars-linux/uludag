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
#include <kpassdlg.h>

/* 
 *  Constructs a AuthDialog which is a child of 'parent', with the 
 *  name 'name' and widget flags set to 'f' 
 *
 *  The dialog will by default be modeless, unless you set 'modal' to
 *  TRUE to construct a modal dialog.
 */
AuthDialog::AuthDialog( const QString &header,
            const QString &message,
            PolKitResult type)
    : AuthDialogUI( NULL, NULL, true, Qt::WStyle_StaysOnTop)
{
    KIconLoader* iconloader = KGlobal::iconLoader();
    lblPixmap->setPixmap(iconloader->loadIcon("lock", KIcon::Desktop));
    pbOK->setIconSet(iconloader->loadIconSet("ok", KIcon::Small, 0, false));
    pbCancel->setIconSet(iconloader->loadIconSet("cancel", KIcon::Small, 0, false));

    cbUsers->hide();

    setType(type);
    setHeader(header);
    setContent(message);
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
    return pePassword->password();
}

void AuthDialog::setType(PolKitResult res)
{
    if (res == POLKIT_RESULT_UNKNOWN || \
            res == POLKIT_RESULT_NO || \
            res == POLKIT_RESULT_YES || \
            res == POLKIT_RESULT_N_RESULTS )
    {
        qWarning("Unexpected PolkitResult type sent. Ignoring.");
        return;
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
}
