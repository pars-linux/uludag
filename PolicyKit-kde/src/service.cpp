/*
  Copyright (c) 2007,2008 TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

//headers required for SIGCHLD handling and strdup
#include <csignal>
#include <cstring>

//kde and qt headers
#include <qvariant.h>
#include <qsocketnotifier.h>
#include <qtimer.h>
#include <kcombobox.h>
#include <klineedit.h>
#include <kcmdlineargs.h>
#include <kapplication.h>

//policykit headers
#include <polkit/polkit.h>
#include <polkit-dbus/polkit-dbus.h>
#include <polkit-grant/polkit-grant.h>

//dbus backport headers
#include "qdbuserror.h"
#include "qdbusmessage.h"

//own headers
#include "service.h"
#include "policykitkde.h"
#include "authdialog.h"
#include "debug.h"

using namespace std;

PolicyService* PolicyService::m_self;

PolicyService::PolicyService(QDBusConnection sessionBus): QObject()
{
    //since kde strips 'no', we have to write -exit to control no-exit option
    if (KCmdLineArgs::parsedArgs()->isSet("-exit"))
    {
        //exit, if no-exit option is not set
        Debug::printWarning("no-exit option is not set, setting timer to exit in 30 seconds...");
        QTimer::singleShot(30000, this, SLOT(quitSlot(void)));
    }
    else
        Debug::printDebug("no-exit option is set, not quiting");

    Q_ASSERT(!m_self);
    m_self = this;

    m_sessionBus = sessionBus;
    m_error = NULL;
    m_grant = NULL;
    m_dialog = NULL;
    bool m_authInProgress = false;
    bool m_gainedPrivilege = false;
    bool m_inputBogus = false;
    m_uniqueSessionName = m_sessionBus.uniqueName();

    Debug::printDebug("Registering object: /");
    if (!m_sessionBus.registerObject("/", this))
    {
        QString msg("Could not register \"/\" object, exiting");
        Debug::printError(msg);
        throw msg;
    }

    //connect all signals to this method
    m_sessionBus.connect(this, SLOT(handleDBusSignals(const QDBusMessage&)));

    m_context = polkit_context_new();
    if (m_context == NULL)
    {
        QString msg("Could not get a new PolKitContext.");
        Debug::printError(msg);
        throw msg;
    }

    polkit_context_set_load_descriptions(m_context);
    polkit_context_set_config_changed (m_context, polkit_config_changed, NULL);

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
}

void PolicyService::quitSlot()
{
    Debug::printWarning("Timeout limit reached and no-exit option is not set, quiting...");
    KApplication::kApplication()->quit();

    //TODO: Do last jobs
}

PolicyService::~PolicyService()
{
    Debug::printDebug(QString("Unregistering object: %1").arg(POLICYKITKDE_OBJECTNAME));
    m_sessionBus.unregisterObject(POLICYKITKDE_OBJECTNAME);
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
        {
            handleIntrospect(message);
            return true;
        }
    }

    else if (message.interface() == POLICYKITKDE_INTERFACENAME && message.member() == "ObtainAuthorization")
    {
        if (message.count() != 3 || message[0].type() != QVariant::String || message[1].type() != QVariant::UInt || message[2].type() != QVariant::UInt)
        {
            sendDBusError(message, "Wrong signature, three arguments expected: (String, UINT, UINT)");
            return false;
        }
        else
        {
            handleObtainAuthorization(message);
            return true;
        }
    }

    else
    {
        Debug::printWarning(QString("No such DBus method: '%1'").arg(message.member()));
        return false;
    }
}

void PolicyService::handleDBusSignals(const QDBusMessage& msg)
{

    // our service has changed
    if (msg.member() == "NameOwnerChanged" && msg.count() == 3 && msg[1].toString() == m_uniqueSessionName)
    {
        Debug::printWarning(QString("Session bus name owner changed: service name='%1', old owner='%2', new owner='%3'").arg(msg[0].toString()).arg(msg[1].toString()).arg(msg[2].toString()));

        //TODO: exit if not busy

    }
}

void PolicyService::sendDBusError(const QDBusMessage& message, const QString& errorstr, const QString& errortype)
{
        Debug::printError(QString("Method call error:'%1'  Interface:'%2' Method:'%3'").arg(errorstr).arg(message.interface()).arg(message.member()));

        QDBusError error(errortype, errorstr);
        QDBusMessage reply = QDBusMessage::methodError(message, error);

        m_sessionBus.send(reply);
}

void PolicyService::handleIntrospect(const QDBusMessage& message)
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
}

void PolicyService::handleObtainAuthorization(const QDBusMessage& message)
{
    Debug::printDebug("Handling obtainAuthorization() call.");

    /*
    if (m_authInProgress)
    {
        QString msg = QString("Already authenticating by another agent");
        Debug::printError(msg);

        // send dbus error
        QDBusMessage dbusError = QDBusMessage::methodError(message, QDBusError(POLICYKITKDE_BUSNAME, msg));
        m_sessionBus.send(dbusError);
    }
    */

    //TODO: Check if another request is in progress
    //m_authInProgress = true;

    obtainAuthorization(message[0].toString(), message[1].toUInt(), message[2].toUInt(), message);

    QDBusMessage reply = QDBusMessage::methodReply(message);

    //in order to send boolean values, a second integer parameter is required by QVariant class
    reply << QVariant(true, 1);

    m_sessionBus.send(reply);

    m_authInProgress = false;
   /*

    */
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

    Debug::printDebug(QString("polkit_grant_add_watch: Watch added, fd=%1").arg(fd));

    return fd;
}

