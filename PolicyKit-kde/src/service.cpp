
#include <qvariant.h>
#include <qsocketnotifier.h>
#include <kcombobox.h>
#include <klineedit.h>

//policykit header
#include <polkit/polkit.h>
#include <polkit-dbus/polkit-dbus.h>
#include <polkit-grant/polkit-grant.h>

//backport headers
#include "qdbuserror.h"
#include "qdbusmessage.h"

#include "service.h"
#include "authdialog.h"
#include "debug.h"


PolicyService* PolicyService::m_self;

PolicyService::PolicyService(QDBusConnection sessionBus): QObject()
{
    Q_ASSERT(!m_self);
    m_self = this;

    m_sessionBus = sessionBus;
    m_systemBus = QDBusConnection::addConnection(QDBusConnection::SystemBus);
    m_error = NULL;
    m_grant = NULL;
    m_dialog = NULL;
    bool m_authInProgress = false;
    bool m_gainedPrivilege = false;
    bool m_inputBogus = false;

    Debug::printDebug("Registering object: /");
    if (!m_sessionBus.registerObject("/", this))
    {
        QString msg("Could not register \"/\" object, exiting");
        Debug::printError(msg);
        throw msg;
    }

    //TODO: handle name owner changed signal

    m_context = polkit_context_new();
    if (m_context == NULL)
    {
        QString msg("Could not get a new PolKitContext.");
        Debug::printError(msg);
        throw msg;
    }

    polkit_context_set_load_descriptions(m_context);

    //TODO: polkit_context_set_config_changed

    polkit_context_set_io_watch_functions (m_context, polkit_context_add_watch, polkit_context_remove_watch);

    if (!polkit_context_init (m_context, &m_error))
    {
        QString msg("Could not initialize PolKitContext");
        if (polkit_error_is_set(m_error))
        {
            Debug::printError(msg + ": " + polkit_error_get_error_message(m_error));
            polkit_error_free(m_error);
        }
        else
            Debug::printError(msg);

        throw msg;
    }

    //TODO: add kill_timer

}

PolicyService::~PolicyService()
{
    Debug::printDebug("Unregistering object: /");
    m_sessionBus.unregisterObject("/");
}

bool PolicyService::handleMethodCall(const QDBusMessage& message)
{
    Debug::printDebug(QString("DBus method called: '%1'").arg(message.member()));

    if (message.interface() == "org.freedesktop.DBus.Introspectable" && message.member() == "Introspect")
    {
        if (message.count() != 0)
        {
            sendDBusError(message, "No argument expected");
            return false;
        }

        else
            return handleIntrospect(message);
    }

    if (message.interface() == "org.freedesktop.PolicyKit.AuthenticationAgent" && message.member() == "ObtainAuthorization")
    {
        if (message.count() != 3 || message[0].type() != QVariant::String || message[1].type() != QVariant::UInt || message[2].type() != QVariant::UInt)
        {
            sendDBusError(message, "Wrong signature, three arguments expected: (String, UINT, UINT)");
            return false;
        }

        else
            return handleObtainAuthorization(message);
    }

    Debug::printWarning(QString("No such DBus method: '%1'").arg(message.member()));
    return false;
}

void PolicyService::slotBusNameOwnerChanged(const QDBusMessage& msg)
{
    //TODO: exit if not busy
    Debug::printWarning(QString("Session bus name owner changed.").arg(msg.member()));
}

void PolicyService::sendDBusError(const QDBusMessage& message, const QString& errorstr, const QString& errortype)
{
        Debug::printError(QString("Method call error:'%1'  Interface:'%2' Method:'%3'").arg(errorstr).arg(message.interface()).arg(message.member()));

        QDBusError error(errortype, errorstr);
        QDBusMessage reply = QDBusMessage::methodError(message, error);

        m_sessionBus.send(reply);
}

