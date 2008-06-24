#include "core.h"

void enroll(){
    load();
    device_discover();
    device_open();

    struct fp_print_data* guvenliparmak = NULL;


    device_close();
    unload();
}
