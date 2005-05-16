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

#include <qmenubar.h>
#include <qpopupmenu.h>
#include <qfiledialog.h>
#include <qlayout.h>
#include <qheader.h>
#include <qmessagebox.h>
#include <qfile.h>
#include <qxml.h>
#include <qsettings.h>
#include <qcursor.h>


#include "dictreader.h"
#include "gozluksettings.h"
#include "newtermdialog.h"
#include "editdialog.h"
#include "anapencere.h"


anaPencere::anaPencere(QWidget *parent, const char *name):
				QMainWindow(parent,name)
{
	setCentralWidget(new QWidget(this,"merkez"));
	this->setCaption(QString::fromUtf8("Gözlük"));
	// menü
	
	QPopupMenu *menuSecenekler = new QPopupMenu(this);
	menuSecenekler->insertItem(QString::fromUtf8("Ye&ni Kelime"),this, SLOT( yeniKelime() ),CTRL+Key_N);
	menuSecenekler->insertItem(QString::fromUtf8("S&eçiliyi Düzenle"), this, SLOT( kelimeDuzenle() ), CTRL+Key_E);
	menuSecenekler->insertItem(QString::fromUtf8("Seçiliyi Sil"), this, SLOT( seciliSil() ), CTRL+Key_E);
	menuSecenekler->insertItem(QString::fromUtf8("Dışarı Aktar"), this, SLOT( exportToXml() ), CTRL+Key_S);
	menuSecenekler->insertSeparator();
	menuSecenekler->insertItem(QString::fromUtf8("Ya&pılandır"), this, SLOT( settings() ), CTRL+Key_P);
	menuSecenekler->insertSeparator();
	menuSecenekler->insertItem(QString::fromUtf8("Kapat"), this, SLOT( close() ), CTRL+Key_Q);
	
	QPopupMenu *menuAbout = new QPopupMenu(this);
	menuAbout->insertItem(QString::fromUtf8("Gözlük Hakkında"), this, SLOT( about() ), Key_F1);
	
	QMenuBar *menu = new QMenuBar(this);
	menu->insertItem(QString::fromUtf8("&Seçenekler"), menuSecenekler);
	menu->insertItem(QString::fromUtf8("&Hakkında"), menuAbout);

	// liste popup menüsü
	lPopup = new QPopupMenu(this);
	lPopup->insertItem(QString::fromUtf8("Düzenle"), this, SLOT( kelimeDuzenle() ) );
	lPopup->insertItem(QString::fromUtf8("Sil"), this, SLOT( seciliSil() ) );

	
	// arayüz
	QHBoxLayout *ana = new QHBoxLayout(centralWidget(),5); 
	QVBoxLayout *sol = new QVBoxLayout(ana,5);
	
	QHBoxLayout *kBox = new QHBoxLayout(sol, 5);
	lblKelime = new QLabel(QString::fromUtf8("Kelime : "),centralWidget());
	lineSatir = new QLineEdit(centralWidget());
	kBox->addWidget(lblKelime);
	kBox->addWidget(lineSatir);
	
	bgroupDiller = new QHButtonGroup(QString::fromUtf8("Dil Seçenekleri"),centralWidget());
	bgroupDiller->setSizePolicy( QSizePolicy( (QSizePolicy::SizeType)5, (QSizePolicy::SizeType)0, 0, 0, bgroupDiller->sizePolicy().hasHeightForWidth() ) );
	radioEng = new QRadioButton(QString::fromUtf8("İngilizce"), bgroupDiller);
	radioEng->setChecked(true);
	radioTur = new QRadioButton(QString::fromUtf8("Türkçe"), bgroupDiller);
	
	sol->addWidget(bgroupDiller);
	
	gboxAnlam = new QVGroupBox(QString::fromUtf8("Anlamlar"), centralWidget());
	sol->addWidget(gboxAnlam);
	
	lblAnlam = new QLabel(gboxAnlam);
	lblAnlam->setTextFormat( Qt::RichText );
	lblAnlam->setFixedWidth(225);
	
	// sag
	lviewListe = new QListView(centralWidget());
	lviewListe->addColumn( QString::null );
	lviewListe->header()->hide();
	ana->addWidget(lviewListe);
	
	
	// connections
	connect(lineSatir, SIGNAL( textChanged( const QString& ) ), this, SLOT( searchSource( const QString& ) ) );
	connect(lineSatir, SIGNAL( returnPressed() ), this, SLOT( showWord() ) );
	connect(lviewListe, SIGNAL( selectionChanged( QListViewItem * ) ), this, SLOT( showFromList( QListViewItem* ) ) );
	connect(radioEng, SIGNAL( toggled( bool ) ), this, SLOT( langChanged( bool ) ) );
	connect( lviewListe, SIGNAL( rightButtonClicked(QListViewItem *, const QPoint & , int)), this, SLOT( popupSag() ));
	
	currentEntry = new TransDef();
	readDict();
	
	this->resize(550,400);
		
}

