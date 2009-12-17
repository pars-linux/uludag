/*
  Copyright (c) TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

/*
  tasma - tmoduleview.h
  ContentWidet: main content widget of the module.
  TMContent:  a scrollview showing module content.
  TModuleView: view a module widget with action buttons.
*/

#ifndef T_MODULE_VIEW_H
#define T_MODULE_VIEW_H

#include <qscrollview.h>
#include <qxembed.h>

class KProcess;
class KCModule;
class KPushButton;
class KSeparator;
class QVBoxLayout;
class QLabel;
class QVBox;
class QVBoxLayout;
class QWidgetStack;

class ContentWidget : public QWidget
{
 public:
 ContentWidget( QWidget* parent ) : QWidget( parent ) {}
  ~ContentWidget(){}

  QSize sizeHint() const { return minimumSizeHint(); }
};


class TMContent : public QScrollView
{
 public:
  TMContent( QWidget *parent, KCModule *module );
  ~TMContent();

  KCModule* module() const;

 private:
  ContentWidget *contentWidget;
  QVBoxLayout *vbox;
  KCModule *_module;
};

class TModuleView : public QWidget
{
 Q_OBJECT

   public:
  TModuleView( QWidget *parent, KCModule* module,
               const QString& icon_path, const QString& text, const QString& filename, bool needsRootPrivileges );

  ~TModuleView();

  /* minimum size is sufficient for a module view */
  QSize sizeHint() const { return minimumSizeHint(); }

 public slots:
  void applyClicked();
  void resetClicked();
  void defaultClicked();
  void contentChanged( bool state );
  void runAsRoot();
  void killRootProcess();
  void embedded();

 private:
  TMContent *contentView;
  KSeparator *_sep;
  KPushButton *_apply, *_reset, *_default, *_back, *_runAsRoot;
  KProcess *_proc;
  QXEmbed *_embedWidget;
  QWidgetStack *_embedStack;
  QVBoxLayout *_embedLayout;
  QVBox *_embedFrame;
  QString _filename;
  QLabel *_icon, *_moduleName;
  QWidget *parentInner;
};

class TModuleViewEmbed : public QXEmbed
{
Q_OBJECT

 public:
 TModuleViewEmbed( QWidget* w ) : QXEmbed( w ) {}
  virtual void windowChanged( WId w ) { if( w ) emit windowEmbedded( w ); }
 signals:
  void windowEmbedded( WId w );
};

#endif // T_MODULE_VIEW_H
