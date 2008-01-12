/* qdbuserror.h QDBusError object
 *
 * Copyright (C) 2005 Harald Fernengel <harry@kdevelop.org>
 * Copyright (C) 2005 Kevin Krammer <kevin.krammer@gmx.at>
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

#ifndef QDBUSERROR_H
#define QDBUSERROR_H

#include "dbus/qdbusmacros.h"
#include <qstring.h>

struct DBusError;

/**
 * @brief Class for transporting DBus errors
 *
 * A DBus error has two parts: an error name (see section
 * @ref dbusconventions-errorname) and a message string detailing the error in
 * human presentable form.
 */
class QDBUS_EXPORT QDBusError
{
public:
    /**
     * @brief Creates an error object from an C API DBus error object
     *
     * @param error a pointer to the C API DBus error
     */
    QDBusError(const DBusError *error = 0);

    /**
     * @brief Creates an error object for its two given components
     *
     * @param error a DBus error name
     * @param message the potentially i18n'ed error description message
     *
     * @see name()
     */
    QDBusError(const QString& error, const QString& message);

    /**
     * @brief Returns the DBus error name
     *
     * See section @ref dbusconventions-errorname for details.
     *
     * @return the DBus error name
     *
     * @see message()
     */
    inline QString name() const { return nm; }

    /**
     * @brief Returns a string describing the error
     *
     * The message is meant to further detail or describe the error.
     * It is usually a translated error message meant for direct
     * presentation to the user.
     *
     * @return the error's message
     *
     * @see name()
     */
    inline QString message() const { return msg; }

    /**
     * @brief Returns whether the error object is valid
     *
     * A QDBusError is considered valid if both name and message are set.
     *
     * @return @c true if neither name nor message is @c QString::null
     */
    inline bool isValid() const { return !nm.isNull() && !msg.isNull(); }

private:
    QString nm, msg;
};

#endif
