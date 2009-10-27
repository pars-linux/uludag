#ifndef PYPULSE_H
#define PYPULSE_H "sample pulse header"
#include <stdlib.h>
#include <pulse/glib-mainloop.h>
#include <pulse/pulseaudio.h>

/*
typedef struct update_sink{
    PyObject_HEAD
    PyObject *index;
		// maybe add an int
}update_sink;

static update_sink sink_watcher[100];
*/

void sink_cb(pa_context *c, const pa_sink_info *i, int eol);
void source_cb(pa_context *c, const pa_source_info *i, int eol);
void sink_input_cb(pa_context *c, const pa_sink_input_info *i, int eol);
void client_cb(pa_context *c, const pa_client_info *i, int eol);
void server_info_cb(pa_context *c, const pa_server_info *i);
void subscribe_cb(pa_context *c, pa_subscription_event_type_t t, uint32_t index);
// new
void py_updateSinkInput(pa_sink_input_info* info);
void alloc_first(void);
static PyObject* check_callback(void);
//
static pa_context* context = NULL;

static pa_channel_map channel_map;
static int channel_map_set = 0;
static pa_stream_flags_t flags = 0;
static size_t latency = 0, process_time=0;
//static int callback_ready_flag = -1;
#endif

