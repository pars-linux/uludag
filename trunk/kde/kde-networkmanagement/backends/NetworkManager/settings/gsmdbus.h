// This file is generated by kconfig_compiler from gsm.kcfg.
// All changes you do to this file will be lost.
#ifndef GSMDBUS_H
#define GSMDBUS_H

#include <nm-setting-gsm.h>

#include <kdebug.h>
#include <kcoreconfigskeleton.h>
#include "settingdbus.h"
#include "nm07dbus_export.h"
namespace Knm{
    class GsmSetting;
}

class NM07DBUS_EXPORT GsmDbus : public SettingDbus
{
  public:
    GsmDbus(Knm::GsmSetting * setting);
    ~GsmDbus();
    void fromMap(const QVariantMap&);
    QVariantMap toMap();
    QVariantMap toSecretsMap();
};
#endif

