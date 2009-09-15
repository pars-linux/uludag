/********************************************************************************
** Form generated from reading ui file 'tvconfigui.ui'
**
** Created: Wed Sep 2 16:24:44 2009
**      by: Qt User Interface Compiler version 4.5.2
**
** WARNING! All changes made in this file will be lost when recompiling ui file!
********************************************************************************/

#ifndef UI_TVCONFIGUI_H
#define UI_TVCONFIGUI_H

#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtGui/QApplication>
#include <QtGui/QButtonGroup>
#include <QtGui/QCheckBox>
#include <QtGui/QGridLayout>
#include <QtGui/QButtonGroup>
#include <QtGui/QHeaderView>
#include <QtGui/QLabel>
#include <QtGui/QListWidget>
#include <QtGui/QRadioButton>
#include <QtGui/QSpacerItem>
#include <QtGui/QSplitter>
#include <QtGui/QTabWidget>
#include <QtGui/QVBoxLayout>
#include <QtGui/QWidget>
#include <QtGui/QGroupBox>
#include <iostream>

QT_BEGIN_NAMESPACE

// class Ui_TvConfigUI
class TvConfigUI : public QWidget
{
public:
    QGridLayout *mainLayout;
    QTabWidget *tvCard;
    QWidget *tab;
    QGridLayout *gridLayout;
    QLabel *cardManufacturer;
    QLabel *cardModel;
    QListWidget *cardManList;
    QListWidget *cardModList;
    QWidget *tab_2;
    QGridLayout *gridLayout_3;
    QLabel *cardManufacturer_2;
    QLabel *cardModel_2;
    QListWidget *tunerManList;
    QListWidget *tunerModList;
    QWidget *tab_3;
    QButtonGroup *pllGroup;
    QVBoxLayout *verticalLayout;
    QRadioButton *pllButton;
    QRadioButton *mhz28Button;
    QRadioButton *mhz35Button;
    QButtonGroup *addOnsGroup;
    QCheckBox *radioCard;
    QGroupBox *pllGroupBox;
    QGroupBox *addOnsGroupBox;
    QSpacerItem *verticalSpacer;
    QSpacerItem *verticalSpacer_2;
    QVBoxLayout *pllLayout;
    QVBoxLayout *tab3Layout;
    QVBoxLayout *addOnsLayout;

    TvConfigUI(QWidget *parent = 0);
    ~TvConfigUI();

    void setupUi(QWidget *TvConfigUI)
    {
        int i = 0;
        std::cout << "Hello from setupUi " << ++i << std::endl;
        if (TvConfigUI->objectName().isEmpty())
            TvConfigUI->setObjectName(QString::fromUtf8("TvConfigUI"));
        TvConfigUI->resize(600, 400);
        mainLayout = new QGridLayout(TvConfigUI);
        mainLayout->setObjectName(QString::fromUtf8("mainLayout"));
        tvCard = new QTabWidget(TvConfigUI);
        tvCard->setObjectName(QString::fromUtf8("tvCard"));
        tab = new QWidget();
        tab->setObjectName(QString::fromUtf8("tab"));
        gridLayout = new QGridLayout(tab);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        cardManufacturer = new QLabel();
        cardManufacturer->setObjectName(QString::fromUtf8("cardManufacturer"));
        gridLayout->addWidget(cardManufacturer, 0, 0);
        cardModel = new QLabel();
        cardModel->setObjectName(QString::fromUtf8("cardModel"));
        gridLayout->addWidget(cardModel, 0, 1);
        cardManList = new QListWidget();
        cardManList->setObjectName(QString::fromUtf8("cardManList"));
        gridLayout->addWidget(cardManList, 1, 0);
        cardModList = new QListWidget();
        cardModList->setObjectName(QString::fromUtf8("cardModList"));
        gridLayout->addWidget(cardModList, 1, 1);

        tvCard->addTab(tab, QString());
        tab_2 = new QWidget();
        tab_2->setObjectName(QString::fromUtf8("tab_2"));
        gridLayout_3 = new QGridLayout(tab_2);
        gridLayout_3->setObjectName(QString::fromUtf8("gridLayout_3"));
        cardManufacturer_2 = new QLabel();
        cardManufacturer_2->setObjectName(QString::fromUtf8("cardManufacturer_2"));
        gridLayout_3->addWidget(cardManufacturer_2, 0, 0);
        cardModel_2 = new QLabel();
        cardModel_2->setObjectName(QString::fromUtf8("cardModel_2"));
        gridLayout_3->addWidget(cardModel_2, 0, 1);
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
        pllGroupBox->setTitle("Phase Locked Loop (PLL)");
        addOnsGroupBox = new QGroupBox("Addons", tab_3);
        pllGroup = new QButtonGroup(pllGroupBox);
        pllGroup->setObjectName(QString::fromUtf8("pllGroup"));
        pllButton = new QRadioButton(pllGroupBox);
        pllButton->setObjectName(QString::fromUtf8("pllButton"));

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
        pllGroupBox->setLayout(pllLayout);

        addOnsGroup = new QButtonGroup(addOnsGroupBox);
        addOnsGroup->setObjectName(QString::fromUtf8("addOnsGroup"));
        radioCard = new QCheckBox(addOnsGroupBox);
        radioCard->setObjectName(QString::fromUtf8("radioCard"));
        addOnsGroup->setExclusive(false);
        addOnsGroup->addButton(radioCard);
        addOnsLayout = new QVBoxLayout;
        addOnsLayout->addWidget(radioCard);
        addOnsGroupBox->setLayout(addOnsLayout);

        tab3Layout = new QVBoxLayout(tab_3);
        tab3Layout->addWidget(pllGroupBox);
        tab3Layout->addWidget(addOnsGroupBox);


        verticalSpacer = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);


