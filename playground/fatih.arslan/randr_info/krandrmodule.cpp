/*
 * Copyright (c) 2007      Gustavo Pichorim Boiko <gustavo.boiko@kdemail.net>
 * Copyright (c) 2002,2003 Hamish Rodda <rodda@kde.org>
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
 */

#include "krandrmodule.h"
#include "legacyrandrconfig.h"
#include <QTextStream>
#include <QSizePolicy>
#include <QBrush>
#include "legacyrandrscreen.h"
#include "randrdisplay.h"
#include "randrconfig.h"

// X11 includes
#include <X11/Xlib.h>
#include <X11/Xutil.h>

// OpenGL includes
#include <GL/gl.h>
#include <GL/glext.h>
#include <GL/glx.h>

#include <KPluginFactory>
#include <KPluginLoader>
#include <KDebug>
#include <KIcon>
#include <KProcess>
#include <KMessageBox>
#include <KColorScheme>
#include <kdesktopfileactions.h>
#include <config-randr.h>

#include "randr.h"
#include "glinfo.h"


// DLL Interface for kcontrol
K_PLUGIN_FACTORY(KSSFactory, registerPlugin<KRandRModule>();)
K_EXPORT_PLUGIN(KSSFactory("krandr"))

KRandRModule::KRandRModule(QWidget *parent, const QVariantList&)
    : KCModule(KSSFactory::componentData(), parent)
{
	m_display = new RandRDisplay();
	if (!m_display->isValid())
	{
		QVBoxLayout *topLayout = new QVBoxLayout(this);
		
       
        QLabel *label =
		    new QLabel(i18n("Your X server does not support resizing and "
		                    "rotating the display. Please update to version 4.3 "
						"or greater. You need the X Resize, Rotate, and Reflect "
						"extension (RANDR) version 1.1 or greater to use this "
						"feature."), this);
						
		label->setWordWrap(true);
		topLayout->addWidget(label);
		kWarning() << "Error: " << m_display->errorCode() ;
		return;
	}

	QVBoxLayout* topLayout = new QVBoxLayout(this);
	topLayout->setMargin(0);
	topLayout->setSpacing(KDialog::spacingHint());

    QFrame* stateContainer = new QFrame(this);
    stateContainer->setAutoFillBackground(true);
    stateContainer->setFrameShape(QFrame::Box);
    stateContainer->setFrameShadow(QFrame::Plain); 

    topLayout->addWidget(stateContainer);

    QHBoxLayout* stateHorizontalLayout = new QHBoxLayout(stateContainer);

    QLabel* stateIconLabel = new QLabel(stateContainer);
    QSizePolicy sizePolicy(QSizePolicy::Fixed, QSizePolicy::Fixed);
    sizePolicy.setHorizontalStretch(0);
    sizePolicy.setVerticalStretch(0);
    sizePolicy.setHeightForWidth(stateIconLabel->sizePolicy().hasHeightForWidth());
    stateIconLabel->setSizePolicy(sizePolicy);
    stateIconLabel->setMinimumSize(QSize(22, 22));

    stateHorizontalLayout->addWidget(stateIconLabel);

    QLabel* stateTextLabel = new QLabel(stateContainer);
    stateTextLabel->setText(QString::fromUtf8("[current notification system information]"));
    stateTextLabel->setWordWrap(false);

    stateHorizontalLayout->addWidget(stateTextLabel);

    QPushButton* startButton = new QPushButton(stateContainer);
    stateContainer->setFixedHeight(38);

    stateHorizontalLayout->addStretch();
    stateHorizontalLayout->addWidget(startButton);

    glInfo = new GlInfo();
    glInfo->getGlStrings();

    QString vendorText;
    vendorText = glInfo->glVendor;

    QString icon = "dialog-information";
    QString text;
    text = i18n("Your graphic card's manufacturer provides a tool for these settings.\n"
                "It's recommended to use this tool. You can start it by clicking the button on the left.");

    bool showStartButton = false;
    bool nvidia = false;
    bool ati = false;

    if (vendorText.startsWith("NVIDIA")){
        nvidia = true;
        startButton->setText("Start Nvidia Settings");
        startButton->setIcon(KIcon("nvidia-settings"));
        showStartButton = true;
    }
    else if (vendorText.startsWith("ATI")){
        ati = true;
        startButton->setText("Start Ati Control Center");
        startButton->setIcon(KIcon("amdccclesu"));
        showStartButton = true;
    }

    // Adjust palette
    KColorScheme scheme(QPalette::Active, KColorScheme::Window);
    QBrush bg = scheme.background(KColorScheme::PositiveBackground);
    QBrush fg = scheme.foreground(KColorScheme::NormalText);

    stateContainer->setStyleSheet(
        QString(".QFrame {"
            "background-color: %1;"
            "border-radius: 3px;"
            "border: 1px solid %2;"
            "}"
            ".QLabel { color: %2; }"
            )
        .arg(bg.color().name())
        .arg(fg.color().name())
        );

    stateIconLabel->setPixmap(KIcon(icon).pixmap(22));
    stateTextLabel->setText(text);
    startButton->setVisible(showStartButton);

    if (nvidia || ati) {
        stateContainer->show();
        if (nvidia) {
            connect(startButton, SIGNAL(clicked(bool)), SLOT(startNvidia()));
        }
        else if (ati) {
            connect(startButton, SIGNAL(clicked(bool)), SLOT(startAti()));
        }

    }
    else {
        stateContainer->hide();
    }

#ifdef HAS_RANDR_1_2
	if (RandR::has_1_2)
	{
		m_config = new RandRConfig(this, m_display);
		connect(m_config, SIGNAL(changed(bool)), SIGNAL(changed(bool)));
		topLayout->addWidget(m_config);
	}
	else
#endif
	{
		m_legacyConfig = new LegacyRandRConfig(this, m_display);
		connect(m_legacyConfig, SIGNAL(changed(bool)), SIGNAL(changed(bool)));
		topLayout->addWidget(m_legacyConfig);
	}

	setButtons(KCModule::Apply);
}

KRandRModule::~KRandRModule(void)
{
	delete m_display;
    delete glInfo;;
}

void KRandRModule::defaults()
{

        if (!m_display->isValid()) {
                return;
        }
#ifdef HAS_RANDR_1_2
	if (RandR::has_1_2)
		m_config->defaults();
	else
#endif
		m_legacyConfig->defaults();
}

void KRandRModule::load()
{
    if (!m_display->isValid()) {
                return;
    }

#ifdef HAS_RANDR_1_2
	if (RandR::has_1_2)
		m_config->load();
	else
#endif
		m_legacyConfig->load();

	emit changed(false);
}

void KRandRModule::save()
{
        if (!m_display->isValid()) {
                return;
        }
#ifdef HAS_RANDR_1_2
	if (RandR::has_1_2)
		m_config->save();
	else
#endif
		m_legacyConfig->save();

}

void KRandRModule::apply()
{
        if (!m_display->isValid()) {
                return;
        }
#ifdef HAS_RANDR_1_2
	if (RandR::has_1_2)
		m_config->apply();
	else
#endif
		m_legacyConfig->apply();
}

void KRandRModule::startNvidia()
{

  KUrl url =  KUrl::fromPath("/usr/share/applications/nvidia-settings.desktop");
  KDesktopFileActions::run(url, true);

}

void KRandRModule::startAti()
{

  KUrl url =  KUrl::fromPath("/usr/share/applications/amdccclesu.desktop");
  KDesktopFileActions::run(url, true);

}
#include "krandrmodule.moc"
