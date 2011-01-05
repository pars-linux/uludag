// This file is generated by kconfig_compiler from ipv4.kcfg.
// All changes you do to this file will be lost.
#ifndef IPV4DBUS_H
#define IPV4DBUS_H

#include <nm-setting-ip4-config.h>

#include <kdebug.h>
#include <kcoreconfigskeleton.h>
#include "settingdbus.h"
#include "nm07dbus_export.h"
namespace Knm{
    class Ipv4Setting;
}

class NM07DBUS_EXPORT Ipv4Dbus : public SettingDbus
{
  public:
    Ipv4Dbus(Knm::Ipv4Setting * setting);
    ~Ipv4Dbus();
    void fromMap(const QVariantMap&);
    QVariantMap toMap();
    QVariantMap toSecretsMap();
};
#endif
