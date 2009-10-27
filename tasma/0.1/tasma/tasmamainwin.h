/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

/*
  tasma - tasmamainwin.h
  Main window. 
  Uses a TModuleCategoryList to show configuration module categories,
  a TIconView to show the modules in a category and a TModuleView to
  show the module contents (KCModule).
*/

#ifndef TASMA_MAIN_WIN_H
#define TASMA_MAIN_WIN_H


#include <kmainwindow.h>

class KMainWindow;
class QHBox;
class QListViewItem;
class QWidgetStack;
class KCModule;
class TModuleCategoryList;
class TModuleView;
class TCategoryView;
class AboutView;

class TasmaMainWin : public KMainWindow
{
    Q_OBJECT

public:
    TasmaMainWin( const char* name = 0 );
    ~TasmaMainWin() {}

protected:
    void setupActions(); // menubar and shortcut keys.

protected slots:
    void categorySelected( QListViewItem *category ); // group/category selected
    void moduleSelected( KCModule *module,
			 const QString& icon_path,
			 const QString& text ); // Configuration module selected
    void backToCategory(); // go back from moduleview to category view.

private:
    QHBox *_hbox;
    TModuleCategoryList *_index;
    TModuleView *_moduleview;
    QWidgetStack *_wstack;
    TCategoryView *_categoryview;
    AboutView *_about;

    QListViewItem *_currentCategory;

};

#endif // TASMA_MAIN_WIN_H
