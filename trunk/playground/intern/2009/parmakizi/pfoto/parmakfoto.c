/*
 * -----------------------------
 *       M. Ali Akmanalp
 * makmanalp -at- wpi [nokta] edu
 * ------------------------------
 *
 * pfoto: parmak izi tarayip raw
 * olarak kaydeder
 *
 * TODO: parmak okuma gelene kadar kitleniyor, napilacak? ayri thread?
 *
 * */


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

struct fp_img* get_image(struct fp_dev* dev){
    if(!fp_dev_supports_imaging(dev)){
        printf("Okuyucuda imaging destegi yok ... :(\n");
        exit(1); //failure
    }

    struct fp_img* image = NULL;
    if(fp_dev_img_capture(dev, 0, &image)){ //0 on success
        printf("Resim alinamadi.\n");
        exit(1); //failure
    } 

    return image;
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

    //open dev
    struct fp_dev* device;

    if(!(device = fp_dev_open(ddevice))){
        printf("Okuyucu baslamadi!\n");
        exit(1); //failure
    }

    //get image
    fp_img_save_to_file(get_image(device), "./parmak.pgm"); //TODO: nasi freelenir lan bu?

    //cleanup
    fp_dev_close(device);
    fp_exit();

    return 0;
}
