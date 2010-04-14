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

#include "osd.h"

#include <QApplication>
#include <QWidget>
#include <QPainter>
#include <QBitmap>
#include <QCursor>
#include <QPaintEvent>

#include <KGlobalSettings>
#include <KIconLoader>
#include <Plasma/Svg>
#include <Plasma/Theme>

#include <iostream>
using namespace std;

#define OSD_BASE_WIDTH 900
#define OSD_BASE_HEIGHT 400

#define ICON_BASE_SIZE 200
//#define ICON_BASE_X 100
// Center the icon assuming that no kosd user passes a label!
#define ICON_BASE_X ((OSD_BASE_WIDTH/2.0)-(ICON_BASE_SIZE/2.0))
#define ICON_BASE_Y 50

#define LABEL_BASE_WIDTH 470
#define LABEL_BASE_HEIGHT 200
#define LABEL_BASE_X 320
#define LABEL_BASE_Y 50

#define METER_BASE_WIDTH 700
#define METER_BASE_HEIGHT 60
#define METER_BASE_X 100
#define METER_BASE_Y 280

#define FONT_BASE_SIZE 65

OSD::OSD()
    : QWidget(0, Qt::Window | Qt::WindowStaysOnTopHint | Qt::FramelessWindowHint | Qt::X11BypassWindowManagerHint),
    m_backPanel(this), m_meter(this), m_timer(this),
    m_hPos(50), m_vPos(70), m_scaleFactor(0.3f),
    m_lockPrimaryScreen(false), m_isVisible(false)
{
    // Load theme
    this->slotReloadTheme();
    connect(Plasma::Theme::defaultTheme(), SIGNAL(themeChanged()), this, SLOT(slotReloadTheme()));

    // Set timer
    m_timer.setSingleShot(true);
    connect(&m_timer, SIGNAL(timeout()), this, SLOT(slotHide()));

    this->setAttribute(Qt::WA_TranslucentBackground);

    this->setWindowOpacity(1.0);
    this->updateLayout();
}


OSD::~OSD()
{
    //
}


void OSD::setSize(unsigned int percent)
{
    if (percent > 100)
        percent = 100;
    else if (percent < 10)
        percent = 10;

    m_scaleFactor = (float)percent / 100.0f;
    this->updateLayout();
}


void OSD::setPosition(unsigned int xPercent, unsigned int yPercent)
{
    if (xPercent > 100)
        xPercent = 100;
    if (yPercent > 100)
        yPercent = 100;

    m_hPos = xPercent;
    m_vPos = yPercent;
}


void OSD::setOpacity(unsigned int percent)
{
    if (percent > 100)
        percent = 100;

    m_opacity = (float)percent / 100.0f;
    this->setWindowOpacity(m_opacity);
}


void OSD::setPrimaryScreenLock(bool lock)
{
    m_lockPrimaryScreen = lock;
}


void OSD::setTimeout(unsigned int seconds)
{
    if (seconds < 1)
        seconds = 1;

    m_timeout = seconds;
}


void OSD::updatePosition()
{
    QRect rect;
    if (m_lockPrimaryScreen)
        rect = QApplication::desktop()->screenGeometry(QApplication::desktop()->primaryScreen());
    else
        rect = QApplication::desktop()->screenGeometry(QCursor::pos());

    m_xPos = rect.x() + (unsigned int)((rect.width() - m_width) / 100.0f * m_hPos);
    m_yPos = rect.y() + (unsigned int)((rect.height() - m_height) / 100.0f * m_vPos);
    this->setGeometry(m_xPos, m_yPos, m_width, m_height);
}


