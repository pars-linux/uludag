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

#ifndef SOZLUKEDITDIALOG_K_H
#define SOZLUKEDITDIALOG_K_H

#include <qdialog.h>
#include <qhgroupbox.h>
#include <qlineedit.h>
#include <qlistbox.h>
#include <qstringlist.h>
#include <qpushbutton.h>
#include <qpopupmenu.h>
#include "anapencere.h"

class editTerm:public QDialog
{
	Q_OBJECT
	public:
		editTerm(QWidget *parent = 0, const char *name = 0, TransDef *entry=0);
		QStringList *sList, *tList, *dList;
	private:
		QLineEdit *satir;
		QHGroupBox *boxSource, *boxTrans, *boxDef;
		QListBox *lSource, *lTrans, *lDef;
		QPushButton *kaydet, *iptal;
		QPushButton *bsEkle, *bsCikar, *btEkle, *btCikar, *bdEkle, *bdCikar;
	public slots:
		void sEkle();
		void tEkle();
		void dEkle();
		void sCikar();
		void tCikar();
		void dCikar();
		void listeKaydet();
};


#endif

