/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef FEEDBACK_H
#define FEEDBACK_H

#include <kwizard.h>
#include <qdom.h>

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

class KLocale;
class KProcess;

class Welcome;
class Question;
class HardwareInfo;
class Goodbye;

class Feedback : public KWizard
{
    Q_OBJECT

public:
	Feedback( QWidget* parent=0, const char *name=0 );
	~Feedback();

	virtual void next();
	virtual void back();

public slots:
	virtual void accept();
	virtual void reject();

private:
	KLocale *locale;
	KProcess *proc;

	Welcome *welcome;
	Question *experience, *ease_of_use, *visual_attractiveness, *organization_layout;
	HardwareInfo *hardwareinfo;
	Goodbye *goodbye;
};

#endif // FEEDBACK_H
