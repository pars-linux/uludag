/****************************************************************************
** Form interface generated from reading ui file './packager.ui'
**
** Created: Cum Tem 22 10:30:03 2005
**      by: The User Interface Compiler ($Id: qt/main.cpp   3.3.4   edited Nov 24 2003 $)
**
** WARNING! All changes made in this file will be lost!
****************************************************************************/

#ifndef PACKAGEMANAGER_H
#define PACKAGEMANAGER_H

#include <qvariant.h>
#include <qwidget.h>

class QVBoxLayout;
class QHBoxLayout;
class QGridLayout;
class QSpacerItem;
class QPushButton;
class QLabel;
class QFrame;

class Package_Manager : public QWidget
{
    Q_OBJECT

public:
    Package_Manager( QWidget* parent = 0, const char* name = 0, WFlags fl = 0 );
    ~Package_Manager();

    QPushButton* m_listPackages;
    QPushButton* m_newPackageButton;
    QLabel* m_PardusLogo;
    QFrame* m_DisplayFrame;

protected:
    QVBoxLayout* m_buttonLayout;

protected slots:
    virtual void languageChange();

};

#endif // PACKAGEMANAGER_H
