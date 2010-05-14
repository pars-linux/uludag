/*
   Copyright (C) 2010 by Ozan Çağlayan <ozan@pardus.org.tr>

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2, or (at your option)
   any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

*/

#include "notifybyosd.h"
#include "knotifyconfig.h"
#include "imageconverter.h"

#include <kconfiggroup.h>
#include <kiconloader.h>
#include <kdialog.h>
#include <kdebug.h>
#include <khbox.h>
#include <kvbox.h>

#include <QDBusConnectionInterface>
#include <QGraphicsLinearLayout>
#include <QGraphicsWidget>
#include <QDBusConnection>
#include <QDesktopWidget>
#include <QTextDocument>
#include <QApplication>
#include <QVBoxLayout>
#include <QImage>
#include <QLabel>


// D-Bus Service
static const char dbusServiceName[] = "org.kde.osd";
static const char dbusInterfaceName[] = "org.kde.osd";
static const char dbusPath[] = "/org/kde/osd";


NotifyByOsd::NotifyByOsd(QObject *parent)
: KNotifyPlugin(parent)
, m_dialog(new Plasma::Dialog(0, Qt::Window | Qt::WindowStaysOnTopHint | Qt::FramelessWindowHint | Qt::X11BypassWindowManagerHint))
, m_meter(new QProgressBar)
, m_osdIcon(new QLabel)
, m_osdText(new QLabel)
, m_layout(new QGridLayout(m_dialog))
, m_timer(new QTimer)
, m_timeout(2)
, m_hPosition(50)
, m_vPosition(70)
, m_width(300)  // FIXME: hardcoded
, m_height(120)
, m_dbusServiceExists(false)
, m_lockPrimaryScreen(false)
, m_isVisible(false)
{
    // Check if service already exists on plugin instantiation
    QDBusConnectionInterface* interface = QDBusConnection::sessionBus().interface();
    m_dbusServiceExists = interface && interface->isServiceRegistered(dbusServiceName);

    if (m_dbusServiceExists) {
        // Connect signals
        slotServiceOwnerChanged(dbusServiceName, QString(), "_");
    }

    // to catch register/unregister events from service in runtime
    connect(interface, SIGNAL(serviceOwnerChanged(const QString&, const QString&, const QString&)),
                       SLOT(slotServiceOwnerChanged(const QString&, const QString&, const QString&)));

    // Setup timer
    m_timer->setSingleShot(true);
    connect(m_timer, SIGNAL(timeout()), this, SLOT(slotHideOsd()));

    // FIXME: Give an initial progress value
    QFont meterFont;
    meterFont.setPixelSize((int)(18 / 7.0f * 4.0f));
    meterFont.setBold(true);
    m_meter->setFont(meterFont);
    m_meter->setValue(75);

    // Setup layout
    initLayout();
}


NotifyByOsd::~NotifyByOsd()
{
}

void NotifyByOsd::initLayout()
{
    // Create spacers
    QSpacerItem *hSpacer = new QSpacerItem(72, 29, QSizePolicy::Expanding, QSizePolicy::Minimum);
    m_layout->addItem(hSpacer, 0, 0, 1, 1);

    m_layout->addWidget(m_osdIcon, 0, 1, 1, 1);
    m_layout->addWidget(m_osdText, 0, 2, 1, 1);

    QSpacerItem *hSpacer2 = new QSpacerItem(72, 29, QSizePolicy::Expanding, QSizePolicy::Minimum);
    m_layout->addItem(hSpacer2, 0, 3, 1, 1);

    m_layout->addWidget(m_meter, 1, 0, 1, 4);

    m_dialog->setLayout(m_layout);
}

void NotifyByOsd::updateOsdPosition()
{
    QRect rect;
    if (m_lockPrimaryScreen)
        rect = QApplication::desktop()->screenGeometry(QApplication::desktop()->primaryScreen());
    else
        rect = QApplication::desktop()->screenGeometry(QCursor::pos());

    m_xPosition = rect.x() + (unsigned int)((rect.width() - m_width) / 100.0f * m_hPosition);
    m_yPosition = rect.y() + (unsigned int)((rect.height() - m_height) / 100.0f * m_vPosition);

    m_dialog->setGeometry(m_xPosition, m_yPosition, m_width, m_height);
}