void anaPencere::popupSag() 
{ 
	lPopup->exec(QCursor::pos()); 
}

void anaPencere::seciliSil()
{
	// nothing... yet :P
}

void anaPencere::yeniKelime()
{
	newTerm a(this);
	if (a.exec() == QDialog::Accepted)
	{
		TransDef *yenisi = new TransDef();
		for (QStringList::Iterator it = a.sList->begin(); it != a.sList->end(); ++it)
			yenisi->addSource( *it );
		
		for (QStringList::Iterator it = a.tList->begin(); it != a.tList->end(); ++it)
			yenisi->addTranslation( *it );
		
		for (QStringList::Iterator it = a.dList->begin(); it != a.dList->end(); ++it)
			yenisi->setDefinition( *it );
			
		entries.append( yenisi );
	}
}

void anaPencere::exportToXml()
{
	QFileDialog *kayitAni = new QFileDialog( this, "saving", TRUE );
	kayitAni->setMode (QFileDialog::AnyFile);
	kayitAni->setCaption( QString::fromUtf8("Sözcükleri XML dosyası olarak dışa aktar"));
	// kayitAni->setFilter( QString::fromUtf8("Xml Dosyaları (*.xml)"));
	QString fileName;
	if (kayitAni->exec() == QDialog::Accepted)
	{
		fileName = kayitAni->selectedFile();
		writeDict(fileName);
	}
	
}

void anaPencere::kelimeDuzenle()
{
	editTerm e(this);
	e.exec();
}

void anaPencere::settings()
{
	 GozlukSettings gs(this); // parenthood :D
    if ( gs.exec() == QDialog::Accepted )
        readDict();
}

void anaPencere::about()
{
	QMessageBox::information(this,QString::fromUtf8("Gözlük Hakkında"),
	QString::fromUtf8("Uludağ/Pardus, Sözlük Programı\nMayıs, 2005"));
}


void anaPencere::readDict()
{
	QSettings settings;
	settings.setPath("Uludag", "Gozluk");
	QString dictFile = settings.readEntry( "sozluk/xml", "none");
	
	DictReader dictreader( this );
	QFile file( dictFile );
	
	if ( !file.exists() ) return;
	
	QXmlInputSource source(file);
	QXmlSimpleReader reader;
	reader.setContentHandler( &dictreader );
	
	connect( &dictreader, SIGNAL( signalSource( const QString ) ),
             this, SLOT( setCurrentSource( const QString ) ) );

   connect( &dictreader, SIGNAL( signalTranslation( const QString ) ),
             this, SLOT( addCurrentTranslation( const QString ) ) );

   connect( &dictreader, SIGNAL( signalDefinition( const QString ) ),
             this, SLOT( setCurrentDefinition( const QString ) ) );

   // end of term, add it to the entries list.
   connect( &dictreader, SIGNAL( signalEndTerm() ),
             this, SLOT( addEntry() ) );

   reader.parse( source );
}

void anaPencere::writeDict( const QString& dictFile )
{
    QFile file( dictFile );

    if ( !file.open( IO_WriteOnly ) ) {
        printf( "dosyaya yazilamiyor...\n" );
        return;
    }

    QTextStream str( &file );
    str << QString::fromUtf8( "<ud_sözlük>\n<short>Uludağ</short>\n\
<copyright>http://www.uludag.org.tr</copyright>\n\n" );

    QPtrListIterator<TransDef> it( entries );
    TransDef *entry;
    while ( ( entry = it.current() ) != 0 ) {
        ++it;

        str << "<term>";

        // sources
        QStringList srcs( entry->getSources() );
        QStringList::ConstIterator sit = srcs.begin();
        QStringList::ConstIterator send = srcs.end();
        for ( ; sit != send; ++sit ) {
            str << "<s>" << *sit << "</s>";
        }

        // translations
        str << "\n";
        QStringList trans( entry->getTranslations() );
        QStringList::ConstIterator it = trans.begin();
        QStringList::ConstIterator tend = trans.end();
        for ( ; it != tend; ++it ) {
            str << "<t>" << *it << "</t>";
        }

        if ( entry->getDefinition().length() != 0 ) {
            str << "<d>" << entry->getDefinition() << "</d>";
        }

        str << "\n</term>\n";
    }

    file.close();
}

