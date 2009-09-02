/****************************************************************************
** Meta object code from reading C++ file 'tvconfigui.h'
**
** Created: Tue Sep 1 14:44:00 2009
**      by: The Qt Meta Object Compiler version 61 (Qt 4.5.2)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "tvconfigui.h"
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'tvconfigui.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 61
#error "This file was generated using the moc from 4.5.2. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
static const uint qt_meta_data_TvConfigUI[] = {

 // content:
       2,       // revision
       0,       // classname
       0,    0, // classinfo
       0,    0, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors

       0        // eod
};

static const char qt_meta_stringdata_TvConfigUI[] = {
    "TvConfigUI\0"
};

const QMetaObject TvConfigUI::staticMetaObject = {
    { &QWidget::staticMetaObject, qt_meta_stringdata_TvConfigUI,
      qt_meta_data_TvConfigUI, 0 }
};

const QMetaObject *TvConfigUI::metaObject() const
{
    return &staticMetaObject;
}

void *TvConfigUI::qt_metacast(const char *_clname)
{
    if (!_clname) return 0;
    if (!strcmp(_clname, qt_meta_stringdata_TvConfigUI))
        return static_cast<void*>(const_cast< TvConfigUI*>(this));
    return QWidget::qt_metacast(_clname);
}

int TvConfigUI::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QWidget::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    return _id;
}
QT_END_MOC_NAMESPACE
