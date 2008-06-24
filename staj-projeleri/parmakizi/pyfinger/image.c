#include "core.h"

// ------------ HELPERS -----------------

/**Helper: Read an image into a variable*/
struct fp_img* image_get(){
    //imaging supported?
    if(!fp_dev_supports_imaging(device)){
        pyfmsg(ERR_LFP_NOIMAGING, 1);
    }

    //capture image
    struct fp_img* image = NULL;
    if (fp_dev_img_capture(device, 0, &image)){
        pyfmsg(ERR_LFP_IMAGINGFAIL, 1);
    }

    return image;
}

/**Helper: Write an image to a file*/
int image_writefile(struct fp_img* image, char* filename){
    return fp_img_save_to_file(image, filename); // 0 on sucess
}

// --------------------------------------

/**Capture an image, standardize it, and write it to a file*/
void image_save(char* filename){
    struct fp_img* img = image_get();
    fp_img_standardize(img);
    image_writefile(img, filename);
    fp_img_free(img); //free it
}

/**Capture an image, standardize and binarize it, and write it to a file*/
void image_save_binarized(char* filename){
    struct fp_img* img = image_get();
    fp_img_standardize(img);
    struct fp_img* img_binarized = fp_img_binarize(img);
    image_writefile(img_binarized, filename);
    fp_img_free(img); //free it
    fp_img_free(img_binarized);
}
