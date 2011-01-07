// This file is generated by kconfig_compiler from 802-3-ethernet.kcfg.
// All changes you do to this file will be lost.

#include "802-3-ethernetdbus.h"

#include "802-3-ethernet.h"

WiredDbus::WiredDbus(Knm::WiredSetting * setting) : SettingDbus(setting)
{
}

WiredDbus::~WiredDbus()
{
}

void WiredDbus::fromMap(const QVariantMap & map)
{
  Knm::WiredSetting * setting = static_cast<Knm::WiredSetting *>(m_setting);
  if (map.contains("port")) {
    setting->setPort(map.value("port").value<int>());
  }
  if (map.contains("speed")) {
    setting->setSpeed(map.value("speed").value<uint>());
  }
  if (map.contains("duplex")) {
    setting->setDuplex(map.value("duplex").value<int>());
  }
  if (map.contains(QLatin1String(NM_SETTING_WIRED_AUTO_NEGOTIATE))) {
    setting->setAutonegotiate(map.value(QLatin1String(NM_SETTING_WIRED_AUTO_NEGOTIATE)).value<bool>());
  }
  if (map.contains(QLatin1String(NM_SETTING_WIRED_MAC_ADDRESS))) {
    setting->setMacaddress(map.value(QLatin1String(NM_SETTING_WIRED_MAC_ADDRESS)).value<QByteArray>());
  }
  if (map.contains("mtu")) {
    setting->setMtu(map.value("mtu").value<uint>());
  }
}

QVariantMap WiredDbus::toMap()
{
  QVariantMap map;
  Knm::WiredSetting * setting = static_cast<Knm::WiredSetting *>(m_setting);
// not in UI yet
#if 0
  switch (setting->port()) {
    case Knm::WiredSetting::EnumPort::tp:
      map.insert("port", "tp");
      break;
    case Knm::WiredSetting::EnumPort::aui:
      map.insert("port", "aui");
      break;
    case Knm::WiredSetting::EnumPort::bnc:
      map.insert("port", "bnc");
      break;
    case Knm::WiredSetting::EnumPort::mii:
      map.insert("port", "mii");
      break;
  }
  map.insert("speed", setting->speed());
  switch (setting->duplex()) {
    case Knm::WiredSetting::EnumDuplex::half:
      map.insert("duplex", "half");
      break;
    case Knm::WiredSetting::EnumDuplex::full:
      map.insert("duplex", "full");
      break;
  }
  map.insert(QLatin1String(NM_SETTING_WIRED_AUTO_NEGOTIATE), setting->autonegotiate());
#endif
  // broken
  //QString mac = setting->macaddress();
  //map.insert(QLatin1String(NM_SETTING_WIRED_MAC_ADDRESS), mac.remove(':').toAscii());
  if (setting->mtu() > 0 ) {
    map.insert("mtu", setting->mtu());
  }
  return map;
}

QVariantMap WiredDbus::toSecretsMap()
{
  QVariantMap map;
  return map;
}
