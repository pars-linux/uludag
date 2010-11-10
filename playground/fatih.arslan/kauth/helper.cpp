#include "helper.h"
#include <iostream>

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


bool Helper::writeKeyboard(const QString &variants, const QString &layouts)
{
    QString hede;
    QString hodo;

    hede = variants;
    hodo = layouts;


    return true;
}

ActionReply Helper::managekeyboard(QVariantMap args)
{
    int code = 0;

    QString a = args.value("layout").toString();
    QString b = args.value("variant").toString();

    writeKeyboard(a,b);
    return createReply(code);
}



KDE4_AUTH_HELPER_MAIN("org.kde.kcontrol.kcmkeyboard", Helper)
