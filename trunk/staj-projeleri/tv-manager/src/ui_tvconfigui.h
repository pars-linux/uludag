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
#include <QtGui/QGroupBox>
#include <QtGui/QHeaderView>
#include <QtGui/QLabel>
#include <QtGui/QListWidget>
#include <QtGui/QRadioButton>
#include <QtGui/QSpacerItem>
#include <QtGui/QSplitter>
#include <QtGui/QTabWidget>
#include <QtGui/QVBoxLayout>
#include <QtGui/QWidget>

QT_BEGIN_NAMESPACE

class Ui_TvConfigUI
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
    QListWidget *cardManList_2;
    QListWidget *cardModList_2;
    QWidget *tab_3;
    QVBoxLayout *verticalLayout_5;
    QVBoxLayout *verticalLayout_3;
    QSplitter *splitter;
    QGroupBox *groupBox;
    QVBoxLayout *verticalLayout_2;
    QVBoxLayout *verticalLayout;
    QRadioButton *radioButton;
    QRadioButton *radioButton_2;
    QRadioButton *radioButton_3;
    QGroupBox *groupBox_2;
    QVBoxLayout *verticalLayout_4;
    QCheckBox *checkBox;
    QSpacerItem *verticalSpacer;
    QSpacerItem *verticalSpacer_2;

    void setupUi(QWidget *TvConfigUI)
    {
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
        cardManList_2 = new QListWidget(splitter_6);
        new QListWidgetItem(cardManList_2);
        new QListWidgetItem(cardManList_2);
        cardManList_2->setObjectName(QString::fromUtf8("cardManList_2"));
        splitter_6->addWidget(cardManList_2);
        cardModList_2 = new QListWidget(splitter_6);
        new QListWidgetItem(cardModList_2);
        new QListWidgetItem(cardModList_2);
        cardModList_2->setObjectName(QString::fromUtf8("cardModList_2"));
        splitter_6->addWidget(cardModList_2);
        splitter_7->addWidget(splitter_6);

        gridLayout_3->addWidget(splitter_7, 0, 0, 1, 1);

        tvCard->addTab(tab_2, QString());
        tab_3 = new QWidget();
        tab_3->setObjectName(QString::fromUtf8("tab_3"));
        verticalLayout_5 = new QVBoxLayout(tab_3);
        verticalLayout_5->setSpacing(6);
        verticalLayout_5->setMargin(11);
        verticalLayout_5->setObjectName(QString::fromUtf8("verticalLayout_5"));
        verticalLayout_3 = new QVBoxLayout();
        verticalLayout_3->setSpacing(6);
        verticalLayout_3->setObjectName(QString::fromUtf8("verticalLayout_3"));
        splitter = new QSplitter(tab_3);
        splitter->setObjectName(QString::fromUtf8("splitter"));
        splitter->setOrientation(Qt::Horizontal);
        groupBox = new QGroupBox(splitter);
        groupBox->setObjectName(QString::fromUtf8("groupBox"));
        verticalLayout_2 = new QVBoxLayout(groupBox);
        verticalLayout_2->setSpacing(6);
        verticalLayout_2->setMargin(11);
        verticalLayout_2->setObjectName(QString::fromUtf8("verticalLayout_2"));
        verticalLayout = new QVBoxLayout();
        verticalLayout->setSpacing(6);
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        radioButton = new QRadioButton(groupBox);
        radioButton->setObjectName(QString::fromUtf8("radioButton"));

        verticalLayout->addWidget(radioButton);

        radioButton_2 = new QRadioButton(groupBox);
        radioButton_2->setObjectName(QString::fromUtf8("radioButton_2"));

        verticalLayout->addWidget(radioButton_2);

        radioButton_3 = new QRadioButton(groupBox);
        radioButton_3->setObjectName(QString::fromUtf8("radioButton_3"));

        verticalLayout->addWidget(radioButton_3);


        verticalLayout_2->addLayout(verticalLayout);

        splitter->addWidget(groupBox);
        groupBox_2 = new QGroupBox(splitter);
        groupBox_2->setObjectName(QString::fromUtf8("groupBox_2"));
        verticalLayout_4 = new QVBoxLayout(groupBox_2);
        verticalLayout_4->setSpacing(6);
        verticalLayout_4->setMargin(11);
        verticalLayout_4->setObjectName(QString::fromUtf8("verticalLayout_4"));
        checkBox = new QCheckBox(groupBox_2);
        checkBox->setObjectName(QString::fromUtf8("checkBox"));

        verticalLayout_4->addWidget(checkBox);

        verticalSpacer = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        verticalLayout_4->addItem(verticalSpacer);

        splitter->addWidget(groupBox_2);

        verticalLayout_3->addWidget(splitter);

        verticalSpacer_2 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        verticalLayout_3->addItem(verticalSpacer_2);


        verticalLayout_5->addLayout(verticalLayout_3);

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

        const bool __sortingEnabled2 = cardManList_2->isSortingEnabled();
        cardManList_2->setSortingEnabled(false);
        QListWidgetItem *___qlistwidgetitem4 = cardManList_2->item(0);
        ___qlistwidgetitem4->setText(QApplication::translate("TvConfigUI", "New Item", 0, QApplication::UnicodeUTF8));
        QListWidgetItem *___qlistwidgetitem5 = cardManList_2->item(1);
        ___qlistwidgetitem5->setText(QApplication::translate("TvConfigUI", "New Item", 0, QApplication::UnicodeUTF8));
        cardManList_2->setSortingEnabled(__sortingEnabled2);


        const bool __sortingEnabled3 = cardModList_2->isSortingEnabled();
        cardModList_2->setSortingEnabled(false);
        QListWidgetItem *___qlistwidgetitem6 = cardModList_2->item(0);
        ___qlistwidgetitem6->setText(QApplication::translate("TvConfigUI", "New Item", 0, QApplication::UnicodeUTF8));
        QListWidgetItem *___qlistwidgetitem7 = cardModList_2->item(1);
        ___qlistwidgetitem7->setText(QApplication::translate("TvConfigUI", "New Item", 0, QApplication::UnicodeUTF8));
        cardModList_2->setSortingEnabled(__sortingEnabled3);

        tvCard->setTabText(tvCard->indexOf(tab_2), QApplication::translate("TvConfigUI", "Tuner", 0, QApplication::UnicodeUTF8));
        groupBox->setTitle(QApplication::translate("TvConfigUI", "Phase Locked Loop(PLL)", 0, QApplication::UnicodeUTF8));
        radioButton->setText(QApplication::translate("TvConfigUI", "Do not use PLL", 0, QApplication::UnicodeUTF8));
        radioButton_2->setText(QApplication::translate("TvConfigUI", "28 Mhz Crystal", 0, QApplication::UnicodeUTF8));
        radioButton_3->setText(QApplication::translate("TvConfigUI", "35 Mhz Crystal", 0, QApplication::UnicodeUTF8));
        groupBox_2->setTitle(QApplication::translate("TvConfigUI", "Eklentiler", 0, QApplication::UnicodeUTF8));
        checkBox->setText(QApplication::translate("TvConfigUI", "Radyo Kart\304\261", 0, QApplication::UnicodeUTF8));
        tvCard->setTabText(tvCard->indexOf(tab_3), QApplication::translate("TvConfigUI", "Se\303\247enekler", 0, QApplication::UnicodeUTF8));
        Q_UNUSED(TvConfigUI);
    } // retranslateUi

};

namespace Ui {
    class TvConfigUI: public Ui_TvConfigUI {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_TVCONFIGUI_H
