/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

/*
	Bu pencere nedir?
	yeni bir term eklemek için gerekli pencere...
	
	Mayıs 2005 - Kaya Oğuz - kaya@kuzeykutbu.org

*/


#ifndef SOZLUKTERMDIALOG_K_H
#define SOZLUKTERMDIALOG_K_H

#include <qdialog.h>
#include <qvgroupbox.h>
#include <qlineedit.h>
#include <qlistbox.h>
#include <qstringlist.h>
#include <qpushbutton.h>
#include <qpopupmenu.h>

class newTerm:public QDialog
{
	Q_OBJECT
	public:
		newTerm(QWidget *parent = 0, const char *name = 0);
		QStringList *sList, *tList, *dList;
	private:
		QLineEdit *ySource, *yTrans, *yDef;
		QVGroupBox *boxSource, *boxTrans, *boxDef;
		QListBox *lSource, *lTrans, *lDef;
		QPushButton *kaydet, *iptal;
		QPopupMenu *sSil, *tSil, *dSil;
	public slots:
		void sPopup();
		void tPopup();
		void dPopup(); 
		void sEkle();
		void tEkle();
		void dEkle();
		void sCikar();
		void tCikar();
		void dCikar();
		void listeKaydet();
};


#endif