int PolicyService::polkit_grant_add_child_watch(PolKitGrant *grant, pid_t pid)
{
    Debug::printDebug("polkit_grant_add_child_watch: Addind watch");

    //TODO: Do this in a KDE/Qt way
    struct sigaction *sigac = (struct sigaction *)calloc(1, sizeof(struct sigaction));

    sigac->sa_sigaction = m_self->polkit_grant_sigchld_handler;
    sigac->sa_flags = SA_SIGINFO;

    if (sigaction(SIGCHLD, sigac, NULL) != 0)
        Debug::printError("polkit_grant_add_child_watch: SIGCHLD action could not be changed.");
    else
        Debug::printDebug(QString("polkit_grant_add_child_watch: Watch added for %1").arg(pid));

    free(sigac);
    return pid;
}

void PolicyService::polkit_grant_sigchld_handler(int sig, siginfo_t *info, void *ucontext)
{
    Debug::printWarning(QString("polkit_grant_sigchld_handler: Received SIGCHLD, child exit status=%1 PID=%2").arg(info->si_status).arg(info->si_pid));

    //this should be called when child dies
    polkit_grant_child_func (m_self->m_grant, info->si_pid, info->si_status);
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

////////////////////// polkit-grant functions ////////////////////////////

void PolicyService::polkit_grant_type(PolKitGrant *grant, PolKitResult result, void *data)
{
    Q_ASSERT(m_self->m_dialog != NULL);

    Debug::printWarning(QString("polkit_grant_type: Type of authentication dialog is set to \"%1\"").arg(polkit_result_to_string_representation(result)));
    m_self->m_dialog->setType(result);
}

void PolicyService::polkit_config_changed(PolKitContext *context, void *data)
{
    Debug::printWarning("polkit_config_changed: PolicyKit configuration changed");
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

    char *selected = strdup(m_self->m_dialog->cbUsers->currentText());

    if (dialogResult == QDialog::Rejected)
    {
        Debug::printDebug("polkit_grant_select_admin_user: Dialog rejected");
        return NULL;
    }
    else
    {
        QString msg = QString("polkit_grant_select_admin_user: User(%1) selected.").arg(selected);
        Debug::printDebug(msg);
        return selected;
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
    {
        Debug::printDebug("polkit_grant_prompt: Dialog cancelled");
        return NULL;
    }

    //In order to be freed by PolKitGrant class without crash, this is needed
    char *answer = strdup(m_dialog->getPass());
    return answer;
}

char *PolicyService::polkit_grant_prompt_echo_off(PolKitGrant *grant, const char *prompt, void *data)
{
    Debug::printDebug(QString("polkit_grant_prompt_echo_off: prompt=\"%1\"").arg(prompt));
    return m_self->polkit_grant_prompt(prompt, false);
}

char *PolicyService::polkit_grant_prompt_echo_on(PolKitGrant *grant, const char *prompt, void *data)
{
    Debug::printDebug(QString("polkit_grant_prompt_echo_on: prompt=\"%1\"").arg(prompt));
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
    Debug::printDebug(QString("In polkit_grant_done: gained_privilege=%1 invalid_data=%2").arg(gained_privilege).arg(invalid_data));
    m_self->m_gainedPrivilege = gained_privilege;
    m_self->m_inputBogus= invalid_data;
    QApplication::eventLoop()->exit();
}

void PolicyService::obtainAuthorization(const QString& actionId, const uint wid, const uint pid, const QDBusMessage& messageToReply)
{
    PolKitError *error = NULL;

    PolKitAction *action = polkit_action_new();
    if (action == NULL)
    {
        QString msg = QString("Could not create new action");
        Debug::printError(msg);
        throw msg;
    }

    polkit_bool_t setActionResult = polkit_action_set_action_id(action, actionId.ascii());
    if (!setActionResult)
    {
        QString msg = QString("Could not set actionid.");
        Debug::printError(msg);
        throw msg;
    }

    Debug::printDebug("Getting policy cache...");
    PolKitPolicyCache *cache = polkit_context_get_policy_cache(m_context);
    if (cache == NULL)
        Debug::printWarning("Could not get policy cache.");

    Debug::printDebug("Getting policy cache entry for an action...");
    PolKitPolicyFileEntry *entry = polkit_policy_cache_get_entry(cache, action);
    if (entry == NULL)
        Debug::printWarning("Could not get policy entry for action.");

    Debug::printDebug("Getting action message...");
    const char *message = polkit_policy_file_entry_get_action_message(entry);

    if (message == NULL)
        Debug::printWarning("Could not get action message for action.");
    else
        Debug::printDebug(QString("Message of action: '%1'").arg(message));

    DBusError dbuserror;
    dbus_error_init (&dbuserror);
    DBusConnection *systemBus = dbus_bus_get (DBUS_BUS_SYSTEM, &dbuserror);
    if (systemBus == NULL) 
    {
        QString msg = QString("Could not connect to system bus.");
        Debug::printError(msg);
        throw msg;
    }

    PolKitCaller *caller = polkit_caller_new_from_pid(systemBus, pid, &dbuserror);
    if (caller == NULL)
    {
        QDBusError *qerror = new QDBusError((const DBusError *)&dbuserror);
        QString msg = QString("Could not define caller from pid: %1").arg(qerror->message());
        Debug::printError(msg);
        throw msg;
    }

    //TODO: Add vendor icon support

    for (int i = 0; i < POLICYKITKDE_MAX_TRY; i++)
    {
        m_grant = polkit_grant_new();

        if (m_grant == NULL)
        {
            QString msg = QString("PolKitGrant object could not be created");
            Debug::printError(msg);
            throw msg;
        }

        QString qMessage = QString(message);
        m_dialog = new AuthDialog(qMessage);
        Debug::printDebug("AuthDialog created.");

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

        // This workaround used for to aviod ourself from a race condition,
        // polkit_grant_done must return before the following privilege check
        QApplication::eventLoop()->exec();

        if (m_gainedPrivilege)
        {
            Debug::printDebug("obtain_authorization: Authentication succeeded, sending DBus reply...");

            //send dbus reply
            QDBusMessage reply = QDBusMessage::methodReply(messageToReply);

            reply << QVariant(m_gainedPrivilege);
            m_sessionBus.send(reply);

            break;
        }
        else
            Debug::printDebug("obtain_authorization: Authentication failed, trying again...");
    }

    Debug::printDebug("obtain_authorization returning");
}

#include "service.moc"
