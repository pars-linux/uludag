#include "helper.h"
#include <iostream>
#include <QStringList>
#include <QFile>
#include <QTextStream>
#include <QDebug>

ActionReply Helper::createReply(int code, const QVariantMap *returnData)
{
    ActionReply reply;

    if (code) {
        reply = ActionReply::HelperError;
        reply.setErrorCode(code);
    } else {
        reply = ActionReply::SuccessReply;
    }

    if (returnData)
        reply.setData(*returnData);

    return reply;
}


bool Helper::writeLocale(const QString &locale)
{
    QString mudurFile = "/etc/conf.d/mudur";
    QString mudurNewFile = "/etc/conf.d/mudurnew";

    // open file to read
    QFile file(mudurFile);
    if( !file.open( QIODevice::ReadOnly | QIODevice::Text)) {
        qDebug() << "Failed to read.";
        return false;
    }

    // read whole file, replace language string and create a new string
    QString output;
    QTextStream in(&file);
    while (!in.atEnd()) {
        QString line = in.readLine();
        if (line.contains("language=")) {
            QString newline = "language=\"" + locale + "\"\n";
            qDebug() << newline << endl;
            output.append(newline);
        } else {
            QString newline = line + "\n";
            output.append(newline);
        }
    }
    file.close();

    // create a new file to write
    QFile fileNew(mudurNewFile);
    if( !fileNew.open( QIODevice::WriteOnly | QIODevice::Text)) {
        qDebug() << "Failed to write.";
        return false;
    }
    QTextStream out(&fileNew);
    out << output; //write the output to the new file
    fileNew.close();

    return true;
}

ActionReply Helper::managelocale(QVariantMap args)
{
    int code = 0;

    QString locale = args.value("locale").toString();

    code = (writeLocale(locale) ? 0 : WriteLocaleError);
    return createReply(code);
}

KDE4_AUTH_HELPER_MAIN("org.kde.kcontrol.kcmlocale", Helper)
