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


bool Helper::writeKeyboard(const QString &layouts, const QString &variants)
{
    QString xorgFile = "/etc/X11/xorg.conf.d/00-configured-keymap.conf";

    // open file to read
    QFile file(xorgFile);
    if( !file.open( QIODevice::ReadOnly | QIODevice::Text)) {
        qDebug() << "Failed to open.";
        return false;
    }

    // store file content and change layout and variant options
    // changed content is stored in fields
    QTextStream in(&file);
    QStringList fields;
    while(!in.atEnd()) {
        QString line = in.readLine();
        if (line.contains("xkb_layout")) {
            QString newLine = "\tOption\t\"xkb_layout\"\t\"" + layouts + "\"";
            fields << newLine;
        }
        else if (line.contains("xkb_variant")) {
            QString newLine = "\tOption\t\"xkb_variant\"\t\"" + variants + "\"";
            fields << newLine;
        }
        else
            fields << line;
    }
    file.close();

    // open file to write
    if( !file.open( QIODevice::WriteOnly | QIODevice::Text)) {
        qDebug() << "Failed to write.";
        return false;
    }

    // content of fields is saved to the new file
    QTextStream out(&file);
    for (int i = 0; i < fields.size() ; i++)
        out << fields.at(i) << "\n";
    file.close();

    return true;
}

ActionReply Helper::managekeyboard(QVariantMap args)
{
    int code = 0;

    QString layouts = args.value("layouts").toString();
    QString variants = args.value("variants").toString();

    writeKeyboard(layouts,variants);
    return createReply(code);
}



KDE4_AUTH_HELPER_MAIN("org.kde.kcontrol.kcmkeyboard", Helper)
