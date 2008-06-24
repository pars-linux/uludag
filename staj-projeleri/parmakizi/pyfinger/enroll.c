#include "core.h"

void enroll(){
    load();
    device_discover();
    device_open();

    struct fp_print_data* fingersample = NULL;
    switch(fp_enroll_finger_img(device, &fingersample, NULL)){
        case FP_ENROLL_FAIL:
            printf("Parmakizi alimi tamamlanamadi!\n");
            exit(1); //fail
        case FP_ENROLL_COMPLETE:
            done = 1;
            printf("Parmakizi alimi basariyla tamamlandi.\n");
            break;
        case FP_ENROLL_PASS:
            printf("Tanima asamasi basarili..\n");
            break;
        default:
            printf("Yeniden deneyin!\n");
            break;
    ·   }


    device_close();
    unload();
}
