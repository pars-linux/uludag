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

#include "experience.h"
#include "goodbye.h"
#include "hardwareinfo.h"
#include "purpose.h"
#include "question.h"
#include "usage.h"
#include "welcome.h"
#include "opinion.h"

#include "feedback.h"
#include "feedback.moc"

Feedback::Feedback( QWidget *parent, const char *name )
    : KWizard( parent, name, true)
{
	int page_number = 0;

	setCaption( kapp->caption() );

	locale = new KLocale( PACKAGE );
	locale->setLanguage( KLocale::defaultLanguage() );

	/* Welcome Page */
	welcome = new Welcome( this );
	addPage( welcome, i18n( "Welcome " ) );
	setHelpEnabled( QWizard::page( page_number ), false );
	
	/* Experience Page */
	experience = new Experience( this, 0 );
	addPage( experience, i18n( "Your experience level" ));
	setHelpEnabled( QWizard::page( ++page_number ), false );
							
	/* Purpose Use Page */
	purpose = new Purpose( this, 0 );
	addPage( purpose, i18n( "Using Pardus" ));
	setHelpEnabled( QWizard::page( ++page_number ), false );

	/* Usage Page */
	usage = new Usage( this, 0 );
	addPage( usage, i18n( "Where do you use Pardus?" ));
	setHelpEnabled( QWizard::page( ++page_number ), false );

	/*  General Ideas Page */
	question = new Question( this, 0 );
	addPage( question, i18n( "Your ideas" ) );
	setHelpEnabled( QWizard::page( ++page_number ), false );

    /* Opinion Page */	
	opinion = new Opinion( this );
	addPage( opinion, i18n( "Your opinions" ) );
	setHelpEnabled( QWizard::page( ++page_number ), false );
    
	/* Hardware Info Page */	
	hardwareinfo = new HardwareInfo( this );
	addPage( hardwareinfo, i18n( "Collecting hardware information" ) );
	setHelpEnabled( QWizard::page( ++page_number ), false );

	/* Goodbye Page */
	goodbye = new Goodbye( this );
	addPage( goodbye, i18n( "Thank you" ) );
	setHelpEnabled( QWizard::page( ++page_number ), false );

	/* Finish */
	setFinishEnabled( QWizard::page( page_number ), true );
}

Feedback::~Feedback()
{
}

void Feedback::next()
{
	QWizard::next();
}

void Feedback::back()
{
	QWizard::back();
}

void Feedback::accept()
{
	exit(0);
}

void Feedback::reject()
{
	exit(0);
}