bool PolicyService::handleIntrospect(const QDBusMessage& message)
{
    QDBusMessage reply = QDBusMessage::methodReply(message);

    QString introspection = ""
"<!DOCTYPE node PUBLIC \"-//freedesktop//DTD D-BUS Object Introspection 1.0//EN\"\n"
"\"http://www.freedesktop.org/standards/dbus/1.0/introspect.dtd\">\n"
"<node>\n"
"   <interface name=\"org.freedesktop.DBus.Introspectable\">\n"
"       <method name=\"Introspect\">\n"
"           <arg name=\"xml_data\" type=\"s\" direction=\"out\" />\n"
"       </method>\n"
"   </interface>\n"
"   <interface name=\"org.freedesktop.PolicyKit.AuthenticationAgent\">\n"
"       <method name=\"ObtainAuthorization\" >\n"
"           <!-- IN: PolicyKit action identifier; see PolKitAction -->\n"
"           <arg direction=\"in\" type=\"s\" name=\"action_id\" />\n"
"           <!-- IN: X11 window ID for the top-level X11 window the dialog will be transient for. -->\n"
"           <arg direction=\"in\" type=\"u\" name=\"xid\" />\n"
"           <!-- IN: Process ID to grant authorization to -->\n"
"           <arg direction=\"in\" type=\"u\" name=\"pid\" />\n"
"           <!-- OUT: whether the user gained the authorization -->\n"
"           <arg direction=\"out\" type=\"b\" name=\"gained_authorization\" />\n"
"       </method>\n"
"   </interface>\n"
"</node>";

    Debug::printDebug("Handling introspect() call.");
    reply << QVariant(introspection);
    m_sessionBus.send(reply);

    return true;
}

bool PolicyService::handleObtainAuthorization(const QDBusMessage& message)
{
    QDBusMessage reply = QDBusMessage::methodReply(message);

    Debug::printDebug("Handling obtainAuthorization() call.");

    bool auth = obtainAuthorization(message[0].toString(), message[1].toUInt(), message[2].toUInt());
    reply << QVariant(auth);

    m_sessionBus.send(reply);

    return true;
}

/////////// PolKit IO watch functions ////////////////
void PolicyService::contextWatchActivated(int fd)
{
    Q_ASSERT(m_contextwatches.contains(fd));

    Debug::printDebug("Context watch activated");

    polkit_context_io_func (m_context, fd);
}

int PolicyService::polkit_context_add_watch(PolKitContext *context, int fd)
{
    Debug::printDebug("polkit_context_add_watch: Adding watch...");

    QSocketNotifier *notify = new QSocketNotifier(fd, QSocketNotifier::Read);
    m_self->m_contextwatches[fd] = notify;

    notify->connect(notify, SIGNAL(activated(int)), m_self, SLOT(contextWatchActivated(int)));

    Debug::printDebug("polkit_context_add_watch: Watch added");

    // policykit requires a result != 0
    return 1;
}

void PolicyService::polkit_context_remove_watch(PolKitContext *context, int fd)
{
    Debug::printDebug("polkit_context_remove_watch: Removing watch...");
    Q_ASSERT(m_self->m_contextwatches.contains(fd));

    QSocketNotifier* notify = m_self->m_contextwatches[fd];
    delete notify;

    m_self->m_contextwatches.remove(fd);
    Debug::printDebug("polkit_context_remove_watch: Watch removed");
}

void PolicyService::grantWatchActivated(int fd)
{
    Q_ASSERT(m_grantwatches.contains(fd));
    Q_ASSERT(m_grant != NULL);

    Debug::printDebug("Grant watch activated");

    polkit_grant_io_func (m_grant, fd);
}

int PolicyService::polkit_grant_add_watch(PolKitGrant *grant, int fd)
{
    Q_ASSERT(m_self->m_grant != NULL);
    Debug::printDebug("polkit_grant_add_watch: Adding watch...");

    QSocketNotifier *notify = new QSocketNotifier(fd, QSocketNotifier::Read);
    m_self->m_grantwatches[fd] = notify;

    notify->connect(notify, SIGNAL(activated(int)), m_self, SLOT(grantWatchActivated(int)));

    Debug::printDebug(QString("polkit_grant_add_watch: Watch added, fd= %1").arg(fd));

    return fd;
}

