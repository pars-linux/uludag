#include "core.h"

// ---------------- GLOBALS --------------------


char* msglist[]={
    "Library could not be loaded.",
    "Device discovery failed.",
    "No reader could be found.",
    "Device discovery failed.",
    "The device does not support imaging.",
    "The device failed to get an image.",
    "Enrollment was completed successfully.",
    "Enrollment failed!",
    "Enrollment step complete.",
    "Please swipe your finger again.",
    "Write to file failed, please check your permissions."
};


// ----------------- HELPERS -------------------

/**Generate a message from given error code according
 * to the definitions in core.h */
void pyfmsg(int id, int fatalerror){
    if (id <= MAXMSG){
        printf("Error: %s\n", msglist[id]);
    } else {
        printf("Unknown error!\n");
    }
    if (fatalerror){ //die if fatal
        //TODO: cleanup?
        exit(1);
    }
}

// ----------------------------------------------

/**Load libfprint*/
void load(){
    if (fp_init()) pyfmsg(ERR_LFP_LIBRARYFAIL, 1);
}

/**Unload libfprint*/
void unload(){
    fp_exit();
}

/**Find and select devices*/
void device_discover(){
    //get device list
    if (!(ddevice_list = fp_discover_devs())){
        pyfmsg(ERR_LFP_DISCOVERYFAIL, 1); //failure
    }

    //TODO:check for multiple devices

    //select 1st  device
    if(!(ddevice_curr = ddevice_list[0])){
        pyfmsg(ERR_LFP_NODEVICE, 1);
    }
}

/**Initialize the selected device*/
void device_open(){
    //check if discovery has been done first?
    if(!(device = fp_dev_open(ddevice_curr))){
        pyfmsg(ERR_LFP_DEVICEINITFAIL, 1);
    }
}

/**Uninitialize the selected device*/
void device_close(){
    fp_dev_close(device);
}

int main (){
    enroll(1);
    return 0;
}