void OSD::updateLayout()
{
    // OSD
    m_width = (unsigned int)(OSD_BASE_WIDTH * m_scaleFactor);
    m_height = (unsigned int)(OSD_BASE_HEIGHT * m_scaleFactor);
    m_rect.setRect(0, 0, m_width, m_height);

    // Icon
    unsigned int iconX = (unsigned int)(ICON_BASE_X * m_scaleFactor);
    unsigned int iconY = (unsigned int)(ICON_BASE_Y * m_scaleFactor);
    unsigned int iconSize = (unsigned int)(ICON_BASE_SIZE * m_scaleFactor);
    m_iconRect.setRect(iconX, iconY, iconSize, iconSize);

    // Label
    unsigned int labelX = (unsigned int)(LABEL_BASE_X * m_scaleFactor);
    unsigned int labelY = (unsigned int)(LABEL_BASE_Y * m_scaleFactor);
    unsigned int labelWidth = (unsigned int)(LABEL_BASE_WIDTH * m_scaleFactor);
    unsigned int labelHeight = (unsigned int)(LABEL_BASE_HEIGHT * m_scaleFactor);
    m_labelRect.setRect(labelX, labelY, labelWidth, labelHeight);
    m_labelFont.setPixelSize((unsigned int)(FONT_BASE_SIZE * m_scaleFactor));

    // Meter
    unsigned int meterX = (unsigned int)(METER_BASE_X * m_scaleFactor);
    unsigned int meterY = (unsigned int)(METER_BASE_Y * m_scaleFactor);
    unsigned int meterWidth = (unsigned int)(METER_BASE_WIDTH * m_scaleFactor);
    unsigned int meterHeight = (unsigned int)(METER_BASE_HEIGHT * m_scaleFactor);
    m_meter.setGeometry(meterX, meterY, meterWidth, meterHeight);

    QFont meterFont;
    meterFont.setPixelSize((int)(meterHeight / 7.0f * 4.0f));
    meterFont.setBold(true);
    m_meter.setFont(meterFont);

    m_backPanel.resizeFrame(QSize(m_width, m_height));
    this->setMask(m_backPanel.mask());
}


void OSD::display(QString icon, QString text, unsigned int percent)
{
    this->updatePosition();

    m_icon = KIconLoader::global()->loadIcon(icon, KIconLoader::NoGroup, m_iconRect.width());
    m_labelText = text;

    if (percent > 100)
        percent = 100;
    m_meter.setValue(percent);

    // Grab a screenshot for fake transparency
    if (!Plasma::Theme::defaultTheme()->windowTranslucencyEnabled() && !m_isVisible)
        m_screenshot = QPixmap::grabWindow(QApplication::desktop()->winId(), m_xPos, m_yPos, m_width, m_height);

    this->QWidget::show();
    this->QWidget::update();

    m_isVisible = true;
    m_timer.start(m_timeout*1000);
}


void OSD::slotHide()
{
    this->hide();
    m_isVisible = false;
}


void OSD::slotReloadTheme()
{
    // Load back panel
    m_backPanel.setImagePath("dialogs/background");
    if (!m_backPanel.isValid())
        cerr << "Back panel SVG is not valid!" << endl;

    // Get the standard plasma font
    m_labelFont = Plasma::Theme::defaultTheme()->font(Plasma::Theme::DefaultFont);
    m_labelFont.setBold(true);
    m_labelColor = Plasma::Theme::defaultTheme()->color(Plasma::Theme::TextColor);

    this->updateLayout();
}


void OSD::paintEvent(QPaintEvent*)
{
    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);

    // Draw screenshot
    if (!Plasma::Theme::defaultTheme()->windowTranslucencyEnabled())
    {
        painter.setOpacity(1.0f);
        painter.drawPixmap(0, 0, m_screenshot);
        painter.setOpacity(m_opacity);
    }

    // Draw the panel
    m_backPanel.paintFrame(&painter);

    // Draw the icon
    painter.drawPixmap(m_iconRect, m_icon);

    // Draw the label
    painter.setPen(m_labelColor);
    painter.setFont(m_labelFont);
    painter.drawText(m_labelRect, Qt::AlignCenter | Qt::TextWordWrap, m_labelText);
}

#include "osd.moc"
