/*
  Copyright (c) 2004, 2006 TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <dcopclient.h>
#include <kapplication.h>
#include <kconfig.h>
#include <kglobal.h>
#include <kipc.h>
#include <kstandarddirs.h>
#include <kstandarddirs.h>

#include <qcheckbox.h>
#include <qcombobox.h>
#include <qdom.h>
#include <qfileinfo.h>
#include <qlabel.h>
#include <qpixmap.h>
#include <qpushbutton.h>
#include <qstringlist.h>

#include "style.h"

Style::Style(QWidget *parent, const char* name)
    : StyleDlg(parent, name)
{
    // Common Pardus settings for all themes
    KConfig *config = new KConfig("kdeglobals");
    config->setGroup("KDE");
    config->writeEntry("ShowIconsOnPushButtons", true);
    config->writeEntry("EffectAnimateCombo", true);
    config->sync();
    delete config;

    // add kaptan themes into resouce pool
    KGlobal::dirs()->addResourceType("themes", KStandardDirs::kde_default("data") + "kaptan/themes/");

    QStringList themes = KGlobal::dirs()->findAllResources("themes", "*.xml", true /*recursive*/);
    themes.sort();

    for (QStringList::const_iterator it = themes.begin(); it != themes.end(); ++it)
        styleBox->insertItem(QFileInfo(*it).baseName());

    connect(styleButton, SIGNAL(clicked()), this, SLOT(testStyle()));
    connect(styleBox, SIGNAL(activated(int)), this, SLOT(styleSelected(int)));
    connect(checkKickoff, SIGNAL(clicked()), this, SLOT(kickoffSelected()));

    styleBox->setCurrentItem(0);
    emit(styleSelected(0));
}

QString Style::getProperty(QDomElement parent, const QString & tag, const QString & attr) const
{
    QDomNodeList _list = parent.elementsByTagName(tag);

    if (_list.count() != 0)
        return _list.item(0).toElement().attribute(attr);
    else
        return QString::null;
}

void Style::kickoffSelected()
{
    styleSelected(styleBox->currentItem());
}

void Style::styleSelected(int item)
{
    QString previewPath;
    QString name = styleBox->text(item);

    if (checkKickoff->isChecked())
        previewPath = KGlobal::dirs()->findResourceDir("themes", "/" ) + name + "/" + name + "_kickoff.preview.png";
    else
        previewPath = KGlobal::dirs()->findResourceDir("themes", "/" ) + name + "/" + name + ".preview.png";

    QString xmlFile = KGlobal::dirs()->findResourceDir("themes", "/" ) + name + "/" + name + ".xml";

    if (QFile::exists( previewPath))
    {
        pix_style->setPixmap(QPixmap(previewPath));
        selectedStyle = xmlFile;
    }
    else
        return;
}

void Style::testStyle()
{
    // Read entire XML into DOM Tree
    QFile file(selectedStyle);
    file.open(IO_ReadOnly);
    dom.setContent(file.readAll());
    file.close();

    // attach to dcop
    DCOPClient *client = kapp->dcopClient();
    if (!client->isAttached())
        client->attach();

    // kicker settings
    KConfig *kickerConf = new KConfig("kickerrc");
    kickerConf->setGroup("General");

    QDomElement Kicker = dom.elementsByTagName("kicker").item(0).toElement();

    kickerConf->writeEntry("LegacyKMenu", !checkKickoff->isChecked());
    kickerConf->writeEntry("Transparent", getProperty(Kicker, "Transparent", "value"));
    kickerConf->writeEntry("SizePercentage", getProperty(Kicker, "SizePercentage", "value"));
    kickerConf->writeEntry("CustomSize", getProperty(Kicker, "CustomSize", "value"));
    kickerConf->writeEntry("Position", getProperty(Kicker, "Position", "value"));
    kickerConf->writeEntry("Alignment", getProperty(Kicker, "Alignment", "value"));
    kickerConf->sync();
    delete kickerConf;

    // restart kicker
    client->send("kicker", "kicker", "restart()", "");

    // kwin settings
    KConfig *kwinConf = new KConfig("kwinrc");
    kwinConf->setGroup("Style");

    QDomElement KWin = dom.elementsByTagName("kwin").item(0).toElement();

    kwinConf->writeEntry("PluginLib", getProperty(KWin, "PluginLib", "value"));
    kwinConf->sync();
    delete kwinConf;

    // restart kwin
    client->send("kwin", "KWinInterface", "reconfigure()", "");

    // widget settings
    KConfig *globalConf = new KConfig("kdeglobals");
    globalConf->setGroup("General");

    QDomElement Widget = dom.elementsByTagName("widget").item(0).toElement();

    globalConf->writeEntry("widgetStyle", getProperty(Widget, "widgetStyle", "value"));
    globalConf->sync();
    delete globalConf;

    testedStyle= styleBox->currentItem();

    KIPC::sendMessageAll(KIPC::StyleChanged);
}

#include "style.moc"
