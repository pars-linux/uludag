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

#ifndef NOTIFYBYOSD_H
#define NOTIFYBYOSD_H

#include "knotifyplugin.h"

#include <QMap>
#include <QHash>
#include <QTimer>
#include <QLabel>
#include <QGridLayout>
#include <QProgressBar>

#include <Plasma/Meter>
#include <Plasma/Dialog>

class NotifyByOsd : public KNotifyPlugin
{
    Q_OBJECT
    public:
        NotifyByOsd(QObject *parent=0l);
        virtual ~NotifyByOsd();

        virtual QString optionName() { return "Osd"; }
        virtual void notify(int id, KNotifyConfig *config);
        virtual void close(int id);
        virtual void update(int id, KNotifyConfig *config);
    private:
        QMap<int, Plasma::Dialog * > m_dialogs;

        // Plasma::Dialog
        Plasma::Dialog *m_dialog;

        // Meter for progress status
        //Plasma::Meter *m_meter;
        QProgressBar *m_meter;

        QLabel *m_osdIcon;
        QLabel *m_osdText;

        QGridLayout *m_layout;

        // OSD timer
        QTimer *m_timer;

        // OSD timeout
        int m_timeout;

        // Dialog geometry & position
        int m_hPosition, m_vPosition;   // Relative position (percent)
        int m_xPosition, m_yPosition;   // Absolute position (pixel)
        int m_width, m_height;

        // Specifies if DBus Notifications interface exists on session bus
        bool m_dbusServiceExists;

        // Visualization stuff
        bool m_lockPrimaryScreen;
        bool m_isVisible;

        /**
         * Updates the position of the OSD widget on the screen.
         */
        void updateOsdPosition();


        /**
         * Populates OSD dialog with icon, progress bar and titles.
         */
        void fillOsd(int id, KNotifyConfig* config);

        /**
         * Initializes OSD visual layout.
         */
        void initLayout();

        /**
         * Sends notification to DBus "/Notifications" interface.
         * @param id knotify-sid identifier of notification
         * @param replacesId knotify-side notification identifier. If not 0, will
         * request DBus service to replace existing notification with data in config
         * @param config notification data
         * @return true for success or false if there was an error.
         */
        bool sendNotificationDBus(int id, int replacesId, KNotifyConfig* config);

        /**
         * Sends request to close Notification with id to DBus "/Notification" interface
         *  @param id knotify-side notification ID to close
         */
        void closeNotificationDBus(int id);

        /**
         * Find the caption and the icon name of the application
         */
        void getAppCaptionAndIconName(KNotifyConfig *config, QString *appCaption, QString *iconName);


    private Q_SLOTS:
        // slot to catch appearance or dissapearance of Notifications DBus service
        void slotServiceOwnerChanged(const QString &, const QString &, const QString &);

        // slot which gets called when DBus signals that some notification was closed
        void slotDBusNotificationClosed(uint, uint);

        // slot which hides the OSD dialog
        void slotHideOsd();

    private:
        /**
         * Maps knotify notification IDs to DBus notifications IDs
         */
        QHash<int,uint> m_idMap;
};

#endif
