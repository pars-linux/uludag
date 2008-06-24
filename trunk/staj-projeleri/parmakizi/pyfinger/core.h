#ifndef CORE_H_
#define CORE_H_

#include <stdio.h>
#include <stdlib.h>
#include <libfprint/fprint.h>
//#include <python2.5/Python.h>


//-------------- ERROR CODES ---------------

/**\brief Basic error codes
 *
 * A list of all the errors that might be returned by the library.
 */
enum msgtype{
    ERR_LFP_LIBRARYFAIL,        ///library load failed
    ERR_LFP_DISCOVERYFAIL,      ///device discovery failed
    ERR_LFP_NODEVICE,           ///no device found
    ERR_LFP_DEVICEINITFAIL,     ///device failed to start
    ERR_LFP_NOIMAGING,          ///imaging not supported
    ERR_LFP_IMAGINGFAIL,        ///imaging attempt failed
    MSG_LFP_ENROLLCOMPLETE,     ///enrollment process complete
    ERR_LFP_ENROLLFAIL,         ///enrollment process failed
    MSG_LFP_ENROLLSTEPCOMPLETE, ///enrollment step complete
    ERR_LFP_ENROLLSTEPFAIL      ///enrollment step must be repeated
};

#define MAXMSG 9                ///Largest error code for error bounds check
extern char* msglist[MAXMSG+1]; ///Error messages


// ------------- GLOBALS --------------

struct fp_dscv_dev** ddevice_list; ///Discovered devices
struct fp_dscv_dev* ddevice_curr;  ///Selected discovered-device

struct fp_dev* device; ///Device that we're using

// ------------ PROTOTYPES ------------

//debug
void pyfmsg(int id, int fatalerror);

//core
void load();
void unload();
void device_discover();
void device_open();
void device_close();

//imaging
void image_write(char* filename);
void image_write_binarized(char* filename);

//enrolling
void enroll();

//verifying

#endif
