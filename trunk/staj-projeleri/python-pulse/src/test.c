#include <Python.h>
#include <gtk/gtk.h>
#include "pypulse.h"




int context_state_callback(pa_context* c)
{
    g_assert(c);

    switch (pa_context_get_state(c)) {
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



static PyObject* enter_loop()
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


static PyObject* context_connect()
{
    pa_glib_mainloop* m = pa_glib_mainloop_new(g_main_context_default()); // instead of pa_mainloop_new()
    printf("m assertion.. \n");
    g_assert(m);
    pa_mainloop_api *api = pa_glib_mainloop_get_api(m);
    printf("api assertion... \n");
    g_assert(api);
    context = pa_context_new(api, "dummy");
    printf("context assertion...\n");
    g_assert(context);
	
    pa_context_set_state_callback(context, context_state_callback, NULL);
	
    if(pa_context_connect(context, NULL, 0, NULL) < 0){
      printf("connection failed\n");
      safe_quit();
    }

    printf("***done***\n");
    return Py_BuildValue("i",0);

}


static PyMethodDef Methods[] = {
    {"connect", context_connect, METH_VARARGS},
    {"loop", enter_loop, METH_VARARGS},
    {NULL , NULL, 0, NULL},
	{NULL , NULL, 0, NULL}
};


PyMODINIT_FUNC
inittest(void)
{
    PyObject* m;
    m = Py_InitModule("test", Methods);
    if(m == NULL) return;
}