void NotifyByOsd::fillOsd(int id, KNotifyConfig * config)
{
    //Q_UNUSED(id)

    QString appCaption, iconName;
    getAppCaptionAndIconName(config, &appCaption, &iconName);

    if (!config->image.isNull()) {
        QPixmap pix = QPixmap::fromImage(config->image.toImage());
        m_osdIcon->setPixmap(pix);
    }
    else {
        m_osdIcon->setPixmap(KIconLoader::global()->loadIcon(iconName, KIconLoader::Desktop, KIconLoader::SizeMedium));
    }
}

void NotifyByOsd::notify(int id, KNotifyConfig * config)
{
    kDebug(300) << id << "  active notifications:" << m_dialogs.keys() << m_idMap.keys();

    if(m_dialogs.contains(id) || m_idMap.contains(id))
    {
        kDebug(300) << "the popup is already shown";
        finish(id);
        return;
    }

    // if Notifications DBus service exists on bus,
    // it'll be used instead
    if(m_dbusServiceExists)
    {
        if(!sendNotificationDBus(id, 0, config)) {
            finish(id); //an error ocurred.
        }
        return;
    }

    updateOsdPosition();
    fillOsd(id, config);
    m_dialog->show();

    m_isVisible = true;
    m_timer->start(m_timeout*1000);

}

void NotifyByOsd::close(int id)
{
    delete m_dialogs.take(id);

    if (m_dbusServiceExists) {
        closeNotificationDBus(id);
    }
}

void NotifyByOsd::update(int id, KNotifyConfig * config)
{
    /*
    if (m_dialogs.contains(id)) {
        Plasma::Dialog *p = m_dialogs[id];
        fillPopup(p, id, config);
        return;
    }

    // if Notifications DBus service exists on bus,
    // it'll be used instead
    if (m_dbusServiceExists)
    {
        sendNotificationDBus(id, id, config);
        return;
    }
    */
}

void NotifyByOsd::getAppCaptionAndIconName(KNotifyConfig *config, QString *appCaption, QString *iconName)
{
    KConfigGroup globalgroup(&(*config->eventsfile), "Global");
    *appCaption = globalgroup.readEntry("Name", globalgroup.readEntry("Comment", config->appname));
    *iconName = globalgroup.readEntry("IconName", config->appname);
}

void NotifyByOsd::slotHideOsd()
{
    m_dialog->hide();
    m_isVisible = false;
}
























void NotifyByOsd::slotDBusNotificationClosed(uint dbus_id, uint reason)
{
    Q_UNUSED(reason)

    // find out knotify id
    int id = m_idMap.key(dbus_id, 0);

    kDebug(300) << dbus_id << "  -> " << id;
    if (id == 0) {
        kDebug(300) << "failed to find knotify id for dbus_id" << dbus_id;
        return;
    }
    // tell KNotify that this notification has been closed
    m_idMap.remove(id);
    finished(id);
}


void NotifyByOsd::slotServiceOwnerChanged(const QString & serviceName,
        const QString & oldOwner, const QString & newOwner)
{
    if (serviceName == dbusServiceName) {
        kDebug(300) << serviceName << oldOwner << newOwner;
        // tell KNotify that all existing notifications which it sent
        // to DBus had been closed
        foreach (int id, m_idMap.keys())
            finished(id);
        m_idMap.clear();

        if(newOwner.isEmpty()) {
            m_dbusServiceExists = false;
        }
        else if(oldOwner.isEmpty()) {
            m_dbusServiceExists = true;

            // connect to action invocation signals
            /*
            bool connected = QDBusConnection::sessionBus().connect(QString(), // from any service
                    dbusPath,
                    dbusInterfaceName,
                    "ActionInvoked",
                    this,
                    SLOT(slotDBusNotificationActionInvoked(uint, const QString&)));

            if (!connected) {
                kWarning(300) << "warning: failed to connect to ActionInvoked dbus signal";
            }
            */

            bool connected = QDBusConnection::sessionBus().connect(QString(), // from any service
                    dbusPath,
                    dbusInterfaceName,
                    "NotificationClosed",
                    this,
                    SLOT(slotDBusNotificationClosed(uint, uint)));

            if (!connected) {
                kWarning(300) << "warning: failed to connect to NotificationClosed dbus signal";
            }
        }
    }
}

