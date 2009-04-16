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
#include <qstatusbar.h>

#include "gozluk32.xpm"
#include "dictreader.h"
#include "gozluksettings.h"
#include "editdialog.h"
#include "anapencere.h"


anaPencere::anaPencere(QWidget *parent, const char *name):
				QMainWindow(parent,name)
{
	setCentralWidget(new QWidget(this,"merkez"));
	this->setCaption(QString::fromUtf8("Gözlük"));
	this->setIcon(QPixmap(gozluk_xpm));
	// menü
	
	menuSecenekler = new QPopupMenu(this);
	menuDosya = new QPopupMenu(this);
	
	menuDosya->insertItem(QString::fromUtf8("Yeni Sözlük"), this, SLOT( yeniSozluk() )); 
	menuDosya->insertItem(QString::fromUtf8("Sözlük Dosyası Aç"), this, SLOT( sozlukAc() ), CTRL+Key_O);
	menuDosya->insertItem(QString::fromUtf8("Dışarı Aktar"), this, SLOT( exportToXml() ), CTRL+Key_S);
	menuDosya->insertSeparator();
	menuDosya->insertItem(QString::fromUtf8("Ya&pılandır"), this, SLOT( settings() ), CTRL+Key_P);
	menuDosya->insertSeparator();
	menuDosya->insertItem(QString::fromUtf8("Kapat"), this, SLOT( close() ), CTRL+Key_Q);
	
	menuSecenekler->insertItem(QString::fromUtf8("Ye&ni Kelime"),this, SLOT( yeniKelime() ),CTRL+Key_N);
	edit1 = menuSecenekler->insertItem(QString::fromUtf8("S&eçiliyi Düzenle"), this, SLOT( kelimeDuzenle() ), CTRL+Key_E);
	sil1 = menuSecenekler->insertItem(QString::fromUtf8("Seçiliyi Sil"), this, SLOT( seciliSil() ), CTRL+Key_D);
	
	menuSecenekler->setItemEnabled(edit1,false);
	menuSecenekler->setItemEnabled(sil1,false);
	
	menuAbout = new QPopupMenu(this);
	menuAbout->insertItem(QString::fromUtf8("Gözlük Hakkında"), this, SLOT( about() ), Key_F1);
	
	QMenuBar *menu = new QMenuBar(this);
	menu->insertItem(QString::fromUtf8("&Dosya"), menuDosya);
	menu->insertItem(QString::fromUtf8("Düze&nle"), menuSecenekler);
	menu->insertItem(QString::fromUtf8("&Hakkında"), menuAbout);

	// liste popup menüsü
	lPopup = new QPopupMenu(this);
	edit2 = lPopup->insertItem(QString::fromUtf8("Düzenle"), this, SLOT( kelimeDuzenle() ) );
	sil2 = lPopup->insertItem(QString::fromUtf8("Sil"), this, SLOT( seciliSil() ) );

	lPopup->setItemEnabled(edit2,false);
	lPopup->setItemEnabled(sil2,false);
	
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
	
	// statusbar :D
	statusBar()->message(QString::fromUtf8("Gözlük'e Hoşgeldiniz!"),2000);
	
	
	// connections
	connect(lineSatir, SIGNAL( textChanged( const QString& ) ), this, SLOT( searchSource( const QString& ) ) );
	connect(lineSatir, SIGNAL( returnPressed() ), this, SLOT( showWord() ) );
	connect(lviewListe, SIGNAL( selectionChanged( QListViewItem * ) ), this, SLOT( showFromList( QListViewItem* ) ) );
	connect(radioEng, SIGNAL( toggled( bool ) ), this, SLOT( langChanged( bool ) ) );
	connect(lviewListe, SIGNAL( rightButtonClicked(QListViewItem *, const QPoint & , int)), this, SLOT( popupSag() ));
	//connect(lviewListe, SIGNAL( selectionChanged() ), this, SLOT(selectionUpdate() ) );
	connect(lviewListe, SIGNAL( selectionChanged(QListViewItem *) ), this, SLOT(selectionUpdate() ) );
	
	currentEntry = new TransDef();
	readDict(QString::null);
	
	edited = FALSE;
	
	this->resize(550,400);
		
}

