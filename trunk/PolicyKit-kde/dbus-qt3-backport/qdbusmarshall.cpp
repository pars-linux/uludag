/* qdbusmarshall.cpp
 *
 * Copyright (C) 2005 Harald Fernengel <harry@kdevelop.org>
 *
 * Licensed under the Academic Free License version 2.1
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301,
 * USA.
 *
 */

#include "qdbusmarshall.h"
#include "dbus/qdbusvariant.h"

#include <qvariant.h>
#include <qvaluelist.h>
#include <qmap.h>
#include <qstringlist.h>
#include <qvaluevector.h>

#include <dbus/dbus.h>

template <typename T>
inline T qIterGet(DBusMessageIter *it)
{
    T t;
    dbus_message_iter_get_basic(it, &t);
    return t;
}

static QStringList qFetchStringList(DBusMessageIter *arrayIt)
{
    QStringList list;

    DBusMessageIter it;
    dbus_message_iter_recurse(arrayIt, &it);

    do {
        list.append(QString::fromUtf8(qIterGet<char *>(&it)));
    } while (dbus_message_iter_next(&it));

    return list;
}

static QVariant qFetchParameter(DBusMessageIter *it)
{
    switch (dbus_message_iter_get_arg_type(it)) {
    case DBUS_TYPE_BYTE:
        return qIterGet<unsigned char>(it);
    case DBUS_TYPE_INT16:
	return qIterGet<dbus_int16_t>(it);
    case DBUS_TYPE_UINT16:
	return qIterGet<dbus_uint16_t>(it);
    case DBUS_TYPE_INT32:
        return qIterGet<dbus_int32_t>(it);
    case DBUS_TYPE_UINT32:
        return qIterGet<dbus_uint32_t>(it);
    case DBUS_TYPE_DOUBLE:
        return qIterGet<double>(it);
    case DBUS_TYPE_BOOLEAN:
        return QVariant(qIterGet<dbus_bool_t>(it), 0);
    case DBUS_TYPE_INT64:
        return QVariant((Q_LLONG)qIterGet<dbus_int64_t>(it));
    case DBUS_TYPE_UINT64:
        return QVariant((Q_ULLONG)qIterGet<dbus_uint64_t>(it));
    case DBUS_TYPE_STRING:
    case DBUS_TYPE_OBJECT_PATH:
    case DBUS_TYPE_SIGNATURE:
        return QString::fromUtf8(qIterGet<char *>(it));
    case DBUS_TYPE_ARRAY: {
        int arrayType = dbus_message_iter_get_element_type(it);
        if (arrayType == DBUS_TYPE_STRING || arrayType == DBUS_TYPE_OBJECT_PATH) {
            return qFetchStringList(it);
        } else if (arrayType == DBUS_TYPE_BYTE) {
            DBusMessageIter sub;
            dbus_message_iter_recurse(it, &sub);
            int len = dbus_message_iter_get_array_len(&sub);
            char* data;
            dbus_message_iter_get_fixed_array(&sub,&data,&len);
            return QCString(data,len);
        } else if (arrayType == DBUS_TYPE_DICT_ENTRY) {
            // ### support other types of maps?
            QMap<QString, QVariant> map;
            DBusMessageIter sub;
            dbus_message_iter_recurse(it, &sub);
            if (!dbus_message_iter_has_next(&sub))
                return map;
            do {
                DBusMessageIter itemIter;
                dbus_message_iter_recurse(&sub, &itemIter);
                Q_ASSERT(dbus_message_iter_has_next(&itemIter));
                QString key = qFetchParameter(&itemIter).toString();
                dbus_message_iter_next(&itemIter);
                // FIXME-QT4 map.insertMulti(key, qFetchParameter(&itemIter));
                map.insert(key, qFetchParameter(&itemIter));
            } while (dbus_message_iter_next(&sub));
            return map;
        } else {
            QValueList<QVariant> list;
            DBusMessageIter sub;
            dbus_message_iter_recurse(it, &sub);
            if (!dbus_message_iter_has_next(&sub))
                return list;
            do {
                list.append(qFetchParameter(&sub));
            } while (dbus_message_iter_next(&sub));
            return list;
        }
        break; }
    case DBUS_TYPE_VARIANT: {
        QDBusVariant dvariant;
        DBusMessageIter sub;
        dbus_message_iter_recurse(it, &sub);
        dvariant.signature = QString::fromUtf8(dbus_message_iter_get_signature(&sub));
        dvariant.value = qFetchParameter(&sub);
        // FIXME-QT4 return qVariantFromValue(dvariant);
        return dvariant.value;
    }
#if 0
    case DBUS_TYPE_DICT: {
        QMap<QString, QVariant> map;
        DBusMessageIter sub;
        dbus_message
        if (dbus_message_iter_init_dict_iterator(it, &dictIt)) {
            do {
                map[QString::fromUtf8(dbus_message_iter_get_dict_key(&dictIt))] =
                    qFetchParameter(&dictIt);
            } while (dbus_message_iter_next(&dictIt));
        }
        return map;
        break; }
    case DBUS_TYPE_CUSTOM:
        return qGetCustomValue(it);
        break;
#endif
    default:
        qWarning("Don't know how to handle type %d '%c'", dbus_message_iter_get_arg_type(it), dbus_message_iter_get_arg_type(it));
        return QVariant();
        break;
    }
}

