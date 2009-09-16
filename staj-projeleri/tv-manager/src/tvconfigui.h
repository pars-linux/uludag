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
#include <QObject>
#include <QtGui/QRadioButton>
#include <QtGui/QSpacerItem>
#include <QtGui/QSplitter>
#include <QtGui/QTabWidget>
#include <QtGui/QVBoxLayout>
#include <QtGui/QHBoxLayout>
#include <QtGui/QPushButton>
#include <QtGui/QDialogButtonBox>
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
    QLabel *tunerManufacturer;
    QLabel *tunerModel;
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
    QVBoxLayout *pllLayout;
    QVBoxLayout *tab3Layout;
    QVBoxLayout *addOnsLayout;
    QDialogButtonBox *buttonBox;
    QPushButton *applyButton;
    QPushButton *reDefaultButton;

    TvConfigUI(QWidget *parent = 0);
    ~TvConfigUI();
};


QT_END_NAMESPACE

#endif // UI_TVCONFIGUI_H
