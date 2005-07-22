#include <kdialog.h>
#include <klocale.h>
/****************************************************************************
** Form implementation generated from reading ui file './packager.ui'
**
** Created: Cum Tem 22 10:30:07 2005
**      by: The User Interface Compiler ($Id: qt/main.cpp   3.3.4   edited Nov 24 2003 $)
**
** WARNING! All changes made in this file will be lost!
****************************************************************************/

#include "packager.h"

#include <qvariant.h>
#include <qpushbutton.h>
#include <qlabel.h>
#include <qframe.h>
#include <qlayout.h>
#include <qtooltip.h>
#include <qwhatsthis.h>

/*
 *  Constructs a Package_Manager as a child of 'parent', with the
 *  name 'name' and widget flags set to 'f'.
 */
Package_Manager::Package_Manager( QWidget* parent, const char* name, WFlags fl )
    : QWidget( parent, name, fl )
{
    if ( !name )
	setName( "PackageManager" );

    QWidget* privateLayoutWidget = new QWidget( this, "m_buttonLayout" );
    privateLayoutWidget->setGeometry( QRect( 450, 110, 114, 70 ) );
    m_buttonLayout = new QVBoxLayout( privateLayoutWidget, 11, 6, "m_buttonLayout"); 

    m_listPackages = new QPushButton( privateLayoutWidget, "m_listPackages" );
    m_buttonLayout->addWidget( m_listPackages );

    m_newPackageButton = new QPushButton( privateLayoutWidget, "m_newPackageButton" );
    m_buttonLayout->addWidget( m_newPackageButton );

    m_PardusLogo = new QLabel( this, "m_PardusLogo" );
    m_PardusLogo->setGeometry( QRect( 30, 10, 501, 61 ) );

    m_DisplayFrame = new QFrame( this, "m_DisplayFrame" );
    m_DisplayFrame->setGeometry( QRect( 30, 100, 401, 341 ) );
    m_DisplayFrame->setFrameShape( QFrame::StyledPanel );
    m_DisplayFrame->setFrameShadow( QFrame::Plain );
    languageChange();
    resize( QSize(600, 465).expandedTo(minimumSizeHint()) );
    clearWState( WState_Polished );
}

/*
 *  Destroys the object and frees any allocated resources
 */
Package_Manager::~Package_Manager()
{
    // no need to delete child widgets, Qt does it all for us
}

/*
 *  Sets the strings of the subwidgets using the current
 *  language.
 */
void Package_Manager::languageChange()
{
    setCaption( tr2i18n( "PackageManager" ) );
    m_listPackages->setText( tr2i18n( "&Paketleri Listele" ) );
    m_listPackages->setAccel( QKeySequence( tr2i18n( "Alt+P" ) ) );
    m_newPackageButton->setText( tr2i18n( "&Yeni Paket Yükle" ) );
    m_newPackageButton->setAccel( QKeySequence( tr2i18n( "Alt+Y" ) ) );
    m_PardusLogo->setText( tr2i18n( "<center><h1>Pardus Logo Buraya</h1></center>" ) );
}

#include "packager.moc"
