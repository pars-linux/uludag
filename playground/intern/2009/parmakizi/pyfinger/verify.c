#include "core.h"

void verify(){

    load();
    device_discover();
    device_open();

    //stuff goes here 

    device_close();
    unload();


}
