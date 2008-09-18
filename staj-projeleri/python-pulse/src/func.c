#include <stdio.h>
#include <Python.h>
#include "pypulse.h"

#define CNT 10

typedef struct _notify{
	int client;
	struct _notify *next;
}notify;

notify **root;
static int allocated = 0; /* allocated -> 1 not allocated-> 0 */

void alloc_first()
{
	printf("allocating root\n");
	int i = 0;
	root = (notify**)calloc(CNT, sizeof(notify));
	printf("root allocated done\n");
	allocated = 1;
}

// add, update application list
void py_updateSinkInput(pa_sink_input_info* info)
{
	int notify_index = 0;
	
	printf("*****index = %i\n", info->index);
	printf("*****name = %c\n", *info->name);
	printf("*****client = %i\n", info->client);// unique one
	printf("*****sink = %i\n", info->sink);
	printf("*****driver = %c\n", *info->driver);
	
	// if **root is not allocated allocate it first
	if(!allocated) alloc_first();
	
	root[notify_index] = (notify*)calloc(1,sizeof(notify));
	root[notify_index]->client = info->client;
	
	if (notify_index > 0){
		printf("adding chain\n");
		root[notify_index - 1]->client = root[notify_index];
	}
	notify_index++;
	
}

void py_updateSink(pa_sink_info* info)
{
	printf("");
	printf("");
	printf("");
	printf("");
	printf("");
	
}


void py_updateSource(pa_source_info* info)
{
	printf("");
	printf("");
	printf("");
	printf("");
	printf("");
	
}



void sink_cb(pa_context *c, const pa_sink_info *i, int eol)
{
	if (eol) {
		//dec_outstanding(w);
		printf("INF: dec_outstanding MainWindow\n");
		return;
	}

	if (!i) {
		//show_error("Sink callback failure");
		printf("<error>sink callback failure \n");
		return;
	}
	
	//w->updateSink(*i);
	printf("INF: suppose to updateSink(*i)\n");
}


void source_cb(pa_context *c, const pa_source_info *i, int eol) {
	if (eol) {
		//dec_outstanding(w);
		printf("INF: dec_outstanding MainWindow\n");
		return;
	}

	if (!i) {
		//show_error("Source callback failure");
		printf("<error>source callback failure\n");
		return;
	}

	//w->updateSource(*i);
	printf("INF: suppose to updateSource(*i)\n");
}

void sink_input_cb(pa_context *c, const pa_sink_input_info *i, int eol)
{
	if (eol) {
        //dec_outstanding(w);
		printf("INF: dec_outstanding MainWindow\n");
		return;
	}

	if (!i){
        //show_error("Sink input callback failure");
		printf("<error>sink input callback failure\n");
		return;
	}

    //w->updateSinkInput(*i);
	py_updateSinkInput(i);
	/*
	printf("*****index = %i\n", i->index);
	printf("*****name = %c\n", *i->name);
	//printf("*****client = %i\n", i->client);
	//printf("*****sink = %i\n", i->sink);
	printf("suppose to updateSinkInput(*i)\n");
	*/
}




void client_cb(pa_context *c, const pa_client_info *i, int eol)
{
	if (eol) {
        //dec_outstanding(w);
		printf("INF: dec_outstanding MainWindow\n");
		return;
	}

	if (!i) {
        //show_error("Client callback failure");
		printf("<error>client callback failure\n");
		return;
	}

    //w->updateClient(*i);
	printf("INF: suppose to updateClient(*i)\n");
}

void server_info_cb(pa_context *c, const pa_server_info *i)
{
	if (!i) {
        //show_error("Server info callback failure");
		printf("<error>server callback failure\n");
		return;
	}
    //w->updateServer(*i);
	printf("INF: suppose to updateServer(*i)\n");
    //dec_outstanding(w);
}



void subscribe_cb(pa_context *c, pa_subscription_event_type_t t, uint32_t index)
{
	switch (t & PA_SUBSCRIPTION_EVENT_FACILITY_MASK) {
		case PA_SUBSCRIPTION_EVENT_SINK:
			if ((t & PA_SUBSCRIPTION_EVENT_TYPE_MASK) == PA_SUBSCRIPTION_EVENT_REMOVE)
                //w->removeSink(index);
				printf("INF: suppose to removeSink(index)\n");
			else {
				pa_operation *o;

				if (!(o = pa_context_get_sink_info_by_index(c, index, sink_cb, NULL))) {
                    //show_error("pa_context_get_sink_info_by_index() failed");
					printf("<error>pa_context_get_sink_info_by_index() failed\n");
					return;
				}
				pa_operation_unref(o);
			}

			break;

		case PA_SUBSCRIPTION_EVENT_SOURCE:
			if ((t & PA_SUBSCRIPTION_EVENT_TYPE_MASK) == PA_SUBSCRIPTION_EVENT_REMOVE)
                //w->removeSource(index);
				printf("INF: suppose to removeSource(index)\n");

			else {
				pa_operation *o;
				if (!(o = pa_context_get_source_info_by_index(c, index, source_cb, NULL))) {
                    //show_error("pa_context_get_source_info_by_index() failed");
					printf("<error>pa_context_get_source_info_by_index() failed\n");
					return;
				}
				pa_operation_unref(o);
			}

			break;

		case PA_SUBSCRIPTION_EVENT_SINK_INPUT:
			if ((t & PA_SUBSCRIPTION_EVENT_TYPE_MASK) == PA_SUBSCRIPTION_EVENT_REMOVE)
                //w->removeSinkInput(index);
				printf("INF: suppose to removeSinkInput(index)\n");
			else {
				pa_operation *o;
				if (!(o = pa_context_get_sink_input_info(c, index, sink_input_cb, NULL))) {
                    //show_error("pa_context_get_sink_input_info() failed");
					printf("<error>pa_context_get_sink_input_info() failed");
					return;
				}
				pa_operation_unref(o);
			}
			break;

		case PA_SUBSCRIPTION_EVENT_CLIENT:
			if ((t & PA_SUBSCRIPTION_EVENT_TYPE_MASK) == PA_SUBSCRIPTION_EVENT_REMOVE)
                //w->removeClient(index);
				printf("INF: suppose to removeClient(index)\n");

			else {
				pa_operation *o;
				if (!(o = pa_context_get_client_info(c, index, client_cb, NULL))) {
                    //show_error("pa_context_get_client_info() failed");
					printf("<error>pa_context_get_client_info() failed\n");
					return;
				}
				pa_operation_unref(o);
			}
			break;

		case PA_SUBSCRIPTION_EVENT_SERVER:
			printf("pa_subscription_event_server triggered\n");
			{
				pa_operation *o;
				if (!(o = pa_context_get_server_info(c, server_info_cb, NULL))) {
					//show_error("pa_context_get_server_info() failed");
					printf("<error>pa_context_get_server_info() failed\n");
					return;
				}
				pa_operation_unref(o);
			}

			break;
	}
}
