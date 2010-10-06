
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

#include <QLineEdit>
#include <QVBoxLayout>

#include <KLocale>
#include <KDebug>
#include <KGlobal>
#include <KIconLoader>
#ifdef COMPILE_MODEM_MANAGER_SUPPORT
#include <solid/control/modemmanager.h>
#endif

#include "mobileconnectionwizard.h"

MobileConnectionWizard::MobileConnectionWizard(QWidget * parent): QWizard(parent), mType(0), mPlanComboBox(0), mCountryList(0), mProvidersList(0), userApn(0), mProviders(0)
{
    mProviders = new MobileProviders();
    setWindowTitle(i18nc("Mobile Connection Wizard", "New Mobile Broadband Connection"));
    addPage(createIntroPage());
    addPage(createCountryPage());
    addPage(createProvidersPage());
    addPage(createPlansPage());
    addPage(createConfirmPage());
    setOptions(QWizard::NoBackButtonOnStartPage);
}

MobileConnectionWizard::~MobileConnectionWizard()
{
}

void MobileConnectionWizard::initializePage(int id)
{
    switch (id) {
        case 1: // Country Page
            //QString country = KGlobal::locale()->country();
            if (country.isEmpty()) {
                country = mProviders->countryFromLocale();
            }
            if (country.isEmpty())
                mCountryList->setCurrentRow(0);
            else {
                QList<QListWidgetItem *> items = mCountryList->findItems(mProviders->getCountryName(country), Qt::MatchExactly);
                if (!items.empty()) {
                    mCountryList->setCurrentItem(items.at(0));
                }
            }
            break;

        case 2: // Providers Page
            country = mCountryList->currentItem()->text();
            mProvidersList->clear();
            lineEditProvider->setText("");
            radioAutoProvider->setChecked(true);
    
            mIface = Solid::Control::NetworkManager::findNetworkInterface(mDeviceComboBox->itemData(mDeviceComboBox->currentIndex()).toString());
            if (mIface) {
                switch (mIface->type()) {
                    case Solid::Control::NetworkInterface::Gsm:
                        mProvidersList->insertItems(0, mProviders->getProvidersList(country, Solid::Control::NetworkInterface::Gsm));
                        break;
                    case Solid::Control::NetworkInterface::Cdma:
                        mProvidersList->insertItems(0, mProviders->getProvidersList(country, Solid::Control::NetworkInterface::Cdma));
                        break;
                    case Solid::Control::NetworkInterface::UnknownType:
                        if (!mType)
                            mType = new QComboBox();
    
                        mType->addItem(i18nc("Mobile Connection Wizard", "My provider uses GSM technology (GPRS, EDGE, UMTS, HSPA)"), Solid::Control::NetworkInterface::Gsm);
                        mType->addItem(i18nc("Mobile Connection Wizard", "My provider uses CDMA technology (1xRTT, EVDO)"), Solid::Control::NetworkInterface::Cdma);
                        mType->setCurrentIndex(0);
                        page(id)->layout()->addWidget(mType);
                        break;
                    default:
                        break;
                }
            }
            mProvidersList->setCurrentRow(0);
            mProvidersList->setFocus();
            break;

        case 3: // Plans Page
            mPlanComboBox->clear();
            if (mIface->type() != Solid::Control::NetworkInterface::Gsm) {
                break;
            }
            if (radioManualProvider->isChecked()) {
                mPlanComboBox->insertSeparator(1);
                mPlanComboBox->addItem(i18nc("Mobile Connection Wizard", "My plan is not listed..."));
                mPlanComboBox->setCurrentIndex(1);
                userApn->setText("");
            } else {
                QStringList mApns = mProviders->getApns(mProvidersList->currentItem()->text());
                mPlanComboBox->insertItems(0, mApns);
                mPlanComboBox->setItemText(0, i18nc("Mobile Connection Wizard", "Default"));
                mPlanComboBox->insertSeparator(1);
                mPlanComboBox->addItem(i18nc("Mobile Connection Wizard", "My plan is not listed..."));
    
                userApn->setText(mApns.at(0));
            }
        break;

        case 4: // Confirm Page
            if (radioManualProvider->isChecked()) {
                labelProvider->setText("    " + lineEditProvider->text() + ", " + country);
                provider = lineEditProvider->text();
            } else {
                labelProvider->setText("    " + mProvidersList->currentItem()->text() + ", " + country);
                provider = mProvidersList->currentItem()->text();
            }
    
            if (mIface && mIface->type() == Solid::Control::NetworkInterface::Cdma) {
                labelPlanLabel->hide();
                labelPlan->hide();
                labelApn->hide();
                userApn->setText("");
                apn = "";
            } else {
                labelPlanLabel->show();
                labelPlan->show();
                labelApn->show();
    
                if (mPlanComboBox->currentText() == i18nc("Mobile Connection Wizard", "My plan is not listed...")) {
                    labelPlan->setText("    " + userApn->text());
                    labelApn->setText("    " + i18nc("Mobile Connection Wizard", "APN") + ": " + userApn->text());
                    apn = userApn->text();
                } else {
                    int i = mPlanComboBox->currentIndex();
                    i = i > 1 ? (i-1) : 0; // ignores separator's index (i == 1).
    
                    QStringList mApns = mProviders->getApns(mProvidersList->currentItem()->text());
                    labelPlan->setText("    " + mPlanComboBox->currentText());
                    labelApn->setText("    " + i18nc("Mobile Connection Wizard", "APN") + ": " + mApns.at(i));
                    apn = mApns.at(i);
                }
            }
            break;
    }
}

