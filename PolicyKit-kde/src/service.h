
#ifndef SERVICE_H
#define SERVICE_H

#include <polkit/polkit.h>
#include <polkit-grant/polkit-grant.h>

#include <qobject.h>
#include <qmap.h>
#include <qsocketnotifier.h>

#include "qdbusconnection.h"
#include "qdbusobject.h"

class AuthDialog;

class PolicyService: public QObject, public QDBusObjectBase
{
    Q_OBJECT

public:
    PolicyService(QDBusConnection sessionBus);
    virtual ~PolicyService();

protected:
    bool handleMethodCall(const QDBusMessage& message);
    bool handleIntrospect(const QDBusMessage& message);
    bool handleObtainAuthorization(const QDBusMessage& message);
    void sendDBusError(const QDBusMessage& message, const QString& errortype, const QString& errorstr = "org.freedesktop.DBus.Error.InvalidSignature");
    bool obtainAuthorization(const QString& actionId, const uint wid, const uint pid);

protected slots:
    void slotBusNameOwnerChanged(const QDBusMessage& msg);
    void contextWatchActivated(int fd);
    void grantWatchActivated(int fd);

private:
    QDBusConnection m_sessionBus;
    AuthDialog *m_dialog;

    PolKitContext *m_context;
    PolKitGrant *m_grant;
    PolKitError *m_error;

    bool m_authInProgress;
    bool m_gainedPrivilege;
    bool m_inputBogus;
    static PolicyService* m_self;

    QMap<int, QSocketNotifier*> m_contextwatches;
    QMap<int, QSocketNotifier*> m_grantwatches;

    static int polkit_context_add_watch(PolKitContext *context, int fd);
    static void polkit_context_remove_watch(PolKitContext *context, int fd);

    // functions required by polkit_grant_set_functions
    static int polkit_grant_add_watch(PolKitGrant *grant, int fd);
    static int polkit_grant_add_child_watch(PolKitGrant *grant, pid_t pid);
    static void polkit_grant_remove_watch(PolKitGrant *grant, int fd);
    static void polkit_grant_type(PolKitGrant *grant, PolKitResult result, void *data);
    static char *polkit_grant_select_admin_user(PolKitGrant *grant, char **adminUsers, void *data);
    static char *polkit_grant_prompt_echo_off(PolKitGrant *grant, const char *prompt, void *data);
    static char *polkit_grant_prompt_echo_on(PolKitGrant *grant, const char *prompt, void *data);
    char *polkit_grant_prompt(const QString &prompt, bool echo);
    static void polkit_grant_error_message(PolKitGrant *grant, const char *error, void *data);
    static void polkit_grant_text_info(PolKitGrant *grant, const char *info, void *data);
    static PolKitResult polkit_grant_override_grant_type(PolKitGrant *grant, PolKitResult result, void *data);
    static void  polkit_grant_done(PolKitGrant *grant, polkit_bool_t gained_privilege, polkit_bool_t invalid_data, void *data);
    static void polkit_config_changed(PolKitContext *context, void *data);
};

#endif