int PolicyService::polkit_grant_add_child_watch(PolKitGrant *grant, pid_t pid)
{
    //this should be called when child dies
    //polkit_grant_child_func (grant, pid_t pid, int exit_code);

    return pid;
}

void PolicyService::polkit_grant_remove_watch(PolKitGrant *grant, int fd)
{
    Q_ASSERT(m_self->m_grant != NULL);

    Debug::printDebug("polkit_grant_remove_watch: Removing watch...");
    Q_ASSERT(m_self->m_grantwatches.contains(fd));

    QSocketNotifier* notify = m_self->m_grantwatches[fd];
    delete notify;

    m_self->m_grantwatches.remove(fd);
    Debug::printDebug("polkit_grant_remove_watch: Watch removed");
}

void PolicyService::polkit_grant_type(PolKitGrant *grant, PolKitResult result, void *data)
{
    Q_ASSERT(m_self->m_dialog != NULL);
    m_self->m_dialog->setType(result);
}

char *PolicyService::polkit_grant_select_admin_user(PolKitGrant *grant, char **adminUsers, void *data)
{
    QStringList list;
    int dialogResult;

    Debug::printDebug("polkit_grant_select_admin_user: Setting user list...");

    for (int n = 0; adminUsers[n] != NULL; n++) {
        list.append(adminUsers[n]);
    }

    m_self->m_dialog->setAdminUsers(list);
    Debug::printDebug("polkit_grant_select_admin_user: Done");
    Debug::printDebug("polkit_grant_select_admin_user: Showing dialog...");

    dialogResult = m_self->m_dialog->exec();
    Debug::printDebug("polkit_grant_select_admin_user: Done");

    const char *selected = m_self->m_dialog->cbUsers->currentText();

    if (dialogResult == QDialog::Rejected)
    {
        Debug::printDebug("polkit_grant_select_admin_user: Dialog rejected");
        return NULL;
    }
    else
    {
        QString msg = QString("polkit_grant_select_admin_user: User(%1) selected.").arg(selected);
        Debug::printDebug(msg);
        return (char *)selected;
    }
}

char *PolicyService::polkit_grant_prompt(const QString &prompt, bool echo)
{
    //TODO: check prompt
    //

    m_dialog->setPrompt(prompt);

    if (echo)
        m_dialog->lePassword->setEchoMode(QLineEdit::Normal);
    else
        m_dialog->lePassword->setEchoMode(QLineEdit::Password);

    int result = m_dialog->exec();

    if (result == QDialog::Rejected)
        return NULL;

    return (char *)m_dialog->getPass();
}

char *PolicyService::polkit_grant_prompt_echo_off(PolKitGrant *grant, const char *prompt, void *data)
{
    Debug::printDebug(QString("In polkit_grant_prompt_echo_off"));
    return m_self->polkit_grant_prompt(prompt, false);
}

char *PolicyService::polkit_grant_prompt_echo_on(PolKitGrant *grant, const char *prompt, void *data)
{
    Debug::printDebug(QString("In polkit_grant_prompt_echo_on"));
    return m_self->polkit_grant_prompt(prompt, true);
}

void PolicyService::polkit_grant_error_message(PolKitGrant *grant, const char *error, void *data)
{
    Debug::printDebug(QString("polkit_grant_error_message: %1").arg(error));
}

void PolicyService::polkit_grant_text_info(PolKitGrant *grant, const char *info, void *data)
{
    Debug::printDebug(QString("polkit_grant_text_info: %1").arg(info));
}

PolKitResult PolicyService::polkit_grant_override_grant_type(PolKitGrant *grant, PolKitResult result, void *data)
{
    Debug::printDebug("In polkit_grant_override_grant_type");
    return result;
}

