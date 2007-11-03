#include "authdialog.h"
#include "authdialog.moc"

#include "qlabel.h"
#include "qstring.h"

#include "kglobal.h"
#include "kiconloader.h"
#include "kcombobox.h"

/* 
 *  Constructs a AuthDialog which is a child of 'parent', with the 
 *  name 'name' and widget flags set to 'f' 
 *
 *  The dialog will by default be modeless, unless you set 'modal' to
 *  TRUE to construct a modal dialog.
 */
AuthDialog::AuthDialog( QWidget* parent,  const char* name, bool modal, WFlags fl )
    : AuthDialogUI( parent, name, modal, fl )
{
    KIconLoader* iconloader = KGlobal::iconLoader();
    lblPixmap->setPixmap(iconloader->loadIcon("lock", KIcon::Desktop));

    cbUsers->hide();
}

/*  
 *  Destroys the object and frees any allocated resources
 */
AuthDialog::~AuthDialog()
{
    // no need to delete child widgets, Qt does it all for us
}

void AuthDialog::setHeader(const QString &header)
{
    lblHeader->setText(header);
}

void AuthDialog::setContent(const QString &msg)
{
    lblContent->setText(msg);
}

