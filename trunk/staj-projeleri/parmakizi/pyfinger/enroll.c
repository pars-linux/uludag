#include "core.h"

#include <string.h>
#include <unistd.h>

// --------------- HELPERS ---------------

/**Save print data to a file*/
void enroll_save(struct fp_print_data* data, int uid){
    unsigned char* out = NULL;
    fp_print_data_get_data(data, &out);

    //generate filename
    char fname[255];
    strcat(fname, PYFDIR);
    sprintf(fname, "%s%d", fname, uid);

    //write
    FILE* handle;
    if(!(handle = fopen(fname, "w"))){
        pyfmsg(ERR_WRITEFAIL, 1);
    }
    fputs(out, handle);
    fclose(handle);
}



//----------------------------------------

/**Enroll a user: save fingerprint data for later use**/
void enroll(int uid){
    load();
    device_discover();
    device_open();

    int done = 0;
    struct fp_print_data* fingersample = NULL;
    switch(fp_enroll_finger_img(device, &fingersample, NULL)){
        case FP_ENROLL_FAIL:
            pyfmsg(ERR_LFP_ENROLLFAIL, 1);
            break;
        case FP_ENROLL_COMPLETE:
            done = 1;
            pyfmsg(MSG_LFP_ENROLLCOMPLETE, 0);
            break;
        case FP_ENROLL_PASS:
            pyfmsg(MSG_LFP_ENROLLSTEPCOMPLETE, 0);
            break;
        default: //retry
            pyfmsg(ERR_LFP_ENROLLSTEPFAIL, 0); //nonfatal error
            break;
    }

    enroll_save(fingersample, getuid());

    device_close();
    unload();
}
