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
    QGridLayout *gridLayout_2;
    QTabWidget *tvCard;
    QWidget *tab;
    QGridLayout *gridLayout;
    QSplitter *splitter_4;
    QSplitter *splitter_2;
    QLabel *cardManufacturer;
    QLabel *cardModel;
    QSplitter *splitter_3;
    QListWidget *cardManList;
    QListWidget *cardModList;
    QWidget *tab_2;
    QGridLayout *gridLayout_3;
    QSplitter *splitter_7;
    QSplitter *splitter_5;
    QLabel *cardManufacturer_2;
    QLabel *cardModel_2;
    QSplitter *splitter_6;
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
    QGroupBox *groupBox;
    QSpacerItem *verticalSpacer;
    QSpacerItem *verticalSpacer_2;

    TvConfigUI(QWidget *parent = 0);
    ~TvConfigUI();

    void setupUi(QWidget *TvConfigUI)
    {
        std::cout << "Hello from setupUi" << std::endl;
        if (TvConfigUI->objectName().isEmpty())
            TvConfigUI->setObjectName(QString::fromUtf8("TvConfigUI"));
        TvConfigUI->resize(600, 400);
        gridLayout_2 = new QGridLayout(TvConfigUI);
        gridLayout_2->setSpacing(6);
        gridLayout_2->setMargin(11);
        gridLayout_2->setObjectName(QString::fromUtf8("gridLayout_2"));
        tvCard = new QTabWidget(TvConfigUI);
        tvCard->setObjectName(QString::fromUtf8("tvCard"));
        tab = new QWidget();
        tab->setObjectName(QString::fromUtf8("tab"));
        gridLayout = new QGridLayout(tab);
        gridLayout->setSpacing(6);
        gridLayout->setMargin(11);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        splitter_4 = new QSplitter(tab);
        splitter_4->setObjectName(QString::fromUtf8("splitter_4"));
        splitter_4->setOrientation(Qt::Vertical);
        splitter_2 = new QSplitter(splitter_4);
        splitter_2->setObjectName(QString::fromUtf8("splitter_2"));
        splitter_2->setOrientation(Qt::Horizontal);
        cardManufacturer = new QLabel(splitter_2);
        cardManufacturer->setObjectName(QString::fromUtf8("cardManufacturer"));
        splitter_2->addWidget(cardManufacturer);
        cardModel = new QLabel(splitter_2);
        cardModel->setObjectName(QString::fromUtf8("cardModel"));
        splitter_2->addWidget(cardModel);
        splitter_4->addWidget(splitter_2);
        splitter_3 = new QSplitter(splitter_4);
        splitter_3->setObjectName(QString::fromUtf8("splitter_3"));
        splitter_3->setOrientation(Qt::Horizontal);
        cardManList = new QListWidget(splitter_3);
        new QListWidgetItem(cardManList);
        new QListWidgetItem(cardManList);
        cardManList->setObjectName(QString::fromUtf8("cardManList"));
        splitter_3->addWidget(cardManList);
        cardModList = new QListWidget(splitter_3);
        new QListWidgetItem(cardModList);
        new QListWidgetItem(cardModList);
        cardModList->setObjectName(QString::fromUtf8("cardModList"));
        splitter_3->addWidget(cardModList);
        splitter_4->addWidget(splitter_3);

        gridLayout->addWidget(splitter_4, 0, 0, 1, 1);

        tvCard->addTab(tab, QString());
        tab_2 = new QWidget();
        tab_2->setObjectName(QString::fromUtf8("tab_2"));
        gridLayout_3 = new QGridLayout(tab_2);
        gridLayout_3->setSpacing(6);
        gridLayout_3->setMargin(11);
        gridLayout_3->setObjectName(QString::fromUtf8("gridLayout_3"));
        splitter_7 = new QSplitter(tab_2);
        splitter_7->setObjectName(QString::fromUtf8("splitter_7"));
        splitter_7->setOrientation(Qt::Vertical);
        splitter_5 = new QSplitter(splitter_7);
        splitter_5->setObjectName(QString::fromUtf8("splitter_5"));
        splitter_5->setOrientation(Qt::Horizontal);
        cardManufacturer_2 = new QLabel(splitter_5);
        cardManufacturer_2->setObjectName(QString::fromUtf8("cardManufacturer_2"));
        splitter_5->addWidget(cardManufacturer_2);
        cardModel_2 = new QLabel(splitter_5);
        cardModel_2->setObjectName(QString::fromUtf8("cardModel_2"));
        splitter_5->addWidget(cardModel_2);
        splitter_7->addWidget(splitter_5);
        splitter_6 = new QSplitter(splitter_7);
        splitter_6->setObjectName(QString::fromUtf8("splitter_6"));
        splitter_6->setOrientation(Qt::Horizontal);
        tunerManList = new QListWidget(splitter_6);
        new QListWidgetItem(tunerManList);
        new QListWidgetItem(tunerManList);
        tunerManList->setObjectName(QString::fromUtf8("tunerManList"));
        splitter_6->addWidget(tunerManList);
        tunerModList = new QListWidget(splitter_6);
        new QListWidgetItem(tunerModList);
        new QListWidgetItem(tunerModList);
        tunerModList->setObjectName(QString::fromUtf8("tunerModList"));
        splitter_6->addWidget(tunerModList);
        splitter_7->addWidget(splitter_6);

        gridLayout_3->addWidget(splitter_7, 0, 0, 1, 1);

        tvCard->addTab(tab_2, QString());
        tab_3 = new QWidget();
        tab_3->setObjectName(QString::fromUtf8("tab_3"));
        groupBox = new QGroupBox(tab_3);
        pllGroup = new QButtonGroup();
        pllGroup->setObjectName(QString::fromUtf8("pllGroup"));
        pllButton = new QRadioButton(groupBox);
        pllButton->setObjectName(QString::fromUtf8("pllButton"));

        pllGroup->addButton(pllButton);

        mhz28Button = new QRadioButton(groupBox);
        mhz28Button->setObjectName(QString::fromUtf8("mhz28Button"));
        pllGroup->addButton(mhz28Button);


        mhz35Button = new QRadioButton(groupBox);
        mhz35Button->setObjectName(QString::fromUtf8("mhz35Button"));
        pllGroup->addButton(mhz35Button);

        addOnsGroup = new QButtonGroup();
        addOnsGroup->setObjectName(QString::fromUtf8("addOnsGroup"));
        radioCard = new QCheckBox();
        radioCard->setObjectName(QString::fromUtf8("radioCard"));
        addOnsGroup->addButton(radioCard);


        verticalSpacer = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);


        tvCard->addTab(tab_3, QString());

        gridLayout_2->addWidget(tvCard, 0, 0, 1, 1);


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
        QListWidgetItem *___qlistwidgetitem = cardManList->item(0);
        ___qlistwidgetitem->setText(QApplication::translate("TvConfigUI", "New Item", 0, QApplication::UnicodeUTF8));
        QListWidgetItem *___qlistwidgetitem1 = cardManList->item(1);
        ___qlistwidgetitem1->setText(QApplication::translate("TvConfigUI", "New Item", 0, QApplication::UnicodeUTF8));
        cardManList->setSortingEnabled(__sortingEnabled);


        const bool __sortingEnabled1 = cardModList->isSortingEnabled();
        cardModList->setSortingEnabled(false);
        QListWidgetItem *___qlistwidgetitem2 = cardModList->item(0);
        ___qlistwidgetitem2->setText(QApplication::translate("TvConfigUI", "New Item", 0, QApplication::UnicodeUTF8));
        QListWidgetItem *___qlistwidgetitem3 = cardModList->item(1);
        ___qlistwidgetitem3->setText(QApplication::translate("TvConfigUI", "New Item", 0, QApplication::UnicodeUTF8));
        cardModList->setSortingEnabled(__sortingEnabled1);

        tvCard->setTabText(tvCard->indexOf(tab), QApplication::translate("TvConfigUI", "TV Kart\304\261", 0, QApplication::UnicodeUTF8));
        cardManufacturer_2->setText(QApplication::translate("TvConfigUI", "\303\234retici", 0, QApplication::UnicodeUTF8));
        cardModel_2->setText(QApplication::translate("TvConfigUI", "Model", 0, QApplication::UnicodeUTF8));

        const bool __sortingEnabled2 = tunerManList->isSortingEnabled();
        tunerManList->setSortingEnabled(false);
        QListWidgetItem *___qlistwidgetitem4 = tunerManList->item(0);
        ___qlistwidgetitem4->setText(QApplication::translate("TvConfigUI", "New Item", 0, QApplication::UnicodeUTF8));
        QListWidgetItem *___qlistwidgetitem5 = tunerManList->item(1);
        ___qlistwidgetitem5->setText(QApplication::translate("TvConfigUI", "New Item", 0, QApplication::UnicodeUTF8));
        tunerManList->setSortingEnabled(__sortingEnabled2);


        const bool __sortingEnabled3 = tunerModList->isSortingEnabled();
        tunerModList->setSortingEnabled(false);
        QListWidgetItem *___qlistwidgetitem6 = tunerModList->item(0);
        ___qlistwidgetitem6->setText(QApplication::translate("TvConfigUI", "New Item", 0, QApplication::UnicodeUTF8));
        QListWidgetItem *___qlistwidgetitem7 = tunerModList->item(1);
        ___qlistwidgetitem7->setText(QApplication::translate("TvConfigUI", "New Item", 0, QApplication::UnicodeUTF8));
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
