// This file is generated by kconfig_compiler from ppp.kcfg.
// All changes you do to this file will be lost.
#ifndef KNM_PPPPERSISTENCE_H
#define KNM_PPPPERSISTENCE_H

#include <kdebug.h>
#include <kcoreconfigskeleton.h>
#include "settingpersistence.h"
#include "knminternals_export.h"
namespace Knm {

class PppSetting;

class KNMINTERNALS_EXPORT PppPersistence : public SettingPersistence
{
  public:
    PppPersistence( PppSetting * setting, KSharedConfig::Ptr config, ConnectionPersistence::SecretStorageMode mode = ConnectionPersistence::Secure);
    ~PppPersistence();
    void load();
    void save();
    QMap<QString,QString> secrets() const;
    void restoreSecrets(QMap<QString,QString>) const;
};
}

#endif

