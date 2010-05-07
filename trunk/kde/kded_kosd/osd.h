/***************************************************************************
 *   Copyright (C) 2008-2009 by Marcel Hasler                              *
 *   mahasler@gmail.com                                                    *
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 *   This program is distributed in the hope that it will be useful,       *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU General Public License for more details.                          *
 *                                                                         *
 *   You should have received a copy of the GNU General Public License     *
 *   along with this program; if not, write to the                         *
 *   Free Software Foundation, Inc.,                                       *
 *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
 ***************************************************************************/

#ifndef OSD_H
#define OSD_H

#include <QTimer>
#include <QDesktopWidget>
#include <QProgressBar>

#include <KDE/Plasma/FrameSvg>

class OSD : public QWidget
{
    Q_OBJECT
    public:
        OSD();
        ~OSD();

        void setSize(unsigned int percent);
        void setPosition(unsigned int xPercent, unsigned int yPercent);
        void setOpacity(unsigned int percent);
        void setFakeTransparency(bool fake);
        void setPrimaryScreenLock(bool lock);
        void setTimeout(unsigned int seconds);

        void display(QString icon, QString text = "", unsigned int percent = 0);

        private slots:
            void slotHide();
        void slotReloadTheme();

    private:
        void updatePosition();
        void updateLayout();
        void paintEvent(QPaintEvent*);

        Plasma::FrameSvg m_backPanel;
        QRect m_rect;

        QPixmap m_icon;
        QRect m_iconRect;

        QString m_labelText;
        QRect m_labelRect;
        QFont m_labelFont;
        QColor m_labelColor;

        QProgressBar m_meter;

        QTimer m_timer;

        unsigned int m_hPos, m_vPos; // Relative positions (in percent)
        unsigned int m_xPos, m_yPos; // Absolute positions
        unsigned int m_width, m_height;
        unsigned int m_timeout;

        float m_scaleFactor;
        float m_opacity;
        bool m_fakeTransparency;
        bool m_lockPrimaryScreen;

        bool m_isVisible;
        QPixmap m_screenshot;
};

#endif // OSD_H