        tvCard->addTab(tab_3, QString());

        mainLayout->addWidget(tvCard, 0, 0, 1, 1);


        retranslateUi(TvConfigUI);

        tvCard->setCurrentIndex(1);


        QMetaObject::connectSlotsByName(TvConfigUI);
    } // setupUi

    void retranslateUi(QWidget *TvConfigUI)
    {
        TvConfigUI->setWindowTitle(QApplication::translate("TvConfigUI", "TvConfigUI", 0, QApplication::UnicodeUTF8));
        cardManufacturer->setText(QApplication::translate("TvConfigUI", "\303\234retici", 0, QApplication::UnicodeUTF8));
        cardModel->setText(QApplication::translate("TvConfigUI", "Model", 0, QApplication::UnicodeUTF8));

        const bool __sortingEnabled = cardManList->isSortingEnabled();
        cardManList->setSortingEnabled(false);
        cardManList->setSortingEnabled(__sortingEnabled);


        const bool __sortingEnabled1 = cardModList->isSortingEnabled();
        cardModList->setSortingEnabled(false);
        cardModList->setSortingEnabled(__sortingEnabled1);

        tvCard->setTabText(tvCard->indexOf(tab), QApplication::translate("TvConfigUI", "TV Kart\304\261", 0, QApplication::UnicodeUTF8));
        cardManufacturer_2->setText(QApplication::translate("TvConfigUI", "\303\234retici", 0, QApplication::UnicodeUTF8));
        cardModel_2->setText(QApplication::translate("TvConfigUI", "Model", 0, QApplication::UnicodeUTF8));

        const bool __sortingEnabled2 = tunerManList->isSortingEnabled();
        tunerManList->setSortingEnabled(false);
        tunerManList->setSortingEnabled(__sortingEnabled2);


        const bool __sortingEnabled3 = tunerModList->isSortingEnabled();
        tunerModList->setSortingEnabled(false);
        tunerModList->setSortingEnabled(__sortingEnabled3);

        tvCard->setTabText(tvCard->indexOf(tab_2), QApplication::translate("TvConfigUI", "Tuner", 0, QApplication::UnicodeUTF8));
        // pllGroup->setTitle(QApplication::translate("TvConfigUI", "Phase Locked Loop(PLL)", 0, QApplication::UnicodeUTF8));
        pllButton->setText(QApplication::translate("TvConfigUI", "Do not use PLL", 0, QApplication::UnicodeUTF8));
        mhz28Button->setText(QApplication::translate("TvConfigUI", "28 Mhz Crystal", 0, QApplication::UnicodeUTF8));
        mhz35Button->setText(QApplication::translate("TvConfigUI", "35 Mhz Crystal", 0, QApplication::UnicodeUTF8));
        // addOnsGroup->setTitle(QApplication::translate("TvConfigUI", "Eklentiler", 0, QApplication::UnicodeUTF8));
         radioCard->setText(QApplication::translate("TvConfigUI", "Radyo Kart\304\261", 0, QApplication::UnicodeUTF8));
        tvCard->setTabText(tvCard->indexOf(tab_3), QApplication::translate("TvConfigUI", "Se\303\247enekler", 0, QApplication::UnicodeUTF8));
        Q_UNUSED(TvConfigUI);
    } // retranslateUi

};


QT_END_NAMESPACE

#endif // UI_TVCONFIGUI_H
