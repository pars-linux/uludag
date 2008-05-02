/*
  Copyright (c) TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

/*
  tasma - ticonview.h
  TIconView: a KIconView showing configuration modules for a category.
*/

#ifndef T_ICON_VIEW_H
#define T_ICON_VIEW_H

#include <kiconview.h>
#include <qtooltip.h>
#include <qlabel.h>

class KCModule;
class KCModuleInfo;
class TIconView;
class QLabel;

class TIconViewItem : public KIconViewItem
{

 public:
  TIconViewItem( TIconView *parent, const QString& text,
                 const QPixmap& icon, KCModuleInfo* moduleinfo, QString itemComment);

  ~TIconViewItem();

  KCModuleInfo* moduleinfo() const;
  QString comment;

 private:
  KCModuleInfo* _moduleinfo;


};


class TIconView : public KIconView
{
 Q_OBJECT

   public:
  TIconView( QWidget *parent, const char* name = 0 );
  virtual ~TIconView();

  void setCategory( const QString& path );

  bool showExtras;

 signals:
    void signalModuleSelected( KCModule*, const QString&, const QString&, const QString&, bool);

 protected slots:
    void slotItemSelected( QIconViewItem* item );

 private slots:
     void showToolTip( QIconViewItem *item );
     void removeToolTip();

 protected:
    virtual void keyPressEvent(QKeyEvent *event);
    virtual void contentsMouseDoubleClickEvent (QMouseEvent *event);
    virtual void contentsMousePressEvent(QMouseEvent* event);
    virtual void focusInEvent ( QFocusEvent * e );
 // virtual void contentsMouseMoveEvent(QMouseEvent* event); //this event causes crashing.

 private:
  KCModule* _module;

  QPoint dragPos;
  TIconViewItem* dragItem;

  void startDrag();
  QLabel *toolTip;


};

#endif // T_ICON_VIEW_H
