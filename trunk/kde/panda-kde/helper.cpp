#include "helper.h"
#include <iostream>
#include <QDebug>
#include <QProcess>
#include <kdebug.h>

ActionReply Helper::save(const QVariantMap &args)
{
    ActionReply reply;

    int ret = 0; // error code
    bool osdriver = args.value("osdriver").toBool();
    bool vendordriver = args.value("vendordriver").toBool();

    QStringList cliOsArgs;
    QStringList cliVendorArgs;
    cliOsArgs << "up" << "os";
    cliVendorArgs << "up" << "vendor";
    QString program = "/usr/bin/panda-cli.py";

    QProcess *p = new QProcess(this);

    if (osdriver){
        p->start(program, cliOsArgs);
        p->waitForFinished();
        QByteArray currentDriver = p->readAllStandardOutput();
        QString osOutput = QString(currentDriver).trimmed();
        qDebug() << "OS: " << osOutput;
    } else if (vendordriver) {
        p->start(program, cliVendorArgs);
        p->waitForFinished();
        QByteArray currentDriver = p->readAllStandardOutput();
        QString vendorOutput = QString(currentDriver).trimmed();
        qDebug() << "Vendor: " << vendorOutput;
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
