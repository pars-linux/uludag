/*
Copyright 2010 Lamarque Souza <lamarque@gmail.com>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 2 of
the License or (at your option) version 3 or any later version
accepted by the membership of KDE e.V. (or its successor approved
by the membership of KDE e.V.), which shall act as a proxy
defined in Section 14 of version 3 of the license.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#ifndef MOBILECONNECTIONWIZARD_H
#define MOBILECONNECTIONWIZARD_H

#include <QWizardPage>
#include <QComboBox>
#include <QListWidget>
#include <QRadioButton>
#include <QLabel>

#include <solid/control/networkmanager.h>

#include "mobileproviders.h"

class MobileConnectionWizard : public QWizard
{
Q_OBJECT
public:
    MobileConnectionWizard(QWidget * parent = 0);
    ~MobileConnectionWizard();

    /*
     * Returns the information to configure one connection from the last wizard run.
     * The format is:
     * for GSM connections: provider's name + QList of Gsm NetworkIds for that provider (can be an empty QList) + QMap with apn information
     * where apn information is: dial number + apn + apn name (optional) + username (optional) + password (optional) + QList of name servers (optional)
     *
     * for CDMA connections: provider's name + QMap with cdma information.
     * where cdma information is: name (optional) + username (optional) + password (optional) + list of sids (optional)
     */
    QVariantList args();

private Q_SLOTS:
    void introDeviceAdded(const QString uni);
    void introDeviceRemoved(const QString uni);
    void introStatusChanged(Solid::Networking::Status);
    void slotEnablePlanEditBox(const QString & text);
    void slotEnableProviderEdit(bool enable);
    void slotCheckProviderEdit();

private:
    QWizardPage * createIntroPage();
    QWizardPage * createCountryPage();
    QWizardPage * createProvidersPage();
    QWizardPage * createPlansPage();
    QWizardPage * createConfirmPage();
    void initializePage(int id);
    int nextId() const;

    MobileProviders * mProviders;
    Solid::Control::NetworkInterface * mIface;
    QString getCountryFromLocale();
    QString country;
    QString provider;
    QString apn;

    // Intro page
    QComboBox * mDeviceComboBox;
    void introAddInitialDevices();
    void introRemoveAllDevices();
    void introAddDevice(Solid::Control::NetworkInterface *device);

    // Country page
    QListWidget * mCountryList;

    // Providers page
    QListWidget * mProvidersList;
    QRadioButton * radioAutoProvider;
    QRadioButton * radioManualProvider;
    QLineEdit * lineEditProvider;
    QComboBox * mType;

    // Plan page
    QComboBox * mPlanComboBox;
    QLineEdit * userApn;

    // Confirm page
    QLabel * labelProvider;
    QLabel * labelPlanLabel;
    QLabel * labelPlan;
    QLabel * labelApn;
};
#endif
