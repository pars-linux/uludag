/*
 *   Copyright (C) 2010 Ozan Çağlayan <ozan@pardus.org.tr>
 *
 *   This program is free software; you can redistribute it and/or modify
 *   it under the terms of the GNU Library General Public License version 2 as
 *   published by the Free Software Foundation
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details
 *
 *   You should have received a copy of the GNU Library General Public
 *   License along with this program; if not, write to the
 *   Free Software Foundation, Inc.,
 *   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
 */

#ifndef PISIRUNNER_H
#define PISIRUNNER_H

#include <Plasma/AbstractRunner>
#include <KProcess>

#include <QHash>

class QWidget;


/**
 * This class runs programs using the literal name of the binary, much as one
 * would use at a shell prompt.
 */
class PisiRunner : public Plasma::AbstractRunner
{
    Q_OBJECT

    public:
        PisiRunner(QObject *parent, const QVariantList &args);
        ~PisiRunner();

        void match(Plasma::RunnerContext &context);
        void run(const Plasma::RunnerContext &context, const Plasma::QueryMatch &action);

    public Q_SLOTS:
        void slotEndCommandNotFound();
        void slotErrorCommandNotFound();

    protected Q_SLOTS:
        void init();
        void prepareForMatchSession();

    private:
        bool m_enabled;
        QHash<QString, QString> m_packageCache;
        QStringList m_paths;
        KProcess* m_commandNotFound;
};

K_EXPORT_PLASMA_RUNNER(pisi, PisiRunner)

#endif