void QDBusMarshall::messageToList(QValueList<QVariant> &list, DBusMessage *message)
{
    Q_ASSERT(message);

    DBusMessageIter it;
    if (!dbus_message_iter_init(message, &it))
        return;

    do {
        list.append(qFetchParameter(&it));
    } while (dbus_message_iter_next(&it));
}

static void qAppendToMessage(DBusMessageIter *it, const QString &str)
{
    QByteArray ba = str.utf8();
    const char *cdata = ba.data();
    dbus_message_iter_append_basic(it, DBUS_TYPE_STRING, &cdata);
}

static QByteArray qDBusListType(const QValueList<QVariant>&);

static QByteArray qDBusNestedListType(const QValueList<QVariant> &list)
{
    QByteArray internal = qDBusListType(list[0].toList());
    if (internal.isNull()) return 0;
    for (uint i = 1; i < list.count(); ++i)
        if (internal != qDBusListType(list[i].toList())) return 0;
    return QCString(DBUS_TYPE_ARRAY_AS_STRING)+internal;
    return internal;
}

static QByteArray qDBusListType(const QValueList<QVariant> &list)
{
    static const char *DBusArgs[] = { 0, 0, DBUS_TYPE_INT32_AS_STRING, DBUS_TYPE_UINT32_AS_STRING,
            DBUS_TYPE_INT64_AS_STRING, DBUS_TYPE_UINT64_AS_STRING, DBUS_TYPE_DOUBLE_AS_STRING, 0,
        0, 0, 0, 0, DBUS_TYPE_ARRAY_AS_STRING DBUS_TYPE_BYTE_AS_STRING };
    static const char *DBusArgs2[] = { 0, 0, DBUS_TYPE_INT16_AS_STRING, 0, 0, DBUS_TYPE_UINT16_AS_STRING,
        DBUS_TYPE_BYTE_AS_STRING };

    // FIXME-QT4 unsigned int tp = list[0].userType();
    int tp = list[0].type();
    if (tp==QVariant::List) return qDBusNestedListType(list); 
/* FIXME-QT4
    if (tp!=QVariant::ByteArray && (tp < QMetaType::Short || tp > QMetaType::UChar) && 
	(tp < QVariant::Int || tp > QVariant::Double))*/
    if (tp!=QVariant::ByteArray &&
    (tp < QVariant::Int || tp > QVariant::Double))
        return 0;

    for (uint i = 1; i < list.count(); ++i) {
    	const QVariant &var = list[i];
	if (var.type() != tp)
            return 0;
    }
    return (tp>127) ? QCString(DBusArgs2[tp-128]) : QCString(DBusArgs[tp]);
}

static void qListToIterator(DBusMessageIter *it, const QValueList<QVariant> &list);