void anaPencere::setCurrentSource( const QString s )
{
    currentEntry->addSource( s );
}

void anaPencere::addCurrentTranslation( const QString t )
{
    currentEntry->addTranslation( t );
}

void anaPencere::setCurrentDefinition( const QString d )
{
    currentEntry->setDefinition( d );
}

void anaPencere::addEntry()
{
    entries.append( currentEntry );

    // from now on we need a new current
    currentEntry = new TransDef();
}

void anaPencere::searchSource( const QString& text )
{
    // clean all found words first;
    lviewListe->clear();

    QString *s = new QString( text );
    QListViewItem *item = NULL;

    QPtrListIterator<TransDef> it( entries );
    TransDef *entry;
    while ( ( entry = it.current() ) != 0 ) {
        ++it;

        if ( searchEnglish ) {
            QStringList srcs( entry->getSources() );
            QStringList::ConstIterator sit = srcs.begin();
            QStringList::ConstIterator send = srcs.end();
            for ( ; sit != send; ++sit ) { // search in sources list
                // fill words list
                if ( (*sit).lower().startsWith( *s ) ) {
                    item = new QListViewItem( lviewListe, *sit );
                }

                // if found set current
                if ( s->lower() == (*sit).lower() )
                    currentEntry = entry;
            }
        }
        else { // Turkish search. Search in translations.
            QStringList trans( entry->getTranslations() );
            QStringList::ConstIterator it = trans.begin();
            QStringList::ConstIterator tend = trans.end();
            for ( ; it != tend; ++it ) {
                if ( (*it).lower().startsWith( *s ) ) {
                    item = new QListViewItem( lviewListe, *it );
                }

                if ( s->lower() == (*it).lower() )
                    currentEntry = entry;
            }
        }
    }
    delete s;
}

void anaPencere::langChanged( bool isEng )
{
    searchEnglish = isEng;

    // lang changed, search again
    searchSource( lineSatir->text() );
}

void anaPencere::showWord()
{
    QString str;

    // sources
    str = QString::fromUtf8( "<font color='maroon'><h3>İngilizce</h3>" );
    QStringList srcs( currentEntry->getSources() );
    QStringList::ConstIterator sit = srcs.begin();
    QStringList::ConstIterator send = srcs.end();
    for ( ; sit != send; ++sit ) {
        str += *sit + "<br>";
    }
    str += "</font>";

    // translations
    str += QString::fromUtf8( "<font color='navy'><h3>Türkçe</h3>" );
    QStringList trans( currentEntry->getTranslations() );
    QStringList::ConstIterator it = trans.begin();
    QStringList::ConstIterator tend = trans.end();
    for ( ; it != tend; ++it ) {
        str += *it + "<br>";
    }
    str += "</font>";

    //definition
    str += QString::fromUtf8( "<font color='darkgreen'><h3>Tanım</h3>" )
           + currentEntry->getDefinition() + "</font>";
    lblAnlam->setText( str );
    return;
}

// set the currentEntry from ListView and call showWord
void anaPencere::showFromList( QListViewItem* item )
{
    QString *s = new QString( item->text( 0 ) );

    QPtrListIterator<TransDef> it( entries );
    TransDef *entry;
    while ( ( entry = it.current() ) != 0 ) {
        ++it;

        if ( searchEnglish ) {
            QStringList srcs( entry->getSources() );
            QStringList::ConstIterator sit = srcs.begin();
            QStringList::ConstIterator send = srcs.end();
            for ( ; sit != send; ++sit ) { // search in sources list
                // if found set current
                if ( s->lower() == (*sit).lower() )
                    currentEntry = entry;
            }
        }
        else { // Turkish search. Search in translations.
            QStringList trans( entry->getTranslations() );
            QStringList::ConstIterator it = trans.begin();
            QStringList::ConstIterator tend = trans.end();
            for ( ; it != tend; ++it ) {
                if ( s->lower() == (*it).lower() )
                    currentEntry = entry;
            }
        }
    }
    delete s;
    showWord();
}

anaPencere::~anaPencere()
{	writeDict( "/tmp/yenigozluk.xml" ); } 


