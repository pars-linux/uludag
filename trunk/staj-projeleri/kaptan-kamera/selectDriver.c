/********************************************************
 *                                                      *
 * Written by Caglar Kilimci                            *
 *                                                      *
 * Prints which cam driver is used by webcam            *
 *                                                      *
 ********************************************************/
#include <stdio.h>          /* For std i/o          */
#include <fcntl.h>          /* For opening device   */
#include <sys/ioctl.h>      /* For ioctl function   */
#include <string.h>         /* For strcpy           */
#include <linux/videodev.h> /* For VIDIOCGCAP       */

typedef enum {

    DRIVER_V4L,
    DRIVER_V4L2,
    DRIVER_NONE

} driver;

int cam;
driver camDriver;
char camName[20];

struct video_capability v4l_capability;
struct v4l2_capability v4l2_capability;

int main(int argc, char ** argv) {

    if(argc == 2) {
        strcpy(camName, argv[1]);
    } else {
        strcpy(camName, "/dev/video0");
    }

    cam = open(camName, O_RDWR);

    if( -1 == ioctl(cam, VIDIOC_QUERYCAP, &v4l2_capability) ) {
        if( -1 == ioctl(cam, VIDIOCGCAP, &v4l_capability) ) {
            camDriver = DRIVER_NONE;
        } else {
            camDriver = DRIVER_V4L;
        }
    } else {
        camDriver = DRIVER_V4L2;
    }

    switch(camDriver) {
        case DRIVER_V4L:
            printf("v4l driver is using..\n");
            break;
        case DRIVER_V4L2:
            printf("v4l2 driver is using..\n");
            break;
        default:
            printf("Neither v4l nor v4l2 is using..\n");
            break;
    }


    close(cam);


    return 0;
}
