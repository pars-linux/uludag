/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <qfile.h>
#include <qxml.h>
#include <qsettings.h>
#include <qlayout.h>
#include <qheader.h>
#include <qdialog.h>

#include "dictreader.h"
#include "gozluksettings.h"
#include "gozlukwin.h"

GozlukWin::GozlukWin( const char *name )
    : QMainWindow( 0, name ), searchEnglish( true )
{
    QVBoxLayout *vbox = new QVBoxLayout( this, 5 );

    QHBoxLayout *hbox1 = new QHBoxLayout( vbox, 5 );
    // search
    source = new QLineEdit( this );
    source->setFixedWidth( 200 ); // deneme FIXME
    // lang
    langGroup = new QHButtonGroup( this );
    langGroup->setFrameStyle( QFrame::NoFrame );
    english = new QRadioButton( QString::fromUtf8( "İ&ngilizce" ), langGroup );
    english->setChecked( true ); // default
    turkish = new QRadioButton( QString::fromUtf8( "&Türkçe" ), langGroup );

    hbox1->addWidget( source, 0, AlignLeft );
    hbox1->addWidget( langGroup );

    QHBoxLayout *hbox2 = new QHBoxLayout( vbox, 5 );
    // found words
    words = new QListView( this );
    words->addColumn( QString::null );
    words->header()->hide();
    words->setFixedWidth( 200 ); // deneme FIXME
    // view
    view = new QLabel( "denemeee", this );
    view->setTextFormat( Qt::RichText );

    hbox2->addWidget( words, 0, AlignLeft );
    hbox2->addWidget( view, 0, AlignTop );

    // interactive search :)
    connect( source, SIGNAL( textChanged( const QString& ) ),
             this, SLOT( searchSource( const QString& ) ) );
    connect( source, SIGNAL( returnPressed() ),
             this, SLOT( showWord() ) );
    connect( words, SIGNAL( selectionChanged( QListViewItem * ) ),
             this, SLOT( showFromList( QListViewItem * ) ) );

    connect( english, SIGNAL( toggled( bool ) ),
             this, SLOT( langChanged( bool ) ) );

    // buttons
    QHBoxLayout *buttons = new QHBoxLayout( vbox, 10 );
    confButton = new QPushButton( QString::fromUtf8( "Yapılandır..." ), this );
    quitButton = new QPushButton( QString::fromUtf8( "Çık" ), this );
    buttons->addWidget( confButton );
    buttons->addStretch( 1 );
    buttons->addWidget( quitButton );

    connect( confButton, SIGNAL( clicked() ),
             this, SLOT( configureGozluk() ) );
    connect( quitButton, SIGNAL( clicked() ),
             this, SLOT( quitHandler() ) );


    currentEntry = new TransDef();

    readDict();
}

void GozlukWin::readDict()
{
    // get xml file
    QSettings settings;
    settings.setPath( "Uludag", "Gozluk" );
    QString dictFile = settings.readEntry( "sozluk/xml", "none" );

    DictReader dictreader( this );
    QFile file( dictFile );

    if ( !file.exists() ) return;

    QXmlInputSource source( file );
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

void GozlukWin::writeDict( const QString& dictFile )
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
        QStringList::Iterator sit = srcs.begin();
        for ( ; sit != srcs.end(); ++sit ) {
            str << "<s>" << *sit << "</s>";
        }

        // translations
        str << "\n";
        QStringList trans( entry->getTranslations() );
        QStringList::Iterator it = trans.begin();
        for ( ; it != trans.end(); ++it ) {
            str << "<t>" << *it << "</t>";
        }

        if ( entry->getDefinition().length() != 0 ) {
            str << "<d>" << entry->getDefinition() << "</d>";
        }

        str << "\n</term>\n";
    }

    file.close();
}

void GozlukWin::setCurrentSource( const QString s )
{
    currentEntry->addSource( s );
}

void GozlukWin::addCurrentTranslation( const QString t )
{
    currentEntry->addTranslation( t );
}

