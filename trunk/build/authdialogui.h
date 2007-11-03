/****************************************************************************
** Form interface generated from reading ui file '/home/gokcen/kits/PolicyKit-kde/authdialogui.ui'
**
** Created: Cts Kas 3 14:53:48 2007
**      by: The User Interface Compiler ($Id: qt/main.cpp   3.3.8   edited Jan 11 14:47 $)
**
** WARNING! All changes made in this file will be lost!
****************************************************************************/

#ifndef AUTHDIALOGUI_H
#define AUTHDIALOGUI_H

#include <qvariant.h>
#include <qdialog.h>

class QVBoxLayout;
class QHBoxLayout;
class QGridLayout;
class QSpacerItem;
class QPushButton;
class QLabel;
class KComboBox;
class KPasswordEdit;
class QCheckBox;

class AuthDialogUI : public QDialog
{
    Q_OBJECT

public:
    AuthDialogUI( QWidget* parent = 0, const char* name = 0, bool modal = FALSE, WFlags fl = 0 );
    ~AuthDialogUI();

    QPushButton* pbOK;
    QPushButton* pbCancel;
    QLabel* lblPixmap;
    QLabel* lblHeader;
    QLabel* lblContent;
    KComboBox* cbUsers;
    QLabel* lblPassword;
    KPasswordEdit* pePassword;
    QCheckBox* cbRemember;
    QCheckBox* cbSession;

protected:
    QGridLayout* AuthDialogUILayout;
    QHBoxLayout* layout2;
    QSpacerItem* Horizontal_Spacing2;
    QVBoxLayout* layout4;
    QSpacerItem* spacer5;
    QVBoxLayout* layout5;
    QHBoxLayout* layout4_2;
    QHBoxLayout* layout4_2_2;
    QSpacerItem* spacer4;

protected slots:
    virtual void languageChange();

};

#endif // AUTHDIALOGUI_H