int MobileConnectionWizard::nextId() const
{
    // Providers page
    if (currentId() == 2 && mIface && mIface->type() != Solid::Control::NetworkInterface::Gsm) {
        // Jumps to Confirm page instead of Plans page if type != Gsm.
        return 4;
    } else {
        return QWizard::nextId();
    }
}

QVariantList MobileConnectionWizard::args()
{
    QVariantList temp;

    if (mIface) {
        switch (mIface->type()) {
            case Solid::Control::NetworkInterface::Cdma:
                temp << provider << mProviders->getCdmaInfo(provider);
                break;
    
            case Solid::Control::NetworkInterface::Gsm:
                temp << provider << mProviders->getNetworkIds(provider) << mProviders->getApnInfo(apn);
                break;

            default:
                break;
        }
    }
    return temp;
}

/**********************************************************/
/* Intro page */
/**********************************************************/

QWizardPage * MobileConnectionWizard::createIntroPage()
{
    QWizardPage *page = new QWizardPage();
    page->setTitle(i18nc("Mobile Connection Wizard", "Set up a Mobile Broadband Connection"));
    QVBoxLayout *layout = new QVBoxLayout;

    QLabel *label = new QLabel(i18nc("Mobile Connection Wizard", "This assistant helps you easily set up a mobile broadband connection to a cellular (3G) network."));
    label->setWordWrap(true);
    layout->addWidget(label);

    label = new QLabel("\n" + i18nc("Mobile Connection Wizard", "You will need the following information:"));
    layout->addWidget(label);

    label = new QLabel(QString("  . %1\n  . %2\n  . %3").
                                    arg(i18nc("Mobile Connection Wizard", "Your broadband provider's name")).
                                    arg(i18nc("Mobile Connection Wizard", "Your broadband billing plan name")).
                                    arg(i18nc("Mobile Connection Wizard", "(in some cases) Your broadband billing plan APN (Access Point Name)")));
    layout->addWidget(label);

    label = new QLabel("\n" + i18nc("Mobile Connection Wizard", "Create a connection for &this mobile broadband device:"));
    layout->addWidget(label);

    mDeviceComboBox = new QComboBox();
    mDeviceComboBox->addItem(i18nc("Mobile Connection Wizard", "Any device"));
    mDeviceComboBox->insertSeparator(1);
    label->setBuddy(mDeviceComboBox);
    layout->addWidget(mDeviceComboBox);

    QObject::connect(Solid::Control::NetworkManager::notifier(), SIGNAL(networkInterfaceAdded(const QString)),
                     this, SLOT(introDeviceAdded(const QString)));
    QObject::connect(Solid::Control::NetworkManager::notifier(), SIGNAL(networkInterfaceRemoved(const QString)),
                     this, SLOT(introDeviceRemoved(const QString)));
    QObject::connect(Solid::Control::NetworkManager::notifier(), SIGNAL(statusChanged(Solid::Networking::Status)),
                     this, SLOT(introStatusChanged(Solid::Networking::Status)));

    introAddInitialDevices();

    page->setLayout(layout);

    return page;
}

