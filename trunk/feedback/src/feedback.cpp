/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <kapplication.h>
#include <klocale.h>
#include <kprocess.h>

#include <qlabel.h>
#include <qradiobutton.h>
#include <qcheckbox.h>
#include <qbuttongroup.h>
#include <qmessagebox.h>
#include <qtextedit.h>

#include "welcome.h"
#include "question.h"
#include "hardwareinfo.h"
#include "goodbye.h"

#include "feedback.h"
#include "feedback.moc"

Feedback::Feedback( QWidget *parent, const char *name )
    : KWizard( parent, name, true)
{
	setCaption( kapp->caption() );

    /* Welcome */
    welcome = new Welcome( this );
    addPage( welcome, i18n( "Welcome" ) );
    setHelpEnabled( QWizard::page( 0 ), false );
	
	/* Experience */
	experience = new Question( this, 0, i18n("Experience") );
	
    experience->questionOne->setText( i18n( "&Starter" ));
    experience->questionTwo->setText( i18n( "&User" ));
    experience->questionThree->setText( i18n( "&Poweruser" ));
	experience->questionFour->setText( i18n( "&Master of the known universe" ));

	addPage( experience, i18n( "Ease of Use" ));
    setHelpEnabled( QWizard::page( 1 ), false );
							
	/* Ease Of Use */
    ease_of_use = new Question( this, 0, i18n("Ease Of Use") );

	ease_of_use->questionOne->setText( i18n( "&Very Good" ));
    ease_of_use->questionTwo->setText( i18n( "&Good" ));
    ease_of_use->questionThree->setText( i18n( "Nice &Try" ));
    ease_of_use->questionFour->setText( i18n( "&Useless" ));
				
	addPage( ease_of_use, i18n( "Ease of Use" ));
    setHelpEnabled( QWizard::page( 2 ), false );

	/* Visual Attractiveness */
	visual_attractiveness = new Question( this, 0, "Visual Attractiveness");

    visual_attractiveness->questionOne->setText( i18n( "&Very Good" ));
    visual_attractiveness->questionTwo->setText( i18n( "&Good" ));
    visual_attractiveness->questionThree->setText( i18n( "Nice &Try" ));
    visual_attractiveness->questionFour->setText( i18n( "&Useless" ));
	
    addPage( visual_attractiveness, i18n( "Visual Attractiveness" ));
	setHelpEnabled( QWizard::page( 3 ), false );

	/* Organization/Layout */
	organization_layout = new Question( this, 0, "Organization/Layout" );

    organization_layout->questionOne->setText( i18n( "&Very Good" ));
    organization_layout->questionTwo->setText( i18n( "Could Be &Better" ));
    organization_layout->questionThree->setText( i18n( "&Optimization work should be done" ));
    organization_layout->questionFour->setText( i18n( "&Very bad" ));

    addPage( organization_layout, i18n( "Organization/Layout" ) );
    setHelpEnabled( QWizard::page( 4 ), false );

	/* Hardware Info */	
    hardwareinfo = new HardwareInfo( this );
	addPage( hardwareinfo, i18n( "Hardware Info" ) );
	setHelpEnabled( QWizard::page( 5 ), false );

	/* Goodbye */
    goodbye = new Goodbye( this );
    addPage( goodbye, i18n( "Thank You" ) );
    setHelpEnabled( QWizard::page( 6 ), false );

	/* Finish */
    setFinishEnabled( QWizard::page( 6 ), true );

    locale = new KLocale( PACKAGE );
    locale->setLanguage( KLocale::defaultLanguage() );
}

Feedback::~Feedback()
{
}

void Feedback::next()
{
	if( currentPage() == hardwareinfo && hardwareinfo->collectBox->isChecked() )
	{
		hardwareinfo->permit = true;
	}
	QWizard::next();
}

void Feedback::back()
{
    QWizard::back();
}

void Feedback::accept()
{
	/* Iterate over pages and send [ if permitted by the user ] answers to the server */
	if( hardwareinfo->permit )
	{			
	    proc = new KProcess();
	    proc->clearArguments();

	    *proc << "/home/caglar/feedback/src/grab_information";
		proc->start();

		for( int i=1; i < pageCount() - 2 ; ++i )
		{
			QMessageBox::information( this, i18n("Sent To Server"), i18n("%1").arg( dynamic_cast<Question*>( page(i) )->buttonGroup->selectedId() ));
    	}
	}
	exit(0);
}

void Feedback::reject()
{
    exit(0);
}
