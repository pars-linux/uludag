#include "core.h"

// ---------------- GLOBALS --------------------


char* errormsg[]={
    "Library could not be loaded.",
    "Device discovery failed.",
    "No reader could be found.",
    "Device discovery failed.",
    "The device does not support imaging.",
    "The device failed to get an image."
};



// ----------------- HELPERS -------------------

/**Generate an error message from given error code according
 * to the definitions in core.h */
void pyferror(int id){
    if (id <= MAXERROR){
        printf("Error: %s\n", errormsg[id]);
    } else {
        printf("Unknown error!\n");
    }
    exit(1);
}

// ----------------------------------------------

/**Load libfprint*/
void load(){
    if (fp_init()) pyferror(ERR_LFP_LIBRARYFAIL);
}

/**Unload libfprint*/
void unload(){
    fp_exit();
}

/**Find and select devices*/
void device_discover(){
    //get device list
    if (!(ddevice_list = fp_discover_devs())){
        pyferror(ERR_LFP_DISCOVERYFAIL); //failure
    }

    //TODO:check for multiple devices

    //select 1st  device
    if(!(ddevice_curr = ddevice_list[0])){
        pyferror(ERR_LFP_NODEVICE);
    }
}

/**Initialize the selected device*/
void device_open(){
    //check if discovery has been done first?
    if(!(device = fp_dev_open(ddevice_curr))){
        pyferror(ERR_LFP_DEVICEINITFAIL);
    }
}

/**Uninitialize the selected device*/
void device_close(){
    fp_dev_close(device);
}

int main (){
    pyferror(4);
    return 0;
}