void MobileConnectionWizard::introAddDevice(Solid::Control::NetworkInterface *device)
{
    QString desc;

#ifdef COMPILE_MODEM_MANAGER_SUPPORT
    Solid::Control::ModemInterface *modem = Solid::Control::ModemManager::findModemInterface(device->udi(), Solid::Control::ModemInterface::GsmCard);
    if (modem) {
        if (!modem->enabled()) {
            modem->enable(true);
        }

        /* By default polkit allows only root to enable devices. */
        if (modem->enabled()) {
            desc.append(modem->getInfo().manufacturer);
            desc.append(" ");
            desc.append(modem->getInfo().model);
        }
    }
#endif

    if (device->type() == Solid::Control::NetworkInterface::Gsm) {
        if (desc.isEmpty()) {
            desc.append(i18nc("Mobile Connection Wizard", "Installed GSM device"));    
        }
    } else if (device->type() == Solid::Control::NetworkInterface::Cdma) {
        if (desc.isEmpty()) {
            desc.append(i18nc("Mobile Connection Wizard", "Installed CDMA device"));    
        }
    } else {
        return;
    }

    mDeviceComboBox->addItem(desc, device->uni());

    if (mDeviceComboBox->count() == 2) {
        mDeviceComboBox->setCurrentIndex(0);
        mDeviceComboBox->setEnabled(false);
    } else {
        mDeviceComboBox->setCurrentIndex(2);
        mDeviceComboBox->setEnabled(true);
    }
}

void MobileConnectionWizard::introDeviceAdded(const QString uni)
{
    introAddDevice(Solid::Control::NetworkManager::findNetworkInterface(uni));
}

void MobileConnectionWizard::introDeviceRemoved(const QString uni)
{
    int index = mDeviceComboBox->findData(uni);

    mDeviceComboBox->removeItem(index);

    if (mDeviceComboBox->count() == 2) {
        mDeviceComboBox->setCurrentIndex(0);
        mDeviceComboBox->setEnabled(false);
        if (currentId() > 0) {
            close();
        }
    } else {
        mDeviceComboBox->setCurrentIndex(2);
        mDeviceComboBox->setEnabled(true);
    }
}

void MobileConnectionWizard::introStatusChanged(Solid::Networking::Status status)
{
    switch (status) {
        case Solid::Networking::Unknown:
        case Solid::Networking::Unconnected:
        case Solid::Networking::Disconnecting:
            introRemoveAllDevices();
            break;
        case Solid::Networking::Connecting:
        case Solid::Networking::Connected:
            introAddInitialDevices();
            break;
    }
}

void MobileConnectionWizard::introAddInitialDevices()
{
    foreach(Solid::Control::NetworkInterface *n, Solid::Control::NetworkManager::networkInterfaces()) {
        introAddDevice(n);
    }

    if (mDeviceComboBox->count() == 2) {
        mDeviceComboBox->setCurrentIndex(0);
        mDeviceComboBox->setEnabled(false);
    } else {
        mDeviceComboBox->setCurrentIndex(2);
        mDeviceComboBox->setEnabled(true);
    }
}

void MobileConnectionWizard::introRemoveAllDevices()
{
    mDeviceComboBox->clear();
    mDeviceComboBox->addItem(i18nc("Mobile Connection Wizard", "Any device"));
    mDeviceComboBox->insertSeparator(1);
    mDeviceComboBox->setCurrentIndex(0);
    mDeviceComboBox->setEnabled(false);
}

/**********************************************************/
/* Country page */
/**********************************************************/

QWizardPage * MobileConnectionWizard::createCountryPage()
{
    QWizardPage *page = new QWizardPage();
    page->setTitle(i18nc("Mobile Connection Wizard", "Choose your Provider's Country"));
    QVBoxLayout *layout = new QVBoxLayout;

    QLabel *label = new QLabel(i18nc("Mobile Connection Wizard", "Country List:"));
    layout->addWidget(label);

    mCountryList = new QListWidget();
    mCountryList->addItem(i18nc("Mobile Connection Wizard", "My country is not listed"));
    mCountryList->insertItems(1, mProviders->getCountryList());
    layout->addWidget(mCountryList);

    page->setLayout(layout);

    return page;
}

/**********************************************************/
/* Providers page */
/**********************************************************/

