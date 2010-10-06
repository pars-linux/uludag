/*
Copyright 2009 Will Stephenson <wstephenson@kde.org>

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) version 3, or any
later version accepted by the membership of KDE e.V. (or its
successor approved by the membership of KDE e.V.), which shall
act as a proxy defined in Section 6 of version 3 of the license.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library.  If not, see <http://www.gnu.org/licenses/>.
*/

#ifndef KNM_INTERNALS_SETTING_H
#define KNM_INTERNALS_SETTING_H

#include "knminternals_export.h"


namespace Knm
{

class KNMINTERNALS_EXPORT Setting
{
public:
    enum Type { Cdma, Gsm, Ipv4, Ipv6, Ppp, Pppoe, Security8021x, Serial, Vpn, Wired, Wireless, WirelessSecurity };
    static QString typeAsString(Setting::Type);
    static Setting::Type typeFromString(const QString & type);

    Setting(Setting::Type type);
    virtual ~Setting();
    bool isNull() const;
    void setInitialized();
    Setting::Type type() const;
    virtual QString name() const = 0;
    virtual bool hasSecrets() const = 0;
    bool secretsAvailable() const;
    void setSecretsAvailable(bool secretsAvailable);
protected:
    bool m_initialized;
private:
    Setting::Type m_type;
    bool m_secretsAvailable;
};

} // namespace Knm

#endif // SETTING_H
