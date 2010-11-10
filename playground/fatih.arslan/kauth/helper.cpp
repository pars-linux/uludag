#include "helper.h"
#include <iostream>
#include <QStringList>
#include <QFile>
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
    QFile file("/etc/X11/xorg.conf.d/00-configured-keymap.conf");

    qDebug() << layouts;
    qDebug() << variants;

    if (!file.exists()) {
        qDebug() << "The file does not exist";
        return 0;
    }
    // It exists, open it
    if( !file.open( QIODevice::ReadOnly ) )
    {
        qDebug() << "Failed to open.";
        return 0;
    }

    // It opened, now we need to close it
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
