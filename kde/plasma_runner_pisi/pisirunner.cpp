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

#include "pisirunner.h"

#include <QVariant>

#include <KRun>
#include <KIcon>
#include <KLocale>
#include <KStandardDirs>

#include <plasma/theme.h>

PisiRunner::PisiRunner(QObject *parent, const QVariantList &args)
    : Plasma::AbstractRunner(parent, args)
{
    setObjectName("pisi");
    m_enabled = true;
    //setPriority(AbstractRunner::HighestPriority);
}

PisiRunner::~PisiRunner()
{
}

void PisiRunner::init()
{
    connect(this, SIGNAL(prepare()), this, SLOT(prepareForMatchSession()));
}

void PisiRunner::prepareForMatchSession()
{
    // Get $PATH
    m_paths = QProcessEnvironment::systemEnvironment().value("PATH").split(":");

    // Load the command-not-found db once
    m_commandNotFound = new KProcess(this);
    (*m_commandNotFound) << "command-not-found" << "--dump";
    m_commandNotFound->setOutputChannelMode(KProcess::OnlyStdoutChannel);
    connect(m_commandNotFound, SIGNAL(finished(int, QProcess::ExitStatus)),
            SLOT(slotEndCommandNotFound()));
    connect(m_commandNotFound, SIGNAL(error(QProcess::ProcessError)),
            SLOT(slotErrorCommandNotFound()));
    m_commandNotFound->start();
}

void PisiRunner::slotErrorCommandNotFound()
{
    // Disable plugin as the db could not be read
    m_enabled = false;
}

void PisiRunner::slotEndCommandNotFound()
{
    while (!m_commandNotFound->atEnd()) {
        // Populate QHash with (fullpath, package) pairs
        QString line = m_commandNotFound->readLine();
        line.chop(1);
        m_packageCache.insert(line.section(",", 0, 0), line.section(",", 1, 1));
    }

    if (m_packageCache.size() == 0)
        m_enabled = false;
}

void PisiRunner::match(Plasma::RunnerContext &context)
{
    if (!m_enabled)
        return;

    QString query = context.query();
    QString package = "";

    if (!KStandardDirs::findExe(query).isEmpty())
        // Don't show redundant match if the package is already installed
        return;

    if (query.length() < 2)
        // Skip short queries
        return;

    for (int i = 0; i < m_paths.size(); ++i) {
        QString fullPath = m_paths.at(i) + "/" + query;
        if (m_packageCache.contains(fullPath)) {
            package = m_packageCache.value(fullPath);
            break;
        }
        if (!context.isValid())
            // The query may be invalidated by the main thread
            return;
    }

    // Check if the query satisfies a binary shipped within any package
    if (!package.isEmpty()) {
        Plasma::QueryMatch match(this);
        match.setId(query);

        // Keep the package name within QueryMatch
        match.setData(QVariant(package));

        match.setType(Plasma::QueryMatch::ExactMatch);
        match.setIcon(KIcon("application-x-pisi"));
        match.setText(package);
        match.setSubtext(i18n("Install '%1' containing the application '%2'", package, query));
        match.setRelevance(0.7);
        context.addMatch(query, match);
    }
}

void PisiRunner::run(const Plasma::RunnerContext &context, const Plasma::QueryMatch &match)
{
    QMutexLocker lock(bigLock());
    Q_UNUSED(match);

    // Run installer giving the package name as the argument
    KRun::runCommand(QString("pm-install --from-repository %1").arg(match.data().toString()) , NULL);
}

#include "pisirunner.moc"
