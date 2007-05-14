/*
** Copyright (c) 2004, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

/*
** ulubot - jabber.c
** connection handling
*/

#include "common.h"

static iksparser *j_parser;
static iksid *j_user;
static int authorized;

static void
on_log (void *ptr, const char *data, size_t size, int is_incoming)
{
	log_protocol (data, is_incoming, iks_is_secure (j_parser));
}

static int
on_stream (void *ptr, int type, iks *node)
{
	iks *x;
	ikspak *pak;

	switch (type) {
		case IKS_NODE_START:
			/* x = iks_make_auth (j_user, prefs.pass, iks_find_attrib (node, "id"));
			iks_insert_attrib (x, "id", "auth");
			iks_send (j_parser, x);
			iks_delete (x); */
			break;

		case IKS_NODE_NORMAL:
			if (strcmp("stream:features", iks_name(node)) == 0) {
				if (authorized) {
					int features;
					features = iks_stream_features(node);
					if (features & IKS_STREAM_BIND) {
						x = iks_make_resource_bind(j_user);
						iks_send(j_parser, x);
						iks_delete(x);
					}
					if (features & IKS_STREAM_SESSION) {
						x = iks_make_session();
						iks_insert_attrib(x, "id", "auth");
						iks_send(j_parser, x);
						iks_delete(x);
					}
				} else {
					iks_start_sasl(j_parser, IKS_SASL_DIGEST_MD5, j_user->user, prefs.pass);
				}
				break;
			} else if (strcmp("failure", iks_name(node)) == 0) {
				log_event ("Hata: SASL başarısız!");
				return IKS_HOOK;
			} else if (strcmp("success", iks_name(node)) == 0) {
				authorized = 1;
				iks_send_header(j_parser, j_user->server);
				break;
			}
		
			pak = iks_packet (node);
			if (pak->type == IKS_PAK_MESSAGE) {
				// process incoming messages
				command_parse (pak->from->partial, iks_find_cdata (node, "body"));
			} else if (pak->type == IKS_PAK_S10N) {
				// always accept subscriptions
				if (pak->subtype == IKS_TYPE_SUBSCRIBE) {
					x = iks_make_s10n (IKS_TYPE_SUBSCRIBED, pak->from->full, NULL);
					iks_send (j_parser, x);
					iks_delete (x);
				}
			} else if (pak->type == IKS_PAK_IQ) {
				if (iks_strcmp (pak->id, "auth") == 0) {
					// auth response
					if (pak->subtype == IKS_TYPE_RESULT) {
						log_event ("Bağlandık.");
						x = iks_make_iq (IKS_TYPE_GET, IKS_NS_ROSTER);
						iks_send (j_parser, x);
						iks_delete (x);
						x = iks_make_pres (IKS_SHOW_AVAILABLE, NULL);
						iks_send (j_parser, x);
						iks_delete (x);
					} else {
						log_event ("Hata: kullanıcı doğrulama başarısız oldu!");
						return IKS_HOOK;
					}
				}
			}
			break;

		case IKS_NODE_STOP:
		case IKS_NODE_ERROR:
			log_event ("Hata: XMPP stream hatası!");
			return IKS_HOOK;
	}
	if (node) iks_delete (node);

	return IKS_OK;
}

int
jabber_connect (void)
{
	int e;

	j_parser = iks_stream_new (IKS_NS_CLIENT, NULL, (iksStreamHook *) on_stream);
	j_user = iks_id_new (iks_parser_stack (j_parser), prefs.jid);
	if (j_user->resource == NULL) {
		char buf[512];
		sprintf (buf, "%s/sozluk", j_user->partial);
		j_user = iks_id_new (iks_parser_stack (j_parser), buf);
	}
	log_event ("Bağlanmayı deniyorum (%s)", j_user->full);
	iks_set_log_hook (j_parser, (iksLogHook *) on_log);

	authorized = 0;

	e = iks_connect_tcp (j_parser, j_user->server, IKS_JABBER_PORT);
	switch (e) {
		case IKS_OK:
			return 0;
		case IKS_NET_NODNS:
		case IKS_NET_NOCONN:
		default:
			log_event ("jabber bork");
			return -1;
	}
}

int
jabber_poll (void)
{
	int e;

	e = iks_recv (j_parser, 1);
	if (IKS_OK != e) {
		log_event ("Hata: iletişim hatası (%d)", e);
		return -1;
	}
	return 0;
}

void
jabber_send (char *user, char *message)
{
	iks *x;

	x = iks_make_msg (IKS_TYPE_NONE, user, message);
	iks_send (j_parser, x);
	iks_delete (x);
}

void
jabber_disconnect (void)
{
	iks_parser_delete (j_parser);
}
