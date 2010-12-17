/*
  Copyright (c) 1997 Christian Czezatke (e9025461@student.tuwien.ac.at)
                1998 Bernd Wuebben <wuebben@kde.org>
                2000 Matthias Elter <elter@kde.org>
                2001 Carsten PFeiffer <pfeiffer@kde.org>

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
*/

#include <QCheckBox>
#include <QPushButton>


//Added by qt3to4:
#include <QVBoxLayout>
#include <QFormLayout>
#include <QBoxLayout>
#include <QGroupBox>

#include <kcmodule.h>
#include <kaboutdata.h>
#include <kapplication.h>
#include <kconfig.h>
#include <kdialog.h>
#include <knotification.h>
#include <klocale.h>
#include <knuminput.h>

#include "panda.h"
#include "panda.moc"

#include <X11/Xlib.h>
#include <QX11Info>
#include <kpluginfactory.h>
#include <kpluginloader.h>



K_PLUGIN_FACTORY(PandaConfigFactory, registerPlugin<PandaConfig>();)
K_EXPORT_PLUGIN(PandaConfigFactory("kcmpanda"))



extern "C"
{
  KDE_EXPORT void kcminit_panda()
  {
    XKeyboardState kbd;
    XKeyboardControl kbdc;

    XGetKeyboardControl(QX11Info::display(), &kbd);

    KConfig _config( "kcmpandarc", KConfig::NoGlobals  );
    KConfigGroup config(&_config, "General");
  }
}

PandaConfig::PandaConfig(QWidget *parent, const QVariantList &args):
    KCModule(PandaConfigFactory::componentData(), parent, args)
{
  QBoxLayout *layout = new QVBoxLayout(this);
  layout->setMargin(0);

  QGroupBox *box = new QGroupBox(i18n("Panda Settings"), this );
  QFormLayout *form = new QFormLayout();
  box->setLayout(form);
  layout->addWidget(box);

  title = new QLabel( i18n("&Make a copy of grub .. EXAMPLE" ), box );
  title->setWhatsThis( i18n("Click on question button, hover on the \"title\" Qlabel, this text will displ."));

  form->addRow(title);

  KAboutData *about =
    new KAboutData(I18N_NOOP("kcmpanda"), 0, ki18n("KDE Panda Control Module"),
                  0, KLocalizedString(), KAboutData::License_GPL,
                  ki18n("(c) 2011 Fatih Arslan"));

  about->addAuthor(ki18n("Fatih Arslan"), ki18n("Original author"), "farslan@pardus.org.tr");
  setAboutData(about);
}

void PandaConfig::load()
{
  XKeyboardState kbd;
  XGetKeyboardControl(QX11Info::display(), &kbd);

  KConfig _cfg("kdeglobals", KConfig::NoGlobals);
  KConfigGroup cfg(&_cfg, "General");
  emit changed(false);
}

void PandaConfig::save()
{
  XKeyboardControl kbd;
  XGetKeyboardControl(QX11Info::display(), &kbd);

  KConfig _config("kcmbellrc", KConfig::NoGlobals);
  KConfigGroup config(&_config, "General");
  config.writeEntry("Volume",bellVolume);
  config.writeEntry("Pitch",bellPitch);
  config.writeEntry("Duration",bellDuration);

  config.sync();

  KConfig _cfg("kdeglobals", KConfig::NoGlobals);
  KConfigGroup cfg(&_cfg, "General");
  cfg.writeEntry("UseSystemBell", m_useBell->isChecked());
  cfg.sync();

  if (!m_useBell->isChecked())
  {
    KConfig config("kaccessrc");

    KConfigGroup group = config.group("Bell");
    group.writeEntry("SystemBell", false);
    group.writeEntry("ArtsBell", false);
    group.writeEntry("VisibleBell", false);
  }
}


void PandaConfig::defaults()
{
  m_volume->setValue(100);
  m_pitch->setValue(800);
  m_duration->setValue(100);
  m_useBell->setChecked( false );
}