void anaPencere::selectionUpdate()
{
	if (lviewListe->childCount() == 0)
	{
		menuSecenekler->setItemEnabled(edit1,false);
		menuSecenekler->setItemEnabled(sil1,false);
		lPopup->setItemEnabled(edit2,false);
		lPopup->setItemEnabled(sil2,false);
	}
	else
	{
		menuSecenekler->setItemEnabled(edit1,true);
		menuSecenekler->setItemEnabled(sil1,true);
		lPopup->setItemEnabled(edit2,true);
		lPopup->setItemEnabled(sil2,true);
	}
}

void anaPencere::yeniSozluk()
{
	// eger su anki sözlük edit edilmişse, kaydetmesi için bir şans ver:)
	while (getEdited())
	{
		if (!QMessageBox::warning(this, QString::fromUtf8("Değişiklikler kaydedilmedi!"),
				QString::fromUtf8("Bu sözlük dosyasındaki değişiklikleri kaydetmek ister misiniz?"),
				QString::fromUtf8("&Evet"),
				QString::fromUtf8("&Hayır"),
				QString::null,0,1))
		{
			exportToXml();
		}
		else setEdited( FALSE );
	}
	entries.clear();
	lviewListe->clear();
	statusBar()->message(QString::fromUtf8("Yeni sözlük açıldı..."),3000);
}
void anaPencere::sozlukAc()
{
	while (getEdited())
	{
		if (!QMessageBox::warning(this, QString::fromUtf8("Değişiklikler kaydedilmedi!"),
				QString::fromUtf8("Bu sözlük dosyasındaki değişiklikleri kaydetmek ister misiniz?"),
				QString::fromUtf8("&Evet"),
				QString::fromUtf8("&Hayır"),
				QString::null,0,1))
		{
			exportToXml();
		}
		else setEdited( FALSE );
	}
	QFileDialog *dosyaAc = new QFileDialog(this,"ac",TRUE);
	dosyaAc->setCaption(QString::fromUtf8("Sözlük dosyasını seçin"));
	if (dosyaAc->exec() == QDialog::Accepted)
	{
		currentEntry = new TransDef();
		entries.clear();
		readDict(dosyaAc->selectedFile());
		searchEnglish = radioEng->isChecked();
		lviewListe->clear();
		searchSource( lineSatir->text() );
	}
}

void anaPencere::popupSag() 
{ 
	lPopup->exec(QCursor::pos()); 
}

void anaPencere::seciliSil()
{
	if (lviewListe->currentItem() == 0)
	{
		QMessageBox::warning(this,QString::fromUtf8("Ufak bir hata!"),
		QString::fromUtf8("Listede kelime seçili değil"));
		return;
	}
	// önce bi uyarı göstermeli :)
	if (!QMessageBox::warning(this, QString::fromUtf8("Uyarı! Silmek üzeresiniz..."),
			QString::fromUtf8("Bu kelimeyi silmek istediğinizden emin misiniz?"),
			QString::fromUtf8("&Evet"),
			QString::fromUtf8("&Hayır"),
			QString::null,1,0) )
	{
		//  eh, sil dedi...
		entries.remove(currentEntry);
		statusBar()->message(QString::fromUtf8("Kelime silindi..."),3000);
		// tazeleme
		lviewListe->clear();
		searchSource( lineSatir->text() );
		setEdited( TRUE );
	}
}

void anaPencere::yeniKelime()
{
	TransDef *yenisi = new TransDef();
	editTerm a(this,"yenisi",yenisi);
	if (a.exec() == QDialog::Accepted)
	{
		for (QStringList::Iterator it = a.sList->begin(); it != a.sList->end(); ++it)
			yenisi->addSource( *it );
		
		for (QStringList::Iterator it = a.tList->begin(); it != a.tList->end(); ++it)
			yenisi->addTranslation( *it );
		
		// Fixed
		QStringList::Iterator it = a.dList->begin();
		yenisi->setDefinition( *it );
		entries.append( yenisi );
		statusBar()->message(QString::fromUtf8("Yeni kelime eklendi"),3000);
		searchEnglish = radioEng->isChecked();
		lviewListe->clear();
		searchSource( lineSatir->text() );
		// edited
		setEdited( TRUE );
	}
	else delete yenisi; // kullanmadiysan sil... sonra bi daha istersin :)
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
		// edited->saved
		setEdited( FALSE );
	}
	
}

