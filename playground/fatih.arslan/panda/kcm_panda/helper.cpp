#include "helper.h"
#include <iostream>
#include <QDebug>
#include <kdebug.h>

ActionReply Helper::save(const QVariantMap &args)
{
    ActionReply reply;

    int ret = 1; // error code
    bool osdriver = args.value("osdriver").toBool();
    bool vendordriver = args.value("vendordriver").toBool();

        qDebug() << "Os Driver is checked";
        kdDebug(0) << "Os Driver is checked";
    if (osdriver){
        qDebug() << "Os Driver is checked";
        kdDebug(0) << "Os Driver is checked" << endl;
    } else if (vendordriver) {
        qDebug() << "Vendor Driver is checked";
    } else {
        qDebug() << "Nothing is checked";
    }

    /* Just an helperarg example for type string
    QString tempBackgroundConfigName = args.value("tempbackgroundrcfile").toString(); */

    if (ret == 0) {
      return ActionReply::SuccessReply;
    } else {
      reply = ActionReply::HelperErrorReply;
      reply.setErrorCode(5);

      return reply;
    }
}


KDE4_AUTH_HELPER_MAIN("org.kde.kcontrol.kcmpanda", Helper)
