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

#include <QRadioButton>
#include <QPushButton>
#include <QLabel>

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
#include <kdebug.h>


// X11 includes
#include <X11/Xlib.h>
#include <X11/Xutil.h>

// OpenGL includes
#include <GL/gl.h>
#include <GL/glext.h>
#include <GL/glx.h>




#include <QX11Info>
#include <kpluginfactory.h>
#include <kpluginloader.h>

#include "panda.h"
#include "panda.moc"

static struct glinfo {
      const char *glVendor;
      const char *glRenderer;
      const char *glVersion;
} gli;

K_PLUGIN_FACTORY(PandaConfigFactory, registerPlugin<PandaConfig>();)
K_EXPORT_PLUGIN(PandaConfigFactory("kcmpanda"))


extern "C"
{
  KDE_EXPORT void kcminit_panda()
  {

    KConfig _config( "kcmpandarc", KConfig::NoGlobals  );
    KConfigGroup config(&_config, "General");
  }
}

PandaConfig::PandaConfig(QWidget *parent, const QVariantList &args):
    KCModule(PandaConfigFactory::componentData(), parent, args)
{
  GLXContext ctx;
  char *displayName = NULL;
  int scrnum = 0;

  const int attribSingle[] = {
    GLX_RGBA,
    GLX_RED_SIZE, 1,
    GLX_GREEN_SIZE, 1,
    GLX_BLUE_SIZE, 1,
    None };
  const int attribDouble[] = {
    GLX_RGBA,
    GLX_RED_SIZE, 1,
    GLX_GREEN_SIZE, 1,
    GLX_BLUE_SIZE, 1,
    GLX_DOUBLEBUFFER,
    None };

  Display *dpy = XOpenDisplay(displayName);
  unsigned long mask;
  XVisualInfo *visinfo;
  Window root, win;
  XSetWindowAttributes attr;

  root = DefaultRootWindow(dpy);

  visinfo = glXChooseVisual(dpy, scrnum, const_cast<int*>(attribSingle));
  if (!visinfo) {
     visinfo = glXChooseVisual(dpy, scrnum, const_cast<int*>(attribDouble));
     if (!visinfo) {
       kDebug() << "Error: couldn't find RGB GLX visual\n";
       return ;
     }
  }

  attr.colormap = XCreateColormap(dpy, root, visinfo->visual, AllocNone);
  attr.event_mask = StructureNotifyMask | ExposureMask;
  mask = CWBackPixel | CWBorderPixel | CWColormap | CWEventMask;
  win = XCreateWindow(dpy, root, 0, 0, 600, 600, 0, visinfo->depth, InputOutput, visinfo->visual, mask, &attr);

  ctx = glXCreateContext( dpy, visinfo, NULL, GL_TRUE);

  if (glXMakeCurrent(dpy, win, ctx)) {
    gli.glVendor = (const char *) glGetString(GL_VENDOR);
    gli.glRenderer = (const char *) glGetString(GL_RENDERER);
    gli.glVersion = (const char *) glGetString(GL_VERSION);
  }

  // TODO: Debug lines, should be removed at release
  fprintf(stderr, "vendor: %s\n", glGetString(GL_VENDOR));
  fprintf(stderr, "renderer: %s\n", glGetString(GL_RENDERER));
  fprintf(stderr, "version: %s\n", glGetString(GL_VERSION));

  // The Main Layout, on top of this are two groupboxes, topBox and bottomBox
  QBoxLayout *layout = new QVBoxLayout(this);
  layout->setMargin(0);

  // Current Driver Information
  QGroupBox *topBox = new QGroupBox(i18n("Current Driver Information"), this );

  QGridLayout *infoLayout = new QGridLayout(this);
  infoLayout->setAlignment(Qt::AlignTop|Qt::AlignLeft);
  infoLayout->setSpacing(10);

  topBox->setLayout(infoLayout);
  layout->addWidget(topBox);

  QLabel *iconLabel = new QLabel();
  iconLabel->setAlignment(Qt::AlignCenter);
  iconLabel->setSizePolicy(QSizePolicy::Maximum, QSizePolicy::Maximum);
  iconLabel->setPixmap(KIcon("hwinfo").pixmap(64));

  QFont bFont;
  bFont.setBold(true);

  QLabel *vendorLabel = new QLabel();
  vendorLabel->setFont(bFont);
  vendorLabel->setText(i18n("Vendor:"));
  QLabel *vendorNameLabel = new QLabel();
  vendorNameLabel->setText(gli.glVendor);
  vendorNameLabel->setIndent(10);

  QLabel *rendererLabel = new QLabel();
  rendererLabel->setFont(bFont);
  rendererLabel->setText(i18n("Renderer:"));
  QLabel *rendererNameLabel = new QLabel();
  rendererNameLabel->setText(gli.glRenderer);
  rendererNameLabel->setIndent(10);

  QLabel *versionLabel = new QLabel();
  versionLabel->setFont(bFont);
  versionLabel->setText(i18n("Version:"));
  QLabel *versionNameLabel = new QLabel();
  versionNameLabel->setText(gli.glVersion);
  versionNameLabel->setIndent(10);

  infoLayout->addWidget(iconLabel,1,1,3,1,Qt::AlignCenter);

  infoLayout->addWidget(vendorLabel,1,2,1,1);
  infoLayout->addWidget(vendorNameLabel,1,3,1,1);

  infoLayout->addWidget(rendererLabel,2,2,1,1);
  infoLayout->addWidget(rendererNameLabel,2,3,1,1);

  infoLayout->addWidget(versionLabel,3,2,1,1);
  infoLayout->addWidget(versionNameLabel,3,3,1,1);

  // Driver Settings
  QGroupBox *bottomGroupBox = new QGroupBox(i18n("Driver Preferencies"), this );
  QVBoxLayout *layout_settings = new QVBoxLayout();
  bottomGroupBox->setLayout(layout_settings);
  layout->addWidget(bottomGroupBox);

  QRadioButton *osDriver = new QRadioButton("Use Open Source Driver ... EXAMPLE");
  layout_settings->addWidget(osDriver);

  QRadioButton *vendorDriver = new QRadioButton("Use Driver from the Vendor itself ... EXAMPLE");
  layout_settings->addWidget(vendorDriver);

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
}


void PandaConfig::defaults()
{
}

