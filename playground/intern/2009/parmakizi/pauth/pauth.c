#include <stdio.h>
#include <stdlib.h>
#include <libfprint/fprint.h>


//driver bilgisi
void print_driver_info(struct fp_dscv_dev* ddev){ //assume valid input
    struct fp_driver* driver;
    driver = fp_dscv_dev_get_driver(ddev);
    //printf("Okuyucu bulundu!\n");
    printf("Driver id: %d\nDriver ismi: %s\n", fp_driver_get_driver_id(driver), fp_driver_get_full_name(driver));
}

int main(){

    //initialize
    if (fp_init()){
        printf("libfprint patladi!\n");
        exit(1); //failure
    }

    //dev discovery
    struct fp_dscv_dev** ddevicelist;
    struct fp_dscv_dev* ddevice;

    if (!(ddevicelist = fp_discover_devs())){ //listeyi al
        printf("Device discovery calismadi!\n");
        exit(1); //failure
    }

    if(!(ddevice = ddevicelist[0])){ //bos? TODO: 2 alet varsa nolacak?
        printf("Alet nerde?\n");
        exit(1); //failure
    }

    print_driver_info(ddevice);

    //open device
    struct fp_dev* device;

    if(!(device = fp_dev_open(ddevice))){
        printf("Okuyucu baslamadi!\n");
        exit(1); //failure
    }

    //enroll
    //printf("%d", fp_dev_get_nr_enroll_stages(device)); //tek olmali, cunku laptop.

    int done = 0;
	struct fp_print_data* guvenliparmak = NULL;
    while(!done){

	switch(fp_enroll_finger_img(device, &guvenliparmak, NULL)){
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
	}

    }

    fp_print_data_free(guvenliparmak);

    //cleanup
    fp_dev_close(device);
    fp_exit();

    return 0;
}