QWizardPage * MobileConnectionWizard::createProvidersPage()
{
    QWizardPage *page = new QWizardPage();
    page->setTitle(i18nc("Mobile Connection Wizard", "Choose your Provider"));
    QVBoxLayout *layout = new QVBoxLayout;

    radioAutoProvider = new QRadioButton(i18nc("Mobile Connection Wizard", "Select your provider from a &list:"));
    radioAutoProvider->setChecked(true);
    layout->addWidget(radioAutoProvider);

    mProvidersList = new QListWidget();
    layout->addWidget(mProvidersList);

    radioManualProvider = new QRadioButton(i18nc("Mobile Connection Wizard", "I can't find my provider and I wish to enter it &manually:"));
    layout->addWidget(radioManualProvider);
    connect(radioManualProvider, SIGNAL(toggled(bool)), this, SLOT(slotEnableProviderEdit(bool)));

    lineEditProvider = new QLineEdit();
    layout->addWidget(lineEditProvider);
    connect(lineEditProvider, SIGNAL(textEdited(const QString)), this, SLOT(slotCheckProviderEdit()));

    page->setLayout(layout);

    return page;
}

void MobileConnectionWizard::slotEnableProviderEdit(bool checked)
{
    if (checked) {
        lineEditProvider->setFocus();
    } else {
        mProvidersList->setFocus();
    }
}

void MobileConnectionWizard::slotCheckProviderEdit()
{
    radioManualProvider->setChecked(true);
}

/**********************************************************/
/* Plan page */
/**********************************************************/

QWizardPage * MobileConnectionWizard::createPlansPage()
{
    QWizardPage *page = new QWizardPage();
    page->setTitle(i18nc("Mobile Connection Wizard", "Choose your Billing Plan"));
    QBoxLayout *layout = new QBoxLayout(QBoxLayout::TopToBottom);

    QLabel *label = new QLabel(i18nc("Mobile Connection Wizard", "&Select your plan:"));
    layout->addWidget(label);

    mPlanComboBox = new QComboBox();
    label->setBuddy(mPlanComboBox);
    connect(mPlanComboBox, SIGNAL(currentIndexChanged(const QString &)), this, SLOT(slotEnablePlanEditBox(const QString &)));
    layout->addWidget(mPlanComboBox);

    label = new QLabel("\n" + i18nc("Mobile Connection Wizard", "Selected plan &APN (Access Point Name):"));
    layout->addWidget(label);

    userApn = new QLineEdit();
    userApn->setEnabled(false);
    label->setBuddy(userApn);
    layout->addWidget(userApn);

    QHBoxLayout *layout2 = new QHBoxLayout();
    label = new QLabel();
    label->setPixmap(KIconLoader::global()->loadIcon("dialog-warning", KIconLoader::Dialog));
    layout2->addWidget(label, 0, Qt::AlignTop);
    label = new QLabel(i18nc("Mobile Connection Wizard", "Warning: Selecting an incorrect plan may result in billing issues for your broadband account or may prevent connectivity.\n\nIf you are unsure of your plan please ask your provider for your plan's APN."));
    label->setWordWrap(true);
    layout2->addWidget(label);
    layout->addWidget(new QLabel(""));
    layout->addLayout(layout2);

     page->setLayout(layout);

    return page;
}

void MobileConnectionWizard::slotEnablePlanEditBox(const QString & text)
{
    if (mIface->type() != Solid::Control::NetworkInterface::Gsm) {
        return;
    }
    if (text == "My plan is not listed...") {
        userApn->setText("");
        userApn->setEnabled(true);
    } else {
        QStringList mApns = mProviders->getApns(mProvidersList->currentItem()->text());
        userApn->setText(mApns.at(0));
        userApn->setEnabled(false);
    }
}

/**********************************************************/
/* Confirm page */
/**********************************************************/

QWizardPage * MobileConnectionWizard::createConfirmPage()
{
    QWizardPage *page = new QWizardPage();
    page->setTitle(i18nc("Mobile Connection Wizard", "Confirm Mobile Broadband Settings"));
    QVBoxLayout *layout = new QVBoxLayout;

    QLabel *label = new QLabel(i18nc("Mobile Connection Wizard", "Your mobile broadband connection is configured with the following settings:"));
    label->setWordWrap(true);
    layout->addWidget(label);

    label = new QLabel("\n" + i18nc("Mobile Connection Wizard", "Your Provider:"));
    layout->addWidget(label);
    labelProvider = new QLabel();
    layout->addWidget(labelProvider);

    labelPlanLabel = new QLabel("\n" + i18nc("Mobile Connection Wizard", "Your Plan:"));
    layout->addWidget(labelPlanLabel);
    labelPlan = new QLabel();
    layout->addWidget(labelPlan);
    labelApn = new QLabel();
    labelApn->setEnabled(false);
    layout->addWidget(labelApn);

    page->setLayout(layout);

    return page;
}
