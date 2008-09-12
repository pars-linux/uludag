#include <stdio.h>
#include <Python.h>
#include "pypulse.h"



void sink_cb(pa_context *c, const pa_sink_info *i, int eol)
{
	if (eol) {
		//dec_outstanding(w);
		printf("dec_outstanding MainWindow\n");
		return;
	}

	if (!i) {
		//show_error("Sink callback failure");
		printf("<error>sink callback failure \n");
		return;
	}
	
	//w->updateSink(*i);
	printf("suppose to updateSink\n");
}


void source_cb(pa_context *c, const pa_source_info *i, int eol) {
	if (eol) {
		//dec_outstanding(w);
		printf("dec_outstanding MainWindow\n");
		return;
	}

	if (!i) {
		//show_error("Source callback failure");
		printf("<error>source callback failure\n");
		return;
	}

	//w->updateSource(*i);
	printf("supoose to updateSource\n");
}

void sink_input_cb(pa_context *c, const pa_sink_input_info *i, int eol)
{
	if (eol) {
        //dec_outstanding(w);
		printf("dec_outstanding MainWindow\n");
		return;
	}

	if (!i) {
        //show_error("Sink input callback failure");
		printf("<error>sink input callback failure\n");
		return;
	}

    //w->updateSinkInput(*i);
	printf("suppose to updateSinkInput\n");
}

void client_cb(pa_context *c, const pa_client_info *i, int eol)
{
	if (eol) {
        //dec_outstanding(w);
		printf("dec_outstanding MainWindow\n");
		return;
	}

	if (!i) {
        //show_error("Client callback failure");
		printf("<error>client callback failure\n");
		return;
	}

    //w->updateClient(*i);
	printf("suppose to updateClient\n");
}

void server_info_cb(pa_context *c, const pa_server_info *i)
{
	if (!i) {
        //show_error("Server info callback failure");
		printf("<error>server callback failure\n");
		return;
	}
    //w->updateServer(*i);
	printf("suppose to updateServer\n");
    //dec_outstanding(w);
}



void subscribe_cb(pa_context *c, pa_subscription_event_type_t t, uint32_t index)
{
	switch (t & PA_SUBSCRIPTION_EVENT_FACILITY_MASK) {
		case PA_SUBSCRIPTION_EVENT_SINK:
			if ((t & PA_SUBSCRIPTION_EVENT_TYPE_MASK) == PA_SUBSCRIPTION_EVENT_REMOVE)
                //w->removeSink(index);
				printf("suppose to removeSink[index]\n");
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
				printf("suppose to removeSource[index]\n");

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
				printf("suppose to removeSinkInput(index)\n");
			else {
				pa_operation *o;
				if (!(o = pa_context_get_sink_input_info(c, index, sink_input_cb, NULL))) {
                    //show_error("pa_context_get_sink_input_info() failed");
					printf("<erro>pa_context_get_sink_input_info() failed");
					return;
				}
				pa_operation_unref(o);
			}
			break;

		case PA_SUBSCRIPTION_EVENT_CLIENT:
			if ((t & PA_SUBSCRIPTION_EVENT_TYPE_MASK) == PA_SUBSCRIPTION_EVENT_REMOVE)
                //w->removeClient(index);
				printf("suppose to removeClient(index)\n");

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
					printf("pa_context_get_server_info() failed\n");
					return;
				}
				pa_operation_unref(o);
			}

			break;
	}
}