static void qVariantToIterator(DBusMessageIter *it, const QVariant &var)
{
    // these really are static asserts
    Q_ASSERT(QVariant::Invalid == 0);
    Q_ASSERT(QVariant::Int == 16);
    Q_ASSERT(QVariant::Double == 19);

    // FIXME-QT4 switch (var.userType()) {
    switch (var.type()) {
/* FIXME-QT4
    case QMetaType::Short: 
    case QMetaType::UShort:
    case QMetaType::UChar:*/
    case QVariant::Bool: {
        dbus_bool_t value = var.toBool();
        dbus_message_iter_append_basic(it, DBUS_TYPE_BOOLEAN, &value);
        break;
    }
    case QVariant::Int: {
        int value = var.toInt();
        dbus_message_iter_append_basic(it, DBUS_TYPE_INT32, &value);
        break;
    }
    case QVariant::UInt: {
        uint value = var.toUInt();
        dbus_message_iter_append_basic(it, DBUS_TYPE_UINT32, &value);
        break;
    }
    case QVariant::LongLong: {
        Q_LLONG value = var.toLongLong();
        dbus_message_iter_append_basic(it, DBUS_TYPE_INT64, &value);
        break;
    }
    case QVariant::ULongLong: {
        Q_ULLONG value = var.toULongLong();
        dbus_message_iter_append_basic(it, DBUS_TYPE_UINT64, &value);
        break;
    }
    case QVariant::Double: {
        double value = var.toDouble();
        dbus_message_iter_append_basic(it, DBUS_TYPE_DOUBLE, &value);
        break;
    }
    case QVariant::String:
        qAppendToMessage(it, var.toString());
        break;
    case QVariant::StringList: {
        const QStringList list = var.toStringList();
        DBusMessageIter sub;
        dbus_message_iter_open_container(it, DBUS_TYPE_ARRAY,
                                         DBUS_TYPE_STRING_AS_STRING, &sub);
        for (uint s = 0; s < list.count(); ++s)
            qAppendToMessage(&sub, list[s]);
        dbus_message_iter_close_container(it, &sub);
        break;
    }
    case QVariant::ByteArray: {
        const QByteArray array = var.toByteArray();
        const char* cdata = array.data();
            DBusMessageIter sub;
            dbus_message_iter_open_container(it, DBUS_TYPE_ARRAY, DBUS_TYPE_BYTE_AS_STRING, &sub);
        dbus_message_iter_append_fixed_array(&sub, DBUS_TYPE_BYTE, &cdata, array.size());
            dbus_message_iter_close_container(it, &sub);
    break;
    }
    case QVariant::List: {
        const QValueList<QVariant> &list = var.toList();
        QByteArray listType = qDBusListType(list);
        if (listType.isNull()) {
            qWarning("Don't know how to marshall list.");
            break;
        }
        DBusMessageIter sub;
        dbus_message_iter_open_container(it, DBUS_TYPE_ARRAY, listType.data(), &sub);
        qListToIterator(&sub, list);
        dbus_message_iter_close_container(it, &sub);
        break;
    }

    case QVariant::Map: {
        // ### TODO - marshall more than qstring/qstring maps
        const QMap<QString, QVariant> &map = var.toMap();
        DBusMessageIter sub;
        QCString sig;
        sig += DBUS_DICT_ENTRY_BEGIN_CHAR;
        sig += DBUS_TYPE_STRING;
        sig += DBUS_TYPE_STRING;
        sig += DBUS_DICT_ENTRY_END_CHAR;
        //qDebug() << QString::fromAscii(sig.constData());
        dbus_message_iter_open_container(it, DBUS_TYPE_ARRAY, sig.data(), &sub);
        for (QMap<QString, QVariant>::const_iterator mit = map.constBegin();
             mit != map.constEnd(); ++mit) {
            DBusMessageIter itemIterator;
            dbus_message_iter_open_container(&sub, DBUS_TYPE_DICT_ENTRY, 0, &itemIterator);
            qAppendToMessage(&itemIterator, mit.key());
            qAppendToMessage(&itemIterator, mit.data().toString());
            dbus_message_iter_close_container(&sub, &itemIterator);
        }
        dbus_message_iter_close_container(it, &sub);
        break;
    }
/* FIXME-QT4
    case QVariant::UserType: {
        if (var.userType() == QMetaTypeId<QDBusVariant>::qt_metatype_id()) {
            DBusMessageIter sub;
            QDBusVariant dvariant = qvariant_cast<QDBusVariant>(var);
            dbus_message_iter_open_container(it, DBUS_TYPE_VARIANT,
                    dvariant.signature.toUtf8().constData(), &sub);
            qVariantToIterator(&sub, dvariant.value);
            dbus_message_iter_close_container(it, &sub);
            break;
        }
    }*/
    // fall through
    default:
        qWarning("Don't know how to handle type %s", var.typeName());
        break;
    }
}

void qListToIterator(DBusMessageIter *it, const QValueList<QVariant> &list)
{
    if (list.isEmpty())
        return;

    for (uint i = 0; i < list.count(); ++i)
        qVariantToIterator(it, list[i]);
}

void QDBusMarshall::listToMessage(const QValueList<QVariant> &list, DBusMessage *msg)
{
    Q_ASSERT(msg);
    DBusMessageIter it;
    dbus_message_iter_init_append(msg, &it);
    qListToIterator(&it, list);
}