void GozlukWin::setCurrentDefinition( const QString d )
{
    currentEntry->setDefinition( d );
}

void GozlukWin::addEntry()
{
    entries.append( currentEntry );

    // from now on we need a new current
    currentEntry = new TransDef();
}

void GozlukWin::searchSource( const QString& text )
{
    // clean all found words first;
    words->clear();

    QString *s = new QString( text );
    QListViewItem *item = NULL;

    QPtrListIterator<TransDef> it( entries );
    TransDef *entry;
    while ( ( entry = it.current() ) != 0 ) {
        ++it;

        if ( searchEnglish ) {
            QStringList srcs( entry->getSources() );
            QStringList::Iterator sit = srcs.begin();
            for ( ; sit != srcs.end(); ++sit ) { // search in sources list
                // fill words list
                if ( (*sit).lower().startsWith( *s ) ) {
                    item = new QListViewItem( words, *sit );
                }

                // if found set current
                if ( s->lower() == (*sit).lower() )
                    currentEntry = entry;
            }
        }
        else { // Turkish search. Search in translations.
            QStringList trans( entry->getTranslations() );
            QStringList::Iterator it = trans.begin();
            for ( ; it != trans.end(); ++it ) {
                if ( (*it).lower().startsWith( *s ) ) {
                    item = new QListViewItem( words, *it );
                }

                if ( s->lower() == (*it).lower() )
                    currentEntry = entry;
            }
        }
    }
    delete s;
}

void GozlukWin::langChanged( bool isEng )
{
    searchEnglish = isEng;

    // lang changed, search again
    searchSource( source->text() );
}

void GozlukWin::showWord()
{
    QString str;

    // sources
    str = QString::fromUtf8( "<em>İngilizce:</em><br>" );
    QStringList srcs( currentEntry->getSources() );
    QStringList::Iterator sit = srcs.begin();
    for ( ; sit != srcs.end(); ++sit ) {
        str += "<b>" + *sit + "</b><br>";
    }
    str += "<br>";

    // translations
    str += QString::fromUtf8( "<em>Türkçe:</em>" );
    QStringList trans( currentEntry->getTranslations() );
    QStringList::Iterator it = trans.begin();
    for ( ; it != trans.end(); ++it ) {
        str += "<br>" + *it;

    }

    //definition
    str += QString::fromUtf8( "<br><br><em>Tanım:</em><br>" )
           + currentEntry->getDefinition();

    view->setText( str );
    return;
}

// set the currentEntry from ListView and call showWord
void GozlukWin::showFromList( QListViewItem* item )
{
    QString *s = new QString( item->text( 0 ) );

    QPtrListIterator<TransDef> it( entries );
    TransDef *entry;
    while ( ( entry = it.current() ) != 0 ) {
        ++it;

        if ( searchEnglish ) {
            QStringList srcs( entry->getSources() );
            QStringList::Iterator sit = srcs.begin();
            for ( ; sit != srcs.end(); ++sit ) { // search in sources list
                // if found set current
                if ( s->lower() == (*sit).lower() )
                    currentEntry = entry;
            }
        }
        else { // Turkish search. Search in translations.
            QStringList trans( entry->getTranslations() );
            QStringList::Iterator it = trans.begin();
            for ( ; it != trans.end(); ++it ) {
                if ( s->lower() == (*it).lower() )
                    currentEntry = entry;
            }
        }
    }
    delete s;
    showWord();
}

GozlukWin::~GozlukWin()
{
    /*
    QSettings settings;
    settings.setPath(  "Uludag",  "Gozluk" );
    writeDict(  settings.readEntry(  "sozluk/xml",  "none" ) );
    */

    //deneme
    writeDict( "/tmp/yenigozluk.xml" );

}

void GozlukWin::configureGozluk()
{
    GozlukSettings gs;
    if ( gs.exec() == QDialog::Accepted )
        readDict();
}

void GozlukWin::quitHandler()
{
    emit signalQuit();
}
