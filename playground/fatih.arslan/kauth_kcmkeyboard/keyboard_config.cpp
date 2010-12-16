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

#include "keyboard_config.h"

#include "helper.h"

#include <ksharedconfig.h>
#include <kconfiggroup.h>
#include <kdebug.h>
#include <QMessageBox>
#include <QDebug>


static const char* SWITCHING_POLICIES[] = {"Global", "Desktop", "WinClass", "Window", NULL };
static const char* LIST_SEPARATOR = ",";
//static const char* DEFAULT_LAYOUT = "us";
static const char* DEFAULT_MODEL = "pc104";

static const QString CONFIG_FILENAME("kxkbrc");
static const QString CONFIG_GROUPNAME("Layout");


static int findStringIndex(const char* strings[], const QString& toFind, int defaultIndex)
{
	for(int i=0; strings[i] != NULL; i++) {
		if( toFind == strings[i] ) {
			return i;
		}
	}
	return defaultIndex;
}

void KeyboardConfig::setDefaults()
{
	keyboardModel = DEFAULT_MODEL;
	resetOldXkbOptions = false;
	xkbOptions.clear();

	// init layouts options
	configureLayouts = false;
	layouts.clear();
//	layouts.append(LayoutUnit(DEFAULT_LAYOUT));

	// switch cotrol options
	switchingPolicy = SWITCH_POLICY_GLOBAL;
//	stickySwitching = false;
//	stickySwitchingDepth = 2;

	// display options
	showIndicator = true;
	showFlag = true;
	showSingle = false;
}


void KeyboardConfig::load()
{
    KConfigGroup config(KSharedConfig::openConfig( CONFIG_FILENAME, KConfig::NoGlobals ), CONFIG_GROUPNAME);

    keyboardModel = config.readEntry("Model", "");

    resetOldXkbOptions = config.readEntry("ResetOldOptions", false);
    QString options = config.readEntry("Options", "");
    xkbOptions = options.split(LIST_SEPARATOR, QString::SkipEmptyParts);

    configureLayouts = config.readEntry("Use", false);
    QString layoutsString = config.readEntry("LayoutList", "");
    QStringList layoutStrings = layoutsString.split(LIST_SEPARATOR, QString::SkipEmptyParts);
//    if( layoutStrings.isEmpty() ) {
//    	layoutStrings.append(DEFAULT_LAYOUT);
//    }
    layouts.clear();
    foreach(const QString& layoutString, layoutStrings) {
    	layouts.append(LayoutUnit(layoutString));
    }
    if( layouts.isEmpty() ) {
    	configureLayouts = false;
    }

	QString layoutMode = config.readEntry("SwitchMode", "Global");
	switchingPolicy = static_cast<SwitchingPolicy>(findStringIndex(SWITCHING_POLICIES, layoutMode, SWITCH_POLICY_GLOBAL));

	showIndicator = config.readEntry("ShowLayoutIndicator", true);
	showFlag = config.readEntry("ShowFlag", false);
	showSingle = config.readEntry("ShowSingle", false);

    QString labelsStr = config.readEntry("DisplayNames", "");
    QStringList labels = labelsStr.split(LIST_SEPARATOR, QString::KeepEmptyParts);
    for(int i=0; i<labels.count() && i<layouts.count(); i++) {
    	if( !labels[i].isEmpty() && labels[i] != layouts[i].layout ) {
    		layouts[i].setDisplayName(labels[i]);
    	}
    }

	kDebug() << "configuring layouts" << configureLayouts << "configuring options" << resetOldXkbOptions;
}

void KeyboardConfig::save()
{
    KConfigGroup config(KSharedConfig::openConfig( CONFIG_FILENAME, KConfig::NoGlobals ), CONFIG_GROUPNAME);

    config.writeEntry("Model", keyboardModel);

    config.writeEntry("ResetOldOptions", resetOldXkbOptions);
    if( resetOldXkbOptions ) {
    	config.writeEntry("Options", xkbOptions.join(LIST_SEPARATOR));
    }
    else {
        config.deleteEntry("Options");
    }

    config.writeEntry("Use", configureLayouts);

    QStringList layoutStrings;
    foreach(const LayoutUnit& layoutUnit, layouts) {
    	layoutStrings.append(layoutUnit.toString());
    }
    config.writeEntry("LayoutList", layoutStrings.join(LIST_SEPARATOR));

    QStringList displayNames;
    foreach(const LayoutUnit& layoutUnit, layouts) {
    	displayNames << layoutUnit.getRawDisplayName();
    }
    config.writeEntry("DisplayNames", displayNames.join(LIST_SEPARATOR));

	config.writeEntry("SwitchMode", SWITCHING_POLICIES[switchingPolicy]);

	config.writeEntry("ShowLayoutIndicator", showIndicator);
	config.writeEntry("ShowFlag", showFlag);
	config.writeEntry("ShowSingle", showSingle);

	config.sync();
}

int KeyboardConfig::saveSystemWide()
{

    KAuth::Action action("org.kde.kcontrol.kcmkeyboard.managekeyboard");
    action.setHelperID("org.kde.kcontrol.kcmkeyboard");

    QVariantMap helperargs;
    QStringList layoutList;
    QStringList variantList;

    foreach(const LayoutUnit& layoutUnit, layouts) {
    	layoutList.append(layoutUnit.layout);
    	variantList.append(layoutUnit.variant);
    }

    helperargs["layouts"] = layoutList.join(LIST_SEPARATOR);
    helperargs["variants"] = variantList.join(LIST_SEPARATOR);

    action.setArguments(helperargs);

    KAuth::ActionReply reply = action.execute();
    return reply.errorCode();
}
