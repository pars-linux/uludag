#include <QApplication>
#include <KMessageBox>
#include <KLocale>
#include <QString>
#include <stdio.h>
#include <dbus/dbus.h>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    
    QDBusConnection::sessionBus().connectToBus(QDBusConnection::SessionBus, "tr.org.pardus.comar");


    if (QDBusReply::error()::isValid()) {
        KMessageBox::error(0, i18n(QString("Unable to connect D-Bus: %1.").arg(dbus_err.message).toLatin1()));
        dbus_error_free(&dbus_err);
        return FALSE;
    }

    QDBusMessage dbus_msg = QDBusMessage::createMethodCall("org.freedesktop.PolicyKit.AuthenticationAgent",
            "/",
            "org.freedesktop.PolicyKit.AuthenticationAgent",
            "ObtainAuthorization");

    const char *v_action = "tr.org.pardus.comar.time.clock.set";
    dbus_int32_t v_win = 0;
    dbus_int32_t v_pid = getpid();

    dbus_msg << v_action << v_win << v_pid;
    dbus_msg.setDelayedReply (true);

    QDBusConnection::sessionBus().send *dbus_reply = dbus_connection_send_with_reply_and_block(dbus_conn, dbus_msg, 65535 * 1000, &dbus_err);
    if (dbus_error_is_set(&dbus_err)) {
        KMessageBox::error(0, i18n(QString("Unable to change date: %1.").arg(dbus_err.message).toLatin1()));
        dbus_message_unref(dbus_msg);
        dbus_error_free(&dbus_err);
        return FALSE;
    }

    dbus_bool_t v_grant = FALSE;
    dbus_message_get_args(dbus_reply, &dbus_err,
            DBUS_TYPE_BOOLEAN, &v_grant,
            DBUS_TYPE_INVALID);

    dbus_message_unref(dbus_reply);
    dbus_message_unref(dbus_msg);
    dbus_error_free(&dbus_err);
    dbus_connection_close(dbus_conn);
    dbus_connection_unref(dbus_conn);

    return 0;
    //return app.exec();
}
