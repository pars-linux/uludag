/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef GOZLUK_WIN_H
#define GOZLUK_WIN_H

#include <qmainwindow.h>
#include <qstringlist.h>
#include <qptrlist.h>
#include <qstringlist.h>

#include <qpushbutton.h>
#include <qlineedit.h>
#include <qhbuttongroup.h>
#include <qradiobutton.h>
#include <qlistview.h>
#include <qlabel.h>

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

private:
    QStringList sources; // sources string list
    QStringList translations; // translations list
    QString definition; // definition
};

// our dear main window
class GozlukWin : public QMainWindow
{
    Q_OBJECT
public:
    GozlukWin( const char *name = 0 );
    ~GozlukWin();

signals:
    void signalQuit();

protected slots:
    void setCurrentSource( const QString s );
    void addCurrentTranslation( const QString t );
    void setCurrentDefinition( const QString d );

    void addEntry();

    void searchSource( const QString& );
    void showWord();
    void showFromList( QListViewItem* );
    
    void langChanged( bool );

    void configureGozluk();
    void quitHandler();

protected:
    void readDict();
    void writeDict( const QString& dictFile );

private:
    QPtrList<TransDef> entries;
    TransDef *currentEntry;
    bool searchEnglish;

    //widgets
    QLineEdit *source;
    QHButtonGroup *langGroup;
    QRadioButton *turkish, *english;
    QListView *words;
    QLabel *view;
    QPushButton *confButton;
    QPushButton *quitButton;
};

#endif // GOZLUK_WIN_H
