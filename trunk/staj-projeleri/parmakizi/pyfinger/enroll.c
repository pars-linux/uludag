#include "core.h"

void enroll(){
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


    device_close();
    unload();
}