bool NotifyByOsd::sendNotificationDBus(int id, int replacesId, KNotifyConfig* config)
{
    // figure out dbus id to replace if needed
    uint dbus_replaces_id = 0;
    if (replacesId != 0 ) {
        dbus_replaces_id = m_idMap.value(replacesId, 0);
        if (!dbus_replaces_id) {
            // The popup has been closed, there is nothing to replace.
            return false;
        }
    }

    QDBusMessage m = QDBusMessage::createMethodCall(dbusServiceName, dbusPath, dbusInterfaceName, "Notify");

    QList<QVariant> args;

    QString appCaption, iconName;
    getAppCaptionAndIconName(config, &appCaption, &iconName);

    args.append(appCaption); // app_name
    args.append(dbus_replaces_id); // replaces_id
    args.append(iconName); // app_icon
    args.append(config->title.isEmpty()?appCaption:config->title); // summary
    args.append(config->text); // body
    // galago spec defines action list to be list like
    // (act_id1, action1, act_id2, action2, ...)
    //
    // assign id's to actions like it's done in fillPopup() method
    // (i.e. starting from 1)
    QStringList actionList;
    int actId = 0;
    foreach (const QString& actName, config->actions) {
        actId++;
        actionList.append(QString::number(actId));
        actionList.append(actName);
    }

    args.append(actionList); // actions

    QVariantMap map;
    // let's see if we've got an image, and store the image in the hints map
    if (!config->image.isNull()) {
        QImage image = config->image.toImage();
        map["image_data"] = ImageConverter::variantForImage(image);
    }

    args.append(map); // hints
    args.append(config->timeout); // expire timout

    m.setArguments(args);
    QDBusMessage replyMsg = QDBusConnection::sessionBus().call(m);
    if(replyMsg.type() == QDBusMessage::ReplyMessage) {
        if (!replyMsg.arguments().isEmpty()) {
            uint dbus_id = replyMsg.arguments().at(0).toUInt();
            if (dbus_id == 0)
            {
                kDebug(300) << "error: dbus_id is null";
                return false;
            }
            if (dbus_replaces_id && dbus_id == dbus_replaces_id) {
                return true;
            }
#if 1
            int oldId = m_idMap.key(dbus_id, 0);
            if (oldId != 0) {
                kWarning(300) << "Received twice the same id "<< dbus_id << "( previous notification: " << oldId << ")";
                m_idMap.remove(oldId);
                finish(oldId);
            }
#endif
            m_idMap.insert(id, dbus_id);
            kDebug(300) << "mapping knotify id to dbus id:"<< id << "=>" << dbus_id;

            return true;
        } else {
            kDebug(300) << "error: received reply with no arguments";
        }
    } else if (replyMsg.type() == QDBusMessage::ErrorMessage) {
        kDebug(300) << "error: failed to send dbus message";
    } else {
        kDebug(300) << "unexpected reply type";
    }
    return false;
}


void NotifyByOsd::closeNotificationDBus(int id)
{
    uint dbus_id = m_idMap.take(id);
    if (dbus_id == 0) {
        kDebug(300) << "not found dbus id to close" << id;
        return;
    }

    QDBusMessage m = QDBusMessage::createMethodCall(dbusServiceName, dbusPath,
            dbusInterfaceName, "CloseNotification" );

    QList<QVariant> args;
    args.append(dbus_id);
    m.setArguments(args);

    bool queued = QDBusConnection::sessionBus().send(m);
    if(!queued) {
        kDebug(300) << "warning: failed to queue dbus message";
    }

}


#include "notifybyosd.moc"