void PolicyService::polkit_grant_done(PolKitGrant *grant, polkit_bool_t gained_privilege, polkit_bool_t invalid_data, void *data)
{
    Debug::printDebug("In polkit_grant_done");
    m_self->m_gainedPrivilege = gained_privilege;
    m_self->m_inputBogus= invalid_data;
}

bool PolicyService::obtainAuthorization(const QString& actionId, const uint wid, const uint pid)
{
    PolKitError *error = NULL;

    PolKitAction *action = polkit_action_new();
    if (action == NULL)
    {
        Debug::printError("Could not create new action.");
        return false;
    }

    polkit_bool_t setActionResult = polkit_action_set_action_id(action, actionId.ascii());
    if (!setActionResult)
    {
        Debug::printError("Could not set actionid.");
        return false;
    }

    Debug::printDebug("Getting policy cache...");
    PolKitPolicyCache *cache = polkit_context_get_policy_cache(m_context);
    if (cache == NULL)
    {
        Debug::printWarning("Could not get policy cache.");
    //    return false;
    }

    Debug::printDebug("Getting policy cache entry for an action...");
    PolKitPolicyFileEntry *entry = polkit_policy_cache_get_entry(cache, action);
    if (entry == NULL)
    {
        Debug::printWarning("Could not get policy entry for action.");
    //    return false;
    }

    Debug::printDebug("Getting action message...");
    const char *message = polkit_policy_file_entry_get_action_message(entry);
    if (message == NULL)
    {
        Debug::printWarning("Could not get action message for action.");
    //    return false;
    }
    else
    {
        Debug::printDebug(QString("Message of action: '%1'").arg(message));
    }

    DBusError dbuserror;
    dbus_error_init (&dbuserror);
    DBusConnection *bus = dbus_bus_get (DBUS_BUS_SYSTEM, &dbuserror);
    if (bus == NULL) 
    {
        Debug::printError("Could not connect to system bus.");
        return false;
    }

    PolKitCaller *caller = polkit_caller_new_from_pid(bus, pid, &dbuserror);
    if (caller == NULL)
    {
        QDBusError *qerror = new QDBusError((const DBusError *)&dbuserror);
        Debug::printError(QString("Could not define caller from pid: %1").arg(qerror->message()));
        return false;
    }

    m_grant = polkit_grant_new();

    if (m_grant == NULL)
    {
        Debug::printError("PolKitGrant object could not be created");
        return false;
    }

    m_dialog = new AuthDialog();
    Debug::printDebug("AuthDialog created");

    polkit_grant_set_functions(m_grant,
                               polkit_grant_add_watch,
                               polkit_grant_add_child_watch,
                               polkit_grant_remove_watch,
                               polkit_grant_type,
                               polkit_grant_select_admin_user,
                               polkit_grant_prompt_echo_off,
                               polkit_grant_prompt_echo_on,
                               polkit_grant_error_message,
                               polkit_grant_text_info,
                               polkit_grant_override_grant_type,
                               polkit_grant_done,
                               NULL);

    if (!polkit_grant_initiate_auth (m_grant, action, caller)) 
    {
        QString msg = QString("Could not initialize grant");
        Debug::printError(msg);
        throw msg;
    }

    /*
    PolKitResult polkitresult;

    polkitresult = polkit_context_is_caller_authorized(m_context, action, caller, false, &m_error);
    if (polkit_error_is_set (m_error))
    {
        Debug::printError("Could not determine if caller is authorized for this action.");
        return false;
    }

    //TODO: Determine AdminAuthType, user, group...

    try
    {
        AuthDialog* dia = new AuthDialog(message, polkitresult);
        dia->show();
    }
    catch (QString exc)
    {
        Debug::printWarning(exc);
        return false;
    }

    // check again if user is authorized
    polkitresult = polkit_context_is_caller_authorized(m_context, action, caller, false, &m_error);
    if (polkit_error_is_set (m_error))
    {
        Debug::printError("Could not determine if caller is authorized for this action.");
        return false;
    }
    */

    return false;
}

#include "service.moc"
