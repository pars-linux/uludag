#include <Python.h>
#include <gtk/gtk.h>
#include "pypulse.h"

static int connection_state = 0;

int context_state_callback(pa_context* c, void* userdata)
{
	printf("context_state_callback pa_context* c assertion\n");
	g_assert(c);

	switch (pa_context_get_state(c)){
		case PA_CONTEXT_CONNECTING:
		printf("INF: connecting..\n");
		break;

	case PA_CONTEXT_AUTHORIZING:
		printf("INF: authorizing..\n");
		break;

	case PA_CONTEXT_SETTING_NAME:
		printf("INF: settings name..\n");
		break;

	case PA_CONTEXT_READY: {
		g_assert(c);
		printf("INF: connection seems  OK\n");
		connection_state = 1; // for is_valid
		// TODO: add pa_context_set_subscribe_callback !
		pa_operation* o;
		pa_context_set_subscribe_callback(c, subscribe_cb, NULL);
		if (!(o = pa_context_subscribe(c, (pa_subscription_mask_t)
														(PA_SUBSCRIPTION_MASK_SINK|
														PA_SUBSCRIPTION_MASK_SOURCE|
														PA_SUBSCRIPTION_MASK_SINK_INPUT|
														PA_SUBSCRIPTION_MASK_CLIENT|
														PA_SUBSCRIPTION_MASK_SERVER), NULL, NULL))) {
			printf("pa_context_subscribe() failed");
			return;
		}
		break;
		}
		case PA_CONTEXT_TERMINATED:
			printf("WAR: context terminated\n");
			return 1;
			break;
			case PA_CONTEXT_FAILED:
			default:
			printf("Connection failure: %s\n", pa_strerror(pa_context_errno(c)));
			return 1;
	}
}

/*
static PyObject* py_context_set_subscribe_callback()
{
	pa_operation* o;
	// c->context
	if(!(o = pa_context_subscribe(context, (pa_subscription_mask_t)
																					(PA_SUBSCRIPTION_MASK_SINK|
																						PA_SUBSCRIPTION_MASK_SOURCE|
																						PA_SUBSCRIPTION_MASK_SINK_INPUT|
																						PA_SUBSCRIPTION_MASK_CLIENT|
																						PA_SUBSCRIPTION_MASK_SERVER), NULL, NULL))){
		printf("py_context_set_subscribe_callback: pa_context_subscribe failed\n");
		Py_INCREF(Py_False);
		return Py_False;
	}else{
		Py_INCREF(Py_True);
		return Py_True;
	}
}
*/

static PyObject* main_event_loop()
{
	gtk_main();
	return Py_BuildValue("i", 0);
}


void safe_quit()
{
	printf("WAR: quitting\n");
	/* prepare and quit */
	if(context) pa_context_unref(context);
	printf("WAR: returning ret\n");
}


static PyObject* check_connection_flag()
{
	if (connection_state){
		Py_INCREF(Py_True);
		return Py_True;
	}else{
		Py_INCREF(Py_False);
		return Py_False;
	}
}

/* run this after py_context_connect()
* if you want to get notified when
* an event occurs.
* Notification starts here
*/
static PyObject* py_context_set_state_callback()
{
	pa_context_set_state_callback(context, context_state_callback, NULL);
	Py_INCREF(Py_None);
	return Py_None;
}


/* connect to default running pulse server
* returns -1 on fail, 0 on success
*/
static PyObject* py_context_connect()
{
	// TODO: change return values ?
	if(pa_context_connect(context, NULL, 0, NULL < 0)){
		return Py_BuildValue("i", -1);
	}
	return Py_BuildValue("i",0);
}


/* main initialize function for pulseaudio
* first step
*/
static PyObject* py_initialize()
{
	pa_glib_mainloop* m = pa_glib_mainloop_new(g_main_context_default()); // instead of pa_mainloop_new()
	printf("ASSERT: m assertion.. \n");
	g_assert(m);
	pa_mainloop_api *api = pa_glib_mainloop_get_api(m);
	printf("ASSERT: api assertion... \n");
	g_assert(api);
	context = pa_context_new(api, "dummy");
	printf("ASSERT: context assertion...\n");
	g_assert(context);

	//pa_context_set_state_callback(context, context_state_callback, NULL);
	//pa_context_connect(context, NULL, 0, NULL);
	return Py_BuildValue("i",0);
}


static PyMethodDef Methods[] =
{
	{"initialize", py_initialize, METH_VARARGS},
	{"context_set_state_callback", py_context_set_state_callback, METH_VARARGS},
	{"context_connect", py_context_connect, METH_VARARGS},
	//{"check_values", check_callback, METH_VARARGS},
	{"is_connection_valid",check_connection_flag , METH_VARARGS},
	//{"context_set_subscribe_callback",py_context_set_subscribe_callback , METH_VARARGS},
	{"loop", main_event_loop, METH_VARARGS},
	{NULL , NULL, 0, NULL}
};


PyMODINIT_FUNC
initpypulse(void)
{
	PyObject* m;
	m = Py_InitModule("pypulse", Methods);
	if(m == NULL) return;
}
