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
	gözlük programının ana penceresini oluşturmaktadır. 
	Arama, yeni kelime ekleme, olanları düzenleme vs. gibi
	işlemler üzerinden gerçekleştirilebilmektedir.
	
	Mayıs 2005 - Kaya Oğuz - kaya@kuzeykutbu.org

*/

#ifndef SOZLUK_KAYA_H
#define SOZLUK_KAYA_H

#include <qmainwindow.h>
#include <qlabel.h>
#include <qlineedit.h>
#include <qhbuttongroup.h>
#include <qradiobutton.h>
#include <qlistview.h>
#include <qvgroupbox.h>
#include <qpopupmenu.h>
#include <qstringlist.h>
#include <qptrlist.h>

/* transdef class, Barış Metin */

/* Translations and Definitions */
class TransDef {

public:

    void addSource( const QString s ) {
	sources.append( s);
    }
    void addTranslation( const QString t ) {
	translations.append( t );
    }
    void setDefinition( const QString d ) {
	definition = d;
    }
    QStringList getSources() const { return sources; }
    QStringList getTranslations() const { return translations; }
    QString getDefinition() const { return definition; }
    
    // güncelleme için:
    
    void temizle()
    {
    	sources.clear();
    	translations.clear();
    }
	
private:
    QStringList sources; // sources string list
    QStringList translations; // translations list
    QString definition; // definition
};



class anaPencere:public QMainWindow
{
	Q_OBJECT
	private:
		QLabel *lblKelime, *lblAnlam;
		QLineEdit *lineSatir;
		QHButtonGroup *bgroupDiller;
		QRadioButton *radioEng, *radioTur;
		QListView *lviewListe;
		QVGroupBox *gboxAnlam;
		QPopupMenu *lPopup, *menuSecenekler, *menuDosya, *menuAbout;
		bool edited;
		int edit1, edit2, sil1, sil2;
		
		QPtrList<TransDef> entries;
		TransDef *currentEntry;
		bool searchEnglish;
		
	public:
		anaPencere(QWidget *parent=0, const char *name=0);
		~anaPencere();
		
		void setEdited( bool newState )
		{ edited = newState; }
		
		bool getEdited() { return edited; }
		
	protected slots:
		void yeniKelime();
		void kelimeDuzenle();
		void seciliSil();
		void settings();
		void about();
		void exportToXml();
		void popupSag();
		
		void yeniSozluk();
		void sozlukAc();
		
		void selectionUpdate();
		
		void setCurrentSource( const QString s );
		void addCurrentTranslation( const QString t );
		void setCurrentDefinition( const QString d );
		void addEntry();
		void searchSource( const QString& );
		void showWord();
		void showFromList( QListViewItem* );
		void langChanged( bool );
		
	protected:
		void readDict(QString dictFile);
		void writeDict(const QString& dictFile);
		void closeEvent(QCloseEvent *event);
};



#endif

