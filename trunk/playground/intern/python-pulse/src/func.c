#include <stdio.h>
#include <Python.h>
#include "pypulse.h"

#define CNT 10
#define BUFF 25

typedef struct _notify{
	char name[BUFF];
	int client;
	struct _notify *next;
}notify;

notify **root;
static int allocated = 0;
static int notify_index = 0;


// check value from python side
static PyObject* check_callback()
{
	int i = 0;

	printf("INF: checking values\n");
	for(;i< CNT;i++){
		printf("getting item : %d",i);
		notify *item = root[i];
		if(item->next != NULL){
			printf("tryout->name   %s :", item->name);
			printf("tryout->client %d :", item->client);
		}else printf("");
	}
	printf("INF: checking values done\n");
}

void alloc_first()
{
	printf("INF: allocating root\n");
	root = (notify**)calloc(CNT, sizeof(notify*));
	printf("INF: root allocated done\n");
	allocated = 1;
}

// add, update application list
void py_updateSinkInput(pa_sink_input_info* info)
{

	printf("func.c: update time = %d\n", notify_index);
	printf("func.c: index = %i\n", info->index);
	printf("func.c: name = %c\n", *info->name);
	printf("func.c: client = %i\n", info->client);// unique one
	printf("func.c: sink = %i\n", info->sink);
	printf("func.c: driver = %c\n", *info->driver);

	// if **root is not allocated allocate it first
	if(!allocated) alloc_first();
	else printf("func.c: root will not allocated this time\n");

	root[notify_index] = (notify*)calloc(1,sizeof(notify));
	root[notify_index]->client = info->client;
	printf("func.c:INF: entering sprintf\n");
	sprintf(root[notify_index]->name, "member %d", notify_index);

	if (notify_index > 0){
		printf("func.c:INF: adding chain\n");
		root[notify_index - 1]->next = root[notify_index];
	}
	notify_index++;
}

/*
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
*/

void sink_cb(pa_context *c, const pa_sink_info *i, int eol)
{
	if (eol) {
		//dec_outstanding(w);
		printf("func.c:INF: dec_outstanding MainWindow\n");
		return;
	}
	if (!i) {
		//show_error("Sink callback failure");
		printf("func.c:<error> sink callback failure \n");
		return;
	}
	//w->updateSink(*i);
	printf("INF: suppose to updateSink(*i)\n");
}


void source_cb(pa_context *c, const pa_source_info *i, int eol)
{
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
					printf("func.c:<error> pa_context_get_sink_info_by_index() failed\n");
					return;
				}
				pa_operation_unref(o);
			}

			break;

		case PA_SUBSCRIPTION_EVENT_SOURCE:
			if ((t & PA_SUBSCRIPTION_EVENT_TYPE_MASK) == PA_SUBSCRIPTION_EVENT_REMOVE)
                //w->removeSource(index);
				printf("func.c:INF: suppose to removeSource(index)\n");

			else {
				pa_operation *o;
				if (!(o = pa_context_get_source_info_by_index(c, index, source_cb, NULL))) {
                    //show_error("pa_context_get_source_info_by_index() failed");
					printf("func.c:<error> pa_context_get_source_info_by_index() failed\n");
					return;
				}
				pa_operation_unref(o);
			}

			break;

		case PA_SUBSCRIPTION_EVENT_SINK_INPUT:
			if ((t & PA_SUBSCRIPTION_EVENT_TYPE_MASK) == PA_SUBSCRIPTION_EVENT_REMOVE)
                //w->removeSinkInput(index);
				printf("func.c:INF: suppose to removeSinkInput(index)\n");
			else {
				pa_operation *o;
				if (!(o = pa_context_get_sink_input_info(c, index, sink_input_cb, NULL))) {
                    //show_error("pa_context_get_sink_input_info() failed");
					printf("func.c:<error> pa_context_get_sink_input_info() failed");
					return;
				}
				pa_operation_unref(o);
			}
			break;

		case PA_SUBSCRIPTION_EVENT_CLIENT:
			if ((t & PA_SUBSCRIPTION_EVENT_TYPE_MASK) == PA_SUBSCRIPTION_EVENT_REMOVE)
                //w->removeClient(index);
				printf("func.c:INF: suppose to removeClient(index)\n");

			else {
				pa_operation *o;
				if (!(o = pa_context_get_client_info(c, index, client_cb, NULL))) {
                    //show_error("pa_context_get_client_info() failed");
					printf("func.c:<error> pa_context_get_client_info() failed\n");
					return;
				}
				pa_operation_unref(o);
			}
			break;

		case PA_SUBSCRIPTION_EVENT_SERVER:
			printf("func.c: pa_subscription_event_server triggered\n");
			{
				pa_operation *o;
				if (!(o = pa_context_get_server_info(c, server_info_cb, NULL))) {
					//show_error("pa_context_get_server_info() failed");
					printf("func.c:<error> pa_context_get_server_info() failed\n");
					return;
				}
				pa_operation_unref(o);
			}

			break;
	}
}
