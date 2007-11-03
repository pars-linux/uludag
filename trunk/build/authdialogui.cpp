#include <kdialog.h>
#include <klocale.h>

/****************************************************************************
** Form implementation generated from reading ui file '/home/gokcen/kits/PolicyKit-kde/authdialogui.ui'
**
** Created: Cts Kas 3 14:53:48 2007
**      by: The User Interface Compiler ($Id: qt/main.cpp   3.3.8   edited Jan 11 14:47 $)
**
** WARNING! All changes made in this file will be lost!
****************************************************************************/

#include "/home/gokcen/kits/PolicyKit-kde/build/authdialogui.h"

#include <qvariant.h>
#include <qpushbutton.h>
#include <qlabel.h>
#include <kcombobox.h>
#include <kpassdlg.h>
#include <qcheckbox.h>
#include <qlayout.h>
#include <qtooltip.h>
#include <qwhatsthis.h>

/*
 *  Constructs a AuthDialogUI as a child of 'parent', with the
 *  name 'name' and widget flags set to 'f'.
 *
 *  The dialog will by default be modeless, unless you set 'modal' to
 *  TRUE to construct a modal dialog.
 */
AuthDialogUI::AuthDialogUI( QWidget* parent, const char* name, bool modal, WFlags fl )
    : QDialog( parent, name, modal, fl )
{
    if ( !name )
	setName( "AuthDialogUI" );
    setSizeGripEnabled( FALSE );
    AuthDialogUILayout = new QGridLayout( this, 1, 1, 11, 6, "AuthDialogUILayout"); 

    layout2 = new QHBoxLayout( 0, 0, 6, "layout2"); 
    Horizontal_Spacing2 = new QSpacerItem( 267, 20, QSizePolicy::Expanding, QSizePolicy::Minimum );
    layout2->addItem( Horizontal_Spacing2 );

    pbOK = new QPushButton( this, "pbOK" );
    pbOK->setSizePolicy( QSizePolicy( (QSizePolicy::SizeType)1, (QSizePolicy::SizeType)0, 0, 0, pbOK->sizePolicy().hasHeightForWidth() ) );
    pbOK->setAutoDefault( TRUE );
    pbOK->setDefault( TRUE );
    layout2->addWidget( pbOK );

    pbCancel = new QPushButton( this, "pbCancel" );
    pbCancel->setSizePolicy( QSizePolicy( (QSizePolicy::SizeType)1, (QSizePolicy::SizeType)0, 0, 0, pbCancel->sizePolicy().hasHeightForWidth() ) );
    pbCancel->setAutoDefault( TRUE );
    layout2->addWidget( pbCancel );

    AuthDialogUILayout->addMultiCellLayout( layout2, 1, 1, 0, 1 );

    layout4 = new QVBoxLayout( 0, 0, 6, "layout4"); 

    lblPixmap = new QLabel( this, "lblPixmap" );
    layout4->addWidget( lblPixmap );
    spacer5 = new QSpacerItem( 20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding );
    layout4->addItem( spacer5 );

    AuthDialogUILayout->addLayout( layout4, 0, 0 );

    layout5 = new QVBoxLayout( 0, 0, 6, "layout5"); 

    lblHeader = new QLabel( this, "lblHeader" );
    layout5->addWidget( lblHeader );

    lblContent = new QLabel( this, "lblContent" );
    lblContent->setAlignment( int( QLabel::WordBreak | QLabel::AlignVCenter ) );
    layout5->addWidget( lblContent );

    cbUsers = new KComboBox( FALSE, this, "cbUsers" );
    layout5->addWidget( cbUsers );

    layout4_2 = new QHBoxLayout( 0, 0, 6, "layout4_2"); 

    lblPassword = new QLabel( this, "lblPassword" );
    layout4_2->addWidget( lblPassword );

    pePassword = new KPasswordEdit( this, "pePassword" );
    layout4_2->addWidget( pePassword );
    layout5->addLayout( layout4_2 );

    cbRemember = new QCheckBox( this, "cbRemember" );
    layout5->addWidget( cbRemember );

    layout4_2_2 = new QHBoxLayout( 0, 0, 6, "layout4_2_2"); 
    spacer4 = new QSpacerItem( 16, 20, QSizePolicy::Fixed, QSizePolicy::Minimum );
    layout4_2_2->addItem( spacer4 );

    cbSession = new QCheckBox( this, "cbSession" );
    cbSession->setEnabled( FALSE );
    layout4_2_2->addWidget( cbSession );
    layout5->addLayout( layout4_2_2 );

    AuthDialogUILayout->addLayout( layout5, 0, 1 );
    languageChange();
    resize( QSize(379, 211).expandedTo(minimumSizeHint()) );
    clearWState( WState_Polished );

    // signals and slots connections
    connect( pbOK, SIGNAL( clicked() ), this, SLOT( accept() ) );
    connect( pbCancel, SIGNAL( clicked() ), this, SLOT( reject() ) );
    connect( cbRemember, SIGNAL( toggled(bool) ), cbSession, SLOT( setEnabled(bool) ) );

    // tab order
    setTabOrder( pePassword, cbUsers );
    setTabOrder( cbUsers, cbRemember );
    setTabOrder( cbRemember, cbSession );
    setTabOrder( cbSession, pbOK );
    setTabOrder( pbOK, pbCancel );
}

/*
 *  Destroys the object and frees any allocated resources
 */
AuthDialogUI::~AuthDialogUI()
{
    // no need to delete child widgets, Qt does it all for us
}

/*
 *  Sets the strings of the subwidgets using the current
 *  language.
 */
void AuthDialogUI::languageChange()
{
    setCaption( tr2i18n( "Authentication Required" ) );
    pbOK->setText( tr2i18n( "&OK" ) );
    pbOK->setAccel( QKeySequence( QString::null ) );
    pbCancel->setText( tr2i18n( "&Cancel" ) );
    pbCancel->setAccel( QKeySequence( QString::null ) );
    lblPixmap->setText( tr2i18n( "Lock Icon Here" ) );
    lblHeader->setText( tr2i18n( "<h3><b>Header is here! </b></h3>" ) );
    lblContent->setText( tr2i18n( "Lorem ipsum dolor sit amet, consectetuer adipiscing elit." ) );
    lblPassword->setText( tr2i18n( "Password:" ) );
    cbRemember->setText( tr2i18n( "Remember authorization" ) );
    cbSession->setText( tr2i18n( "For this session only" ) );
}