void anaPencere::kelimeDuzenle()
{
	if (lviewListe->currentItem() == 0)
	{
		QMessageBox::warning(this,QString::fromUtf8("Ufak bir hata!"),
		QString::fromUtf8("Listede kelime seçili değil"));
		return;
	}
	editTerm e(this, "myEditDialog:P", currentEntry);
	if (e.exec() == QDialog::Accepted)
	{
		// not a lot to do ;)
		currentEntry->temizle(); // lists are cleared
		for (QStringList::Iterator it = e.sList->begin(); it != e.sList->end(); ++it)
			currentEntry->addSource( *it );
		
		for (QStringList::Iterator it = e.tList->begin(); it != e.tList->end(); ++it)
			currentEntry->addTranslation( *it );
		
		// Fixed
		QStringList::Iterator it = e.dList->begin();
		currentEntry->setDefinition( *it );
		
		searchEnglish = radioEng->isChecked();
		lviewListe->clear();
		searchSource( lineSatir->text() );
		showWord();
		
		statusBar()->message(QString::fromUtf8("Kelime düzenlendi..."),3000);
		
		// edited
		setEdited( TRUE );
	}
}

void anaPencere::settings()
{
	 GozlukSettings gs(this); // parenthood :D
    if ( gs.exec() == QDialog::Accepted )
        readDict(QString::null);
}

void anaPencere::about()
{
	QMessageBox::information(this,QString::fromUtf8("Gözlük Hakkında"),
	QString::fromUtf8("Uludağ/Pardus, Gözlük Programı\n2005"));
}


void anaPencere::readDict(QString sozlukDosyasi)
{
	QSettings settings;
	QString dictFile;
	settings.setPath("Uludag", "Gozluk");
	if (sozlukDosyasi == QString::null)
		dictFile = settings.readEntry( "sozluk/xml", "none");
	else dictFile = sozlukDosyasi;
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
   searchEnglish = radioEng->isChecked();
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
	 // son hamle
	 str << QString::fromUtf8("</ud_sözlük>");
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

    if (text.isEmpty())
	 {
		menuSecenekler->setItemEnabled(edit1,false);
		menuSecenekler->setItemEnabled(sil1,false);
		lPopup->setItemEnabled(edit2,false);
		lPopup->setItemEnabled(sil2,false);
		return;
	 }

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
				if (lviewListe->childCount() == 0)
				{
					menuSecenekler->setItemEnabled(edit1,false);
					menuSecenekler->setItemEnabled(sil1,false);
					lPopup->setItemEnabled(edit2,false);
					lPopup->setItemEnabled(sil2,false);
				}
				else
				{
					menuSecenekler->setItemEnabled(edit1,true);
					menuSecenekler->setItemEnabled(sil1,true);
					lPopup->setItemEnabled(edit2,true);
					lPopup->setItemEnabled(sil2,true);
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
				if (lviewListe->childCount() == 0)
				{
					menuSecenekler->setItemEnabled(edit1,false);
					menuSecenekler->setItemEnabled(sil1,false);
					lPopup->setItemEnabled(edit2,false);
					lPopup->setItemEnabled(sil2,false);
				}
				else
				{
					menuSecenekler->setItemEnabled(edit1,true);
					menuSecenekler->setItemEnabled(sil1,true);
					lPopup->setItemEnabled(edit2,true);
					lPopup->setItemEnabled(sil2,true);
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

void anaPencere::closeEvent(QCloseEvent *event)
{
	while (getEdited())
		{
			if (!QMessageBox::warning(this, QString::fromUtf8("Değişiklikler kaydedilmedi!"),
					QString::fromUtf8("Bu sözlük dosyasındaki değişiklikleri kaydetmek ister misiniz?"),
					QString::fromUtf8("&Evet"),
					QString::fromUtf8("&Hayır"),
					QString::null,0,1))
			{
				exportToXml();
			}
			else 
			{ 
				setEdited( FALSE );
			}
		}	
	event->accept();
}

anaPencere::~anaPencere()
{	writeDict( "/tmp/yenigozluk.xml" ); } 


