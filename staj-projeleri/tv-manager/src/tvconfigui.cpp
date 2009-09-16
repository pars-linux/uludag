#include <iostream>
#include "tvconfigui.h"

TvConfigUI::TvConfigUI(QWidget *parent) : QWidget(parent)
{
    resize(600, 400);
    mainLayout = new QGridLayout(this);
    tvCard = new QTabWidget(this);
    tab = new QWidget();
    gridLayout = new QGridLayout(tab);
    cardManufacturer = new QLabel();
    gridLayout->addWidget(cardManufacturer, 0, 0);
    cardModel = new QLabel();
    gridLayout->addWidget(cardModel, 0, 1);
    cardManList = new QListWidget();
    gridLayout->addWidget(cardManList, 1, 0);
    cardModList = new QListWidget();
    gridLayout->addWidget(cardModList, 1, 1);

    tvCard->addTab(tab, QString());
    tab_2 = new QWidget();
    tab_2->setObjectName(QString::fromUtf8("tab_2"));
    gridLayout_3 = new QGridLayout(tab_2);
    gridLayout_3->setObjectName(QString::fromUtf8("gridLayout_3"));
    tunerManufacturer = new QLabel();
    tunerManufacturer->setObjectName(QString::fromUtf8("tunerManufacturer"));
    gridLayout_3->addWidget(tunerManufacturer, 0, 0);
    tunerModel = new QLabel();
    tunerModel->setObjectName(QString::fromUtf8("tunerModel"));
    gridLayout_3->addWidget(tunerModel, 0, 1);
    tunerManList = new QListWidget();
    tunerManList->setObjectName(QString::fromUtf8("tunerManList"));
    gridLayout_3->addWidget(tunerManList, 1, 0);
    tunerModList = new QListWidget();
    tunerModList->setObjectName(QString::fromUtf8("tunerModList"));
    gridLayout_3->addWidget(tunerModList, 1, 1);

    tvCard->addTab(tab_2, QString());
    tab_3 = new QWidget();
    tab_3->setObjectName(QString::fromUtf8("tab_3"));
    pllGroupBox = new QGroupBox(tab_3);
    addOnsGroupBox = new QGroupBox(tab_3);
    pllGroup = new QButtonGroup(pllGroupBox);
    pllButton = new QRadioButton(pllGroupBox);

    pllGroup->addButton(pllButton);

    mhz28Button = new QRadioButton(pllGroupBox);
    mhz28Button->setObjectName(QString::fromUtf8("mhz28Button"));
    pllGroup->addButton(mhz28Button);

    mhz35Button = new QRadioButton(pllGroupBox);
    mhz35Button->setObjectName(QString::fromUtf8("mhz35Button"));
    pllGroup->addButton(mhz35Button);
    pllLayout = new QVBoxLayout;
    pllLayout->addWidget(pllButton);
    pllLayout->addWidget(mhz28Button);
    pllLayout->addWidget(mhz35Button);
    pllLayout->addStretch();
    pllGroupBox->setLayout(pllLayout);

    addOnsGroup = new QButtonGroup(addOnsGroupBox);
    radioCard = new QCheckBox(addOnsGroupBox);
    addOnsGroup->setExclusive(false);
    addOnsGroup->addButton(radioCard);
    addOnsLayout = new QVBoxLayout;
    addOnsLayout->addWidget(radioCard);
    addOnsLayout->addStretch();
    addOnsGroupBox->setLayout(addOnsLayout);

    tab3Layout = new QVBoxLayout(tab_3);
    tab3Layout->addWidget(pllGroupBox);
    tab3Layout->addWidget(addOnsGroupBox);

    tvCard->addTab(tab_3, QString());

    tvCard->setCurrentIndex(0);

    reDefaultButton = new QPushButton(tr("Restore Defaults"));
    applyButton = new QPushButton(tr("Apply"));
    applyButton->setDefault(true);

    
    buttonBox = new QDialogButtonBox(Qt::Horizontal, tab_3);
    buttonBox->addButton(reDefaultButton, QDialogButtonBox::ActionRole);
    buttonBox->addButton(applyButton, QDialogButtonBox::ActionRole);

    mainLayout->addWidget(tvCard, 0, 0, 1, 1);
    mainLayout->addWidget(buttonBox, 1, 0, 1, 1);

    QMetaObject::connectSlotsByName(this);

    cardManufacturer->setText(QObject::tr("Manufacturer"));
    cardModel->setText(QObject::tr("Model"));

    const bool __sortingEnabled = cardManList->isSortingEnabled();
    cardManList->setSortingEnabled(false);
    cardManList->setSortingEnabled(__sortingEnabled);

    const bool __sortingEnabled1 = cardModList->isSortingEnabled();
    cardModList->setSortingEnabled(false);
    cardModList->setSortingEnabled(__sortingEnabled1);

    tvCard->setTabText(tvCard->indexOf(tab), QObject::tr("Tv Card"));
    tunerManufacturer->setText(QObject::tr("Manufacturer"));
    tunerModel->setText(QObject::tr("Model"));

    const bool __sortingEnabled2 = tunerManList->isSortingEnabled();
    tunerManList->setSortingEnabled(false);
    tunerManList->setSortingEnabled(__sortingEnabled2);

    const bool __sortingEnabled3 = tunerModList->isSortingEnabled();
    tunerModList->setSortingEnabled(false);
    tunerModList->setSortingEnabled(__sortingEnabled3);

    tvCard->setTabText(tvCard->indexOf(tab_2), QObject::tr("Tuner"));
    pllGroupBox->setTitle(QObject::tr("Phase Locked Loop (PLL)"));
    pllButton->setText(QObject::tr("Do not use PLL"));
    mhz28Button->setText(QObject::tr("28 Mhz Crystal"));
    mhz35Button->setText(QObject::tr("35 Mhz Crystal"));
    addOnsGroupBox->setTitle(QObject::tr("Addons"));
    radioCard->setText(QObject::tr("Radio Card"));
    tvCard->setTabText(tvCard->indexOf(tab_3), QObject::tr("Options"));
}

TvConfigUI::~TvConfigUI()
{
}
