/*
  Copyright (c) 2007,2008 TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include "authdialog.h"
#include "authdialog.moc"

#include <qcheckbox.h>
#include <qgroupbox.h>
#include <qimage.h>
#include <qlabel.h>
#include <qnamespace.h>
#include <qpixmap.h>
#include <qstring.h>
#include <qtimer.h>

#include <kcombobox.h>
#include <kglobal.h>
#include <kiconloader.h>
#include <kimageeffect.h>
#include <klineedit.h>
#include <klocale.h>
#include <kpixmap.h>
#include <kpushbutton.h>

#include "debug.h"

static const int maxFaded = 2300;
static const int slice = 20;

/* 
 *  Constructs a AuthDialog which is a child of 'parent', with the 
 *  name 'name' and widget flags set to 'f' 
 *
 *  The dialog will by default be modeless, unless you set 'modal' to
 *  TRUE to construct a modal dialog.
 */
AuthDialog::AuthDialog(QString &header)
    : AuthDialogUI( NULL, NULL, true, Qt::WType_Popup),
        m_currentY( 0 ), grabKeyboard( false )
{
    KIconLoader* iconloader = KGlobal::iconLoader();
    lblPixmap->setPixmap(iconloader->loadIcon("lock", KIcon::Desktop));
    pbOK->setIconSet(iconloader->loadIconSet("ok", KIcon::Small, 0, false));
    pbCancel->setIconSet(iconloader->loadIconSet("cancel", KIcon::Small, 0, false));

    lePassword->setFocus();
    cbUsers->hide();
    setHeader(header);

    setBackgroundMode(QWidget::NoBackground);
    QRect geo(QApplication::desktop()->geometry());
    setGeometry(geo);
    int dep = QPixmap::defaultDepth();
    if (dep == 24 || dep == 16)
    {
        dep = 32;
    }
    m_grabbed.create(geo.size(), dep);
    QTimer::singleShot(0, this, SLOT( slotGrab()));
    m_root.resize(width(), height());
}

AuthDialog::~AuthDialog()
{
}

void AuthDialog::paintEvent(QPaintEvent* ev)
{
    // Grab keyboard when widget is mapped to screen
    // It might be a little weird to do it here, but it works!
    if(!grabKeyboard)
    {
        lePassword->grabKeyboard();
        grabKeyboard = true;
    }
    QDialog::paintEvent(ev);
}

void AuthDialog::hideEvent(QHideEvent* ev)
{
    lePassword->releaseKeyboard();
    grabKeyboard = false;
    QDialog::hideEvent(ev);
}

void AuthDialog::keyPressEvent(QKeyEvent* e)
{
    // pressing Esc closes the dialog
    if (e->state() == 0 && e->key() == Key_Escape)
    {
        emit reject();
        return;
    }
    QDialog::keyPressEvent(e);
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
        //TODO: Add user selection support
        case POLKIT_RESULT_ONLY_VIA_ADMIN_AUTH:
        case POLKIT_RESULT_ONLY_VIA_ADMIN_AUTH_KEEP_SESSION:
        case POLKIT_RESULT_ONLY_VIA_ADMIN_AUTH_KEEP_ALWAYS:
            msg = i18n("An application is attempting to perform an action that requires privileges."
                    " Authentication as the <b>super user</b> is required to perform this action.");
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

void AuthDialog::setPrompt(const QString &prompt)
{
    lblPassword->setText(prompt);
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

    if (res == POLKIT_RESULT_ONLY_VIA_ADMIN_AUTH || \
            res == POLKIT_RESULT_ONLY_VIA_SELF_AUTH || \
            res == POLKIT_RESULT_ONLY_VIA_ADMIN_AUTH_ONE_SHOT || \
            res == POLKIT_RESULT_ONLY_VIA_SELF_AUTH_ONE_SHOT)
    {
        cbRemember->hide();
        cbSession->hide();
    }

    if (res == POLKIT_RESULT_ONLY_VIA_ADMIN_AUTH_KEEP_SESSION || res == POLKIT_RESULT_ONLY_VIA_SELF_AUTH_KEEP_SESSION)
    {
        cbRemember->hide();
        cbSession->setEnabled(true);
        cbSession->setText(i18n("Remember authorization for this session"));
    }

    m_type = res;

    //set content message according to m_type
    setContent();
}

void AuthDialog::slotGrab()
{
    // we start the passed early
    if (m_currentY * 4 >= height() * 3 && m_passed.isNull())
        m_passed.start();

    if (m_currentY >= height()) 
    {
        slotPaintEffect();
        return;
    }

    QImage img;
    img = QPixmap::grabWindow(qt_xrootwin(), 0, m_currentY, width(), slice);
    bitBlt(&m_grabbed, 0, m_currentY, &img);
    m_currentY += slice;
    QTimer::singleShot(0, this, SLOT(slotGrab()));
}

void AuthDialog::slotPaintEffect()
{
    const unsigned int shift_scale = 10;
    const unsigned int scale = 1 << shift_scale;

    int current_fade = QMIN(scale, m_passed.elapsed() * scale / maxFaded);

    QImage copy;

    if (m_grabbed.depth() == 32) 
    {
        copy.create(m_grabbed.size(), m_grabbed.depth());
        unsigned int pixels = m_grabbed.width() * m_grabbed.height();
        QRgb *orig = (QRgb*)m_grabbed.bits();
        QRgb *dest = (QRgb*)copy.bits();
        QColor clr;

        int r, g, b, tg;

        for (unsigned int i = 0; i < pixels; ++i)
        {
            r = qRed(orig[i]);
            g = qGreen(orig[i]);
            b = qBlue(orig[i]);

            // qGray formla
            tg = (r*11 + g*16 + b*5)/32;
            // make it a bit darker than gray
            tg = tg - tg / 5;

            r = ((r << shift_scale) + current_fade * (tg - r)) >> shift_scale;
            g = ((g << shift_scale) + current_fade * (tg - g)) >> shift_scale;
            b = ((b << shift_scale) + current_fade * (tg - b)) >> shift_scale;

            dest[i] = qRgb(r, g, b);
        }
    } 
    else 
    {
        // old code - now used for 8bit
        copy = m_grabbed;
        copy = KImageEffect::desaturate(copy, current_fade);
        copy = KImageEffect::fade(copy, 0.1 * current_fade, Qt::black);
    }
    bitBlt( this, 0, 0, &copy);

    if (current_fade >= scale)
    {
        if (backgroundMode() == QWidget::NoBackground)
        {
            setBackgroundMode(QWidget::NoBackground);
            setBackgroundPixmap(copy);
        }
        return;
    }
    QTimer::singleShot(0, this, SLOT(slotPaintEffect()));
}
