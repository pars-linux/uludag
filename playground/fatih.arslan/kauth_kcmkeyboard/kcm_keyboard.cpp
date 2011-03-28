/*
 *  Copyright (C) 2010 Andriy Rysin (rysin@kde.org)
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


#include "kcm_keyboard.h"

#include <kdebug.h>
#include <kaboutdata.h>
#include <kpluginfactory.h>
#include <kpluginloader.h>
#include <kmessagebox.h>

#include <QtDBus/QDBusMessage>
#include <QtDBus/QDBusConnection>
//#include <QtDBus/QDBusInterface>

#include "kcm_keyboard_widget.h"
#include "x11_helper.h"
#include "keyboard_config.h"
#include "xkb_rules.h"
#include "keyboard_dbus.h"

#include "xkb_helper.h"

//temp hack
#include "kcmmisc.h"


K_PLUGIN_FACTORY(KeyboardModuleFactory, registerPlugin<KCMKeyboard>();)
K_EXPORT_PLUGIN(KeyboardModuleFactory("kcmkeyboard"))

KCMKeyboard::KCMKeyboard(QWidget *parent, const QVariantList &/*args*/)
  : KCModule(KeyboardModuleFactory::componentData(), parent/*, name*/)
{
  KGlobal::locale()->insertCatalog("kxkb");
  KGlobal::locale()->insertCatalog("kcmmisc");

  KAboutData *about =
		  new KAboutData("kcmkeyboard", 0, ki18n("KDE Keyboard Control Module"),
                  0, KLocalizedString(), KAboutData::License_GPL,
                  ki18n("(c) 2010 Andriy Rysin"));

  setAboutData( about );
  setQuickHelp( i18n("<h1>Keyboard</h1> This control module can be used to configure keyboard"
    " parameters and layouts."));


  rules = Rules::readRules();

  keyboardConfig = new KeyboardConfig();

  systemWide = new QCheckBox(i18n("Save settings system &wide"));

  QVBoxLayout *layout = new QVBoxLayout(this);
  layout->setMargin(0);
  layout->setSpacing(KDialog::spacingHint());

  widget = new KCMKeyboardWidget(rules, keyboardConfig, componentData(), parent);
  layout->addWidget(widget);
  layout->addWidget(systemWide);

  connect(widget, SIGNAL(changed(bool)), this, SIGNAL(changed(bool)));

#ifdef DEFAULT_TAB
  widget->setCurrentIndex(DEFAULT_TAB);
#endif

  setButtons(Help|Default|Apply);
}

KCMKeyboard::~KCMKeyboard()
{
	delete keyboardConfig;
	delete rules;
}

void KCMKeyboard::defaults()
{
	keyboardConfig->setDefaults();
	widget->updateUI();
	widget->getKcmMiscWidget()->defaults();
	emit changed(true);
}

void KCMKeyboard::load()
{
	keyboardConfig->load();
	widget->updateUI();
	widget->getKcmMiscWidget()->load();
}

//static void initializeKeyboardSettings();
void KCMKeyboard::save()
{
	keyboardConfig->save();
	widget->save();
	widget->getKcmMiscWidget()->save();

	QDBusMessage message = QDBusMessage::createSignal(KEYBOARD_DBUS_OBJECT_PATH, KEYBOARD_DBUS_SERVICE_NAME, KEYBOARD_DBUS_CONFIG_RELOAD_MESSAGE);
    QDBusConnection::sessionBus().send(message);

    if (systemWide->isChecked()) {
        int replyErrorCode = keyboardConfig->saveSystemWide();
        if (replyErrorCode != 0)
            KMessageBox::error(this, i18n("KAuth returned an error code: %1", replyErrorCode));
    };




//    initializeKeyboardSettings();
}

//static const char* KEYBOARD_KDED_NAME = "keyboard";
//
//static void initializeKeyboardSettings()
//{
//	init_keyboard_hardware();
//
//	KeyboardConfig config;
//	config.load();
//
//	// start daemon if we're configured or there's more than one layout currently
//	QDBusInterface dbus_iface("org.kde.kded", "/kded");
//	if( config.configureLayouts || X11Helper::getLayoutsList().size() > 1 ) {
//		bool started = dbus_iface.call("loadModule", KEYBOARD_KDED_NAME).arguments().at(0).toBool();
//		if( ! started ) {
//			kError() << "Failed to start keyboard daemon";
//		}
//	}
//	else {
//		// initialize keyboard model and xkb options as daemon won't be there to do it
//		XkbHelper::initializeKeyboardLayouts();
//	}

	// daemon now always starts by itself
	// start/stop kded_keyboard from here if needed
//    QDBusInterface dbus_iface("org.kde.kded", "/kded");
//    bool daemonRunning = dbus_iface.call("loadedModules").arguments().at(0).toStringList().contains(KEYBOARD_KDED_NAME);
//    if( config.configureLayouts ) {
//    	if( ! daemonRunning ) {
//    		bool started = dbus_iface.call("loadModule", KEYBOARD_KDED_NAME).arguments().at(0).toBool();
//    		kDebug() << "keyboard daemon started" << started;
//    	}
//    	else {
//    		// initialize keyboard model and xkb options as daemon won't be there to do it
//    		XkbHelper::initializeKeyboardLayouts();
//    	}
//    }
//    else {
//    	if( daemonRunning ) {
//    		bool stopped = dbus_iface.call("unloadModule", KEYBOARD_KDED_NAME).arguments().at(0).toBool();
//    		kDebug() << "keyboard daemon stopped" << stopped;
//    	}
//    }
//}
//
//extern "C"
//{
//	KDE_EXPORT void kcminit_keyboard()
//	{
//		initializeKeyboardSettings();
//	}
//}
