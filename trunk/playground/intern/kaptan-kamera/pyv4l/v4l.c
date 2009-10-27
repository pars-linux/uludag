/*
 *  PyV4L
 *
 *  A Python wrapper library to access V4L (video4linux) and V4L2 devices
 *
 * Copyright (c) 2002 Michael Dove <pythondeveloper@optushome.com.au>
 * Copyright (c) 2007, Onur Küçük <onur@pardus.org.tr>
 * Copyright (c) 2008  Çağlar Kilimci <ckilimci@gmail.com>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 *
 * Original work was done by Michael Dove. Since the upstream page got loss
 * and the original authors email address could not be reached, we have forked the
 * project to clean up the code, fix bugs and add v4l2 support.
 *
 * V4L2 support and maintenance by Onur Küçük <onur@pardus.org.tr> and Çağlar Kilimci <ckilimci@gmail.com>
 *
 *
 * Overlay functions derived from G-Streamer <v4l-overlay_calls.c> by Ronald Bultje <rbultje@ronald.bitfreak.net>
 * Frame Buffer Setup functions from v4l-conf by Gerd Knorr <kraxel@bytesex.org>
 *
 * Colour palette conversion from XawTV <color_yuv2rgb.c> by Gerd Knorr <kraxel@bytesex.org>
 * patched by Frederik Fix
 *
 * Derived from fmio <bktr.c> by Vladimir Popov <jumbo@narod.ru>
 *
 */


#include <Python.h>
#include <fcntl.h>
#include <linux/videodev.h>
#include <sys/ioctl.h>
#include <stdio.h>
#include <sys/mman.h>
#include <math.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/extensions/xf86dga.h>
#include "libv4l1.h"

#define WIDTH 320
#define HEIGHT 240


/* colourspace conversion */
#define CLIP         320

# define RED_NULL    128
# define BLUE_NULL   128
# define LUN_MUL     256
# define RED_MUL     512
# define BLUE_MUL    512

#define GREEN1_MUL  (-RED_MUL/2)
#define GREEN2_MUL  (-BLUE_MUL/6)
#define RED_ADD     (-RED_NULL  * RED_MUL)
#define BLUE_ADD    (-BLUE_NULL * BLUE_MUL)
#define GREEN1_ADD  (-RED_ADD/2)
#define GREEN2_ADD  (-BLUE_ADD/6)

/* colorspace conversion lookup tables */
static unsigned int  ng_yuv_gray[256];
static unsigned int  ng_yuv_red[256];
static unsigned int  ng_yuv_blue[256];
static unsigned int  ng_yuv_g1[256];
static unsigned int  ng_yuv_g2[256];
static unsigned int  ng_clip[256 + 2 * CLIP];


#define GRAY(val)               ng_yuv_gray[val]
#define RED(gray,red)           ng_clip[ CLIP + gray + ng_yuv_red[red] ]
#define GREEN(gray,red,blue)    ng_clip[ CLIP + gray + ng_yuv_g1[red] + \
                                                       ng_yuv_g2[blue] ]
#define BLUE(gray,blue)         ng_clip[ CLIP + gray + ng_yuv_blue[blue] ]



/* conversion buffer */
struct ng_video_buf {
    int			size;
    unsigned char	*data;
    int			width;
    int			height;
};

/* radioobject information */
typedef struct {
    PyObject_HEAD
    int		fd;
    float	fact;
} radioobject;

/* videoobject information */
typedef struct {
    PyObject_HEAD
    int		fd;
    float	fact;
    char	*map;
    struct 	video_mbuf mbuf;
    struct 	video_mmap vm;
    float	fps;
    int		frame_count;
    clock_t	cstart;
    clock_t	clast;

    struct ng_video_buf conversion_buffer;
    void(*convertFunc)(struct ng_video_buf *, struct ng_video_buf *);
} videoobject;


/* v4lobject information */
typedef struct {
    PyObject_HEAD
    int		fd;
    float	fact;
} v4lobject;



/* display info */
struct DISPLAYINFO {
    int   width;             /* visible display width  (pixels) */
    int   height;            /* visible display height (pixels) */
    int   depth;             /* color depth                     */
    int   bpp;               /* bit per pixel                   */
    int   bpl;               /* bytes per scanline              */
    unsigned char *base;
};




staticforward PyTypeObject V4LType;
staticforward PyTypeObject RadioType;
staticforward PyTypeObject VideoType;


PyObject * setupConversion(videoobject *self, unsigned int from, unsigned int to);
void yuv420p_to_rgb24(struct ng_video_buf *out, struct ng_video_buf *in);
void yuv422p_to_rgb24(struct ng_video_buf *out, struct ng_video_buf *in);
void color_yuv2rgb_init(void);


/* Some Doc Strings */
static char radio_doc[] =
"v4l.radio(filedescriptor) -> radio object\n"
"\n"
"Control a v4l radio tuner.\n"
"Open a radio device file (eg. /dev/radio), pass device file name to constructor.";

static char video_doc[] =
"v4l.video(filedescriptor) -> video object\n"
"\n"
"Control a v4l video device.\n"
"Open a video device file (eg. /dev/video), pass device file name to constructor.";

static char v4l_doc[] =
"v4l.V4L(filedescriptor) -> generic V4L object\n"
"\n"
"Control a v4l video device.\n"
"Open a video device file (eg. /dev/video), pass device file name to constructor.\n";

static char getfreq_doc[] =
"getFrequency() -> int frequency (Khz)\n"
"\n"
"Gets the current frequency of device.";

static char getmode_doc[] =
"getMode() -> int mode\n"
"\n"
"Returns audio mode.";

static char getvol_doc[] =
"getVolume() -> int volume\n"
"\n"
"Returns volume level (0-9).";

static char setfreq_doc[] =
"setFrequency(integer) -> None\n"
"\n"
"Set Frequency (Khz)";

static char setvol_doc[] =
"setVolume(volumelevel) -> None\n"
"\n"
"Sets the volume level, not supported by all devices.\n";

static char mute_doc[] =
"mute() -> None\n"
"\n"
"Mutes device.";

static char setbass_doc[] =
"setBass(basslevel) -> None\n"
"\n"
"Sets the bass level (0-9), not supported by all devices.";

static char settreble_doc[] =
"setTreble(treblelevel) -> None\n"
"\n"
"Sets the treble level (0-9), not supported by all devices.";

static char setmono_doc[] =
"setMono() -> None\n"
"\n"
"Sets audio mode to mono.";

static char setstereo_doc[] =
"setStereo() -> None\n"
"\n"
"Sets audio mode to stereo, not supported by all devices.";

static char getbuffer_doc[] =
"getBuffer() -> (int height, int width, int depth, int bytesperline, string base)\n"
"\n"
"Returns buffer tuple.";

static char setupframebuffer_doc[] =
"setupFrameBuffer(display) -> None\n"
"\n"
"Setup V4L framebuffer, optional argument display specifies X display to setup.";


static char getcapabilities_doc[] =
"getCapabilities() -> (string name, int type,\n int channels, int audios,\n int maxwidth, int maxheight,\n int minwidth, int minheight)\n"
"\n"
"Returns the device capabilities.";

static char getchannel_doc[] =
"getChannel(channel) -> (int channel, string name, int tuners)"
"\n"
"Returns channel information.";

static char getchannelext_doc[] =
"getChannelExt(channel) -> (int channel, string name, int tuners, int type, int norm)"
"\n"
"Returns full channel information.";

static char getoverlay_doc[] =
"getOverlay() -> (int x, int y, int width, int height, int chromakey, int flags, int clipcount)\n"
"\n"
"Return overlay information.";

static char getpicture_doc[] =
"getPicture() -> (int brightness, int hue, int colour, int contrast, int whiteness, int depth, int palette)\n"
"\n"
"Returns picture information, whiteness only for black & white palette types.";

static char settuner_doc[] =
"setTuner() -> None\n"
"\n"
"Set tuner mode.";

static char gettuner_doc[] =
"getTuner() -> (int tuner, string name, int rangelow, int rangehigh, int flags, int mode, int signal)\n"
"\n"
"Returns tuner information.";

static char getvbi_doc[] =
"getVbi() -> (int sampling_rate, int samples_per_line,\n\
    int sample_format, (int start1, int start2),\n\
    (int count1, int count2), int flags)\n"
"\n"
"Returns VBI information.";

static char setchannel_doc[] =
"setChannel(channel,norm) -> None\n"
"\n"
"Set Channel. Optional norm can be specified for channel";

static char setoverlay_doc[] =
"setOverlay(x, y, width, height) -> None\n"
"\n"
"Set Overlay information.";

static char setpicture_doc[] =
"setPicture(bright, hue, colour, contrast, whiteness, depth, palette) -> None\n"
"\n"
"Set Picture information.\n";

static char setsync_doc[] =
"setSync(sync) -> None\n"
"\n"
"Set sync.";

static char startcapture_doc[] =
"startCapture() -> None\n"
"\n"
"Start Capture.";

static char stopcapture_doc[] =
"stopCapture() -> None\n"
"\n"
"Stop Capture.";

static char prequeueframes_doc[] =
"preQueueFrames() -> None\n"
"\n"
"Queue up frames before capture.";

static char queueframe_doc[] =
"queueFrame() -> None\n"
"\n"
"Queue up a single frame.";

static char getimage_doc[] =
"getImage() -> string image\n"
"\n"
"Get a frame from device.";

static char setupimage_doc[] =
"setupImage(width, height, palette, conversion_palette) -> None\n"
"\n"
"Set image capture parameters and colourspace (conversion).";




/* Instance methods
 * 	radio.setFrequency()	- set tuner frequency
 * 	radio.getFrequency()	- get tuner frequency
 * 	radio.mute()		- mute tuner
 * 	radio.setVolume()	- set volume
 * 	radio.getVolume()	- get volume
 * 	radio.setMono()		- set mode to Mono
 * 	radio.setStereo()	- set mode to Stereo
 * 	radio.getMode()		- get mode
 * 	radio.setBass()		- set bass level - hardware must support
 * 	radio.setTreble()	- set treble level - hardware must support
 */


/* Exceptions */
static PyObject *V4lError;
static PyObject *AudioError; /* Errors anything to do with audio */
static PyObject *VideoError; /* Errors anything to do with video */





/* Functions */
static PyObject *
v4l_getCapabilities(v4lobject *self) {
     struct video_capability vc;
     PyObject *cap;
     if (v4l1_ioctl(self->fd, VIDIOCGCAP, &vc) < 0) {
	 PyErr_SetString(V4lError, "Error retriving video capability.");
	 return NULL;
     }
     cap = Py_BuildValue("(siiiiiii)",
	     vc.name,
	     vc.type,
	     vc.channels,
	     vc.audios,
	     vc.maxwidth,
	     vc.maxheight,
	     vc.minwidth,
	     vc.minheight
	     );
     //printf("VID_TYPE_CHROMAKEY: %d\n", VID_TYPE_CHROMAKEY);
     return cap;
}

static PyObject *
v4l_getChannel(v4lobject *self, PyObject *args) {
    int chan;
    if (!PyArg_ParseTuple(args, "i", &chan)) return NULL;
    struct video_channel vc;
    vc.channel = chan;
    PyObject *vidchan;
    if (v4l1_ioctl(self->fd, VIDIOCGCHAN, &vc) < 0) {
	PyErr_SetString(V4lError, "Error retriving video channel.");
	return NULL;
    }
    vidchan = Py_BuildValue("(isi)",
	    vc.channel,
	    vc.name,
	    vc.tuners
	    );
    return vidchan;
}


static PyObject *
v4l_getChannelExt(v4lobject *self, PyObject *args) {
  int chan;
  if (!PyArg_ParseTuple(args, "i", &chan)) return NULL;
  struct video_channel vc;
  vc.channel = chan;
  PyObject *vidchan;
  if (v4l1_ioctl(self->fd, VIDIOCGCHAN, &vc) < 0) {
    PyErr_SetString(V4lError, "Error retriving video channel.");
    return NULL;
  }
  vidchan = Py_BuildValue("(isiii)",
			  vc.channel,
			  vc.name,
			  vc.tuners,
			  vc.type,
			  vc.norm
			  );
  return vidchan;
}


static PyObject *
v4l_setChannel(v4lobject *self, PyObject *args) {
    int chan;
    int norm;
    if (!PyArg_ParseTuple(args, "i|i", &chan, &norm))
      return NULL;
    struct video_channel vc;
    vc.channel = chan;
    if (v4l1_ioctl(self->fd, VIDIOCGCHAN, &vc) < 0) {
	PyErr_SetString(V4lError, "Error retriving video channel.");
	return NULL;
    }
    if ( PySequence_Length(args) > 1) // norm is requested to be set
      vc.norm = norm;

    if (v4l1_ioctl(self->fd, VIDIOCSCHAN, &vc) < 0) {
	PyErr_SetString(V4lError, "Error setting channel.");
	return NULL;
    }
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *
v4l_getTuner(v4lobject *self) {
    struct video_tuner vt;
    PyObject *tuner;
    vt.tuner = 0; // first tuner?
    if (v4l1_ioctl(self->fd, VIDIOCGTUNER, &vt) < 0) {
	PyErr_SetString(V4lError, "Error retriving tuner.");
	return NULL;
    }
    tuner = Py_BuildValue("(icllihh)",
	    vt.tuner,
	    vt.name,
	    vt.rangelow,
	    vt.rangehigh,
	    vt.flags,
	    vt.mode,
	    vt.signal
	    );
    return tuner;
}

static PyObject *
v4l_setTuner(v4lobject *self, PyObject *args) {
    int mode;
    if (!PyArg_ParseTuple(args, "i", &mode)) return NULL;
    struct video_tuner vt;
    vt.tuner = 0; //first tuner?
    if (v4l1_ioctl(self->fd, VIDIOCGTUNER, &vt) < 0) {
	PyErr_SetString(V4lError, "Error retriving tuner.");
	return NULL;
    }

    vt.mode = mode;

    if (v4l1_ioctl(self->fd, VIDIOCSTUNER, &vt) < 0) {
	PyErr_SetString(V4lError, "Error setting tuner mode.");
	return NULL;
    }

    Py_INCREF(Py_None);
    return Py_None;
}


static PyObject *
v4l_getPicture(v4lobject *self) {
    struct video_picture vp;
    PyObject *pic;
    if (v4l1_ioctl(self->fd, VIDIOCGPICT, &vp) < 0) {
	PyErr_SetString(V4lError, "Error retriving picture.");
	return NULL;
    }
    pic = Py_BuildValue("(hhhhhhh)",
	    vp.brightness,
	    vp.hue,
	    vp.colour,
	    vp.contrast,
	    vp.whiteness,
	    vp.depth,
	    vp.palette
	    );
    return pic;
}

static PyObject *
v4l_setPicture(v4lobject *self, PyObject *args) {
    unsigned int bright, hue, colour, contrast, whiteness, depth, palette;
    if (!PyArg_ParseTuple(args, "iiiiiii",
		&bright,
		&hue,
		&colour,
		&contrast,
		&whiteness,
		&depth,
		&palette
		)) return NULL;
    struct video_picture vp;
    vp.brightness = bright;
    vp.hue = hue;
    vp.colour = colour;
    vp.contrast = contrast;
    vp.whiteness = whiteness;
    vp.depth = depth;
    vp.palette = palette;

    if (v4l1_ioctl(self->fd, VIDIOCSPICT, &vp) < 0) {
	PyErr_SetString(V4lError, "Error setting picture.");
	return NULL;
    }
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *
v4l_startCapture(v4lobject *self) {
    int start = 1;
    if (v4l1_ioctl(self->fd, VIDIOCCAPTURE, &start) < 0) {
	PyErr_SetString(V4lError, "Error starting video capture.");
	return NULL;
    }
   Py_INCREF(Py_None);
   return Py_None;
}

static PyObject *
v4l_stopCapture(v4lobject *self) {
    int stop = 0;
    if (v4l1_ioctl(self->fd, VIDIOCCAPTURE, &stop) < 0) {
	PyErr_SetString(V4lError, "Error stopping video capture.");
	return NULL;
    }
   Py_INCREF(Py_None);
   return Py_None;
}

static PyObject *
v4l_getOverlay(v4lobject *self) {
    struct video_window vw;
    PyObject *overlay;
    if (v4l1_ioctl(self->fd, VIDIOCGWIN, &vw) < 0) {
	PyErr_SetString(V4lError, "Error retriving overlay window.");
	return NULL;
    }
    overlay = Py_BuildValue("(iiiiiii)",
	    vw.x,
	    vw.y,
	    vw.width,
	    vw.height,
	    vw.chromakey,
	    vw.flags,
	    vw.clipcount
	    );
    return overlay;
}

static PyObject *
v4l_setOverlay(v4lobject *self, PyObject *args) {
    int x, y, width, height;
    if (!PyArg_ParseTuple(args, "iiii", &x, &y, &width, &height))
	return Py_BuildValue("i", 1);
    struct video_window vw;
    vw.x = x;
    vw.y = y;
    vw.width = width;
    vw.height = height;
    vw.flags = 0;
    vw.chromakey = 0;
    vw.clips = 0;
    vw.clipcount = 0;

    if (v4l1_ioctl(self->fd, VIDIOCSWIN, &vw) < 0) {
	PyErr_SetString(V4lError, "Error setting overlay window.");
	return NULL;
    }
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *
v4l_getBuffer(v4lobject *self) {
    struct video_buffer vb;
    PyObject *buffer;
    if (v4l1_ioctl(self->fd, VIDIOCGFBUF, &vb) < 0) {
	PyErr_SetString(V4lError, "Unable to retrieve Video Buffer.");
	return NULL;
    }

    char base[10];
    sprintf(base, "%p", vb.base);
    buffer = Py_BuildValue("iiiis",
	    vb.height,
	    vb.width,
	    vb.depth,
	    vb.bytesperline,
	    base
	    );
    return buffer;
}

static int
displayinfo_v4l(v4lobject *self, struct DISPLAYINFO *d) {
    struct video_buffer vb;

    if (v4l1_ioctl(self->fd, VIDIOCGFBUF, &vb) < 0) {
	PyErr_SetString(VideoError, "Unable to retrieve Video Buffer.");
	return 1;
    }

    vb.width		= d->width;
    vb.height		= d->height;
    vb.depth		= d->bpp;
    vb.bytesperline	= d->bpl;

    if (NULL != d->base)
	vb.base = d->base;
    if (NULL == vb.base) {
	PyErr_SetString(VideoError, "Could not find framebuffer base address.");
	return 1;
    }

    if (d->depth == 15)
	vb.depth = 15;

    if (v4l1_ioctl(self->fd, VIDIOCSFBUF, &vb) < 0) {
	PyErr_SetString(VideoError, "Unable to setup Video Buffer, possible root problem.");
	return 1;
    }

    return 0;
}



static int
displayinfo_x11(Display *dpy, struct DISPLAYINFO *d) {
    Window		root;
    XVisualInfo		*info, template;
    XPixmapFormatValues *pf;
    XWindowAttributes	wts;
    int			found,v,i,n;

    /* get size from root window */
    root = DefaultRootWindow(dpy);
    XGetWindowAttributes(dpy, root, &wts);
    d->width = wts.width;
    d->height = wts.height;

    /* look for a usable visual */
    template.screen = XDefaultScreen(dpy);
    info = XGetVisualInfo(dpy, VisualScreenMask, &template, &found);
    v = -1;
    for (i = 0; v == -1 && i < found; i++)
	if (info[i].class == TrueColor && info[i].depth >= 15)
	    v = i;

    for (i = 0; v == -1 && i < found; i++)
	if (info[i].class == StaticGray && info[i].depth == 8)
	    v = i;
    if (-1 == v) {
	PyErr_SetString(VideoError, "No X11 visual available.");
	return 1;
    }

    /* get depth + bpp */
    pf = XListPixmapFormats(dpy, &n);
    for (i = 0; i < n; i++) {
	if (pf[i].depth == info[v].depth) {
	    d->depth = pf[i].depth;
	    d->bpp   = pf[i].bits_per_pixel;
	    d->bpl   = d->bpp * d->width / 8;
	    break;
	}
    }
    if (0 == d->bpp) {
	PyErr_SetString(VideoError, "Unable to get X11 framebuffer depth.");
	return 1;
    }
    return 0;
}


static int
displayinfo_dga(Display *dpy, struct DISPLAYINFO *d) {
    int width,bar,foo,flags=0;
    void *base = NULL;

    if (!XF86DGAQueryExtension(dpy, &foo, &bar)) {
    	PyErr_SetString(VideoError, "X-Server has no DGA support.");
	return 1;
    }

    //XF86DGAQueryVersion(dpy, &major, &minor);
    XF86DGAQueryDirectVideo(dpy, XDefaultScreen(dpy), &flags);
    if (!(flags & XF86DGADirectPresent)) {
	PyErr_SetString(VideoError, "No DGA Support for specified display.");
	return 1;
    }

    XF86DGAGetVideoLL(dpy, XDefaultScreen(dpy), (void *)&base, &width, &foo, &bar);
    d->bpl = width * d->bpp/8;
    d->base = base;

    return 0;

}

static PyObject *
v4l_setupFrameBuffer(v4lobject *self, PyObject *args) {
    char *display = NULL;
    Display *dpy;
    struct DISPLAYINFO d;

    if (!PyArg_ParseTuple(args, "|s", &display))
	return Py_BuildValue("i", 1);

    memset(&d,0,sizeof(struct DISPLAYINFO));

    if (NULL == display) {
	if (NULL == (display = getenv("DISPLAY"))) {
    	    PyErr_SetString(VideoError, "Unable to find DISPLAY.");
    	    return NULL;
	}
    }


    if (display[0] != ':') {
	PyErr_SetString(VideoError, "Remote display is not allowed.");
	return NULL;
    }

    if (NULL == (dpy = XOpenDisplay(display))) {
	PyErr_SetString(VideoError, "Unable to open X11 display.");
	return NULL;
    }

    if (displayinfo_x11(dpy, &d))
	return NULL;

    if (displayinfo_dga(dpy, &d))
	return NULL;


    //FIXME: possibly add framebuffer device attempt here

    if(displayinfo_v4l(self, &d))
	return NULL;

    Py_INCREF(Py_None);
    return Py_None;
}

/*
static PyObject *
v4l_setBuffer(v4lobject *self, PyObject *args) {
    struct video_buffer vb;
    int width, height, depth, bytesperline;
    PyObject *buffer;

    if (!PyArg_ParseTuple(args, "iiii", &width, &height, &depth, &bytesperline))
	return Py_BuildValue("i", 1);

    if (ioctl(self->fd, VIDIOCGFBUF, &vb) < 0) {
	PyErr_SetString(V4lError, "Error retriving video buffer.");
	return NULL;
    }
    vb.height = height;
    vb.width = width;
    vb.depth = depth;
    vb.bytesperline = bytesperline;

    if (ioctl(self->fd, VIDIOCSFBUF, &vb) < 0) {
	PyErr_SetString(V4lError, "Error setting video buffer.");
	return NULL;
    }

    Py_INCREF(Py_None);
    return Py_None;
}
*/

static PyObject *
v4l_setSync(v4lobject *self, PyObject *args) {
    int sync;
    if (!PyArg_ParseTuple(args, "i", &sync))
	return Py_BuildValue("i", 1);
    if (v4l1_ioctl(self->fd, VIDIOCSYNC, &sync) < 0) {
	PyErr_SetString(V4lError, "Error syncing video.");
	return NULL;
    }
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *
v4l_getVbi(v4lobject *self) {
    struct vbi_format vf;
    PyObject * vbi;
    if (v4l1_ioctl(self->fd, VIDIOCGVBIFMT, &vf) < 0) {
	PyErr_SetString(V4lError, "Error retriving VBI.");
	return NULL;
    }
    vbi = Py_BuildValue("(iii(ii)(ii)i)",
	    vf.sampling_rate,
	    vf.samples_per_line,
	    vf.sample_format,
	    vf.start[0],
	    vf.start[1],
	    vf.count[0],
	    vf.count[1],
	    vf.flags
	    );
    return vbi;
}

static PyObject *
v4l_setupImage(videoobject *self, PyObject *args) {
    unsigned int height;
    unsigned int width;
    unsigned int format = 0;
    unsigned int convertfmt = 0;
    if (!PyArg_ParseTuple(args, "ii|ii", &width, &height, &format, &convertfmt)) return NULL;
    self->vm.height = height;
    self->vm.width = width;
    if (format != 0)
    	self->vm.format = format;

    if (convertfmt != 0)
	return setupConversion(self, format, convertfmt);
    Py_INCREF(Py_None);
    return Py_None;
}


static int
v4l_setupCapture(videoobject *self) {
    if (v4l1_ioctl(self->fd, VIDIOCGMBUF, &self->mbuf) < 0) return -1;
    //fprintf(stderr,"  mbuf: size=%d frames=%d\n", self->mbuf.size,self->mbuf.frames);
    //self->map = mmap(0, self->mbuf.size, PROT_READ|PROT_WRITE, MAP_SHARED, self->fd, 0);
    //self->map = mmap(0, self->mbuf.size, PROT_READ, MAP_PRIVATE, self->fd, 0);
    self->map = v4l1_mmap(0, self->mbuf.size, PROT_READ|PROT_WRITE, MAP_SHARED, self->fd, 0);
    if ((self->map == NULL) | (self->map == MAP_FAILED)) {
	PyErr_SetString(VideoError, "Error Memory Mapping device.");
    	return -1;
    }


    //printf("Frame: %d\n", self->vm.frame);
    self->vm.frame = 0;
    return 0;
}

static PyObject *
v4l_preQueueFrames(videoobject *self) {
    unsigned int frame;
    if (self->map == NULL) if (v4l_setupCapture(self) < 0) return NULL;
    for (frame=0; frame < self->mbuf.frames; frame++) {
	self->vm.frame = frame;
     	if (v4l1_ioctl(self->fd, VIDIOCMCAPTURE, &self->vm) < 0) {
	    PyErr_SetString(VideoError, "Error queuing frame.");
	    return NULL;
	}
    }
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *
v4l_queueFrame(videoobject *self) {
    unsigned short frame;
    if (self->map == NULL) if (v4l_setupCapture(self) < 0) return NULL;
    if (v4l1_ioctl(self->fd, VIDIOCMCAPTURE, &self->vm) < 0) {
	PyErr_SetString(VideoError, "Error queuing frame.");
	return NULL;
    }
    frame = self->vm.frame + 1;
    if (frame >= self->mbuf.frames) frame = 0;
    return Py_BuildValue("h", frame); // next frame number
}

static PyObject *
v4l_getImage(videoobject *self, PyObject *args) {
    unsigned short frame = 0;
    if (!PyArg_ParseTuple(args, "|h", &frame)) return NULL;

    self->vm.frame = frame;
    if (v4l1_ioctl(self->fd, VIDIOCSYNC,  &self->vm.frame) == -1) {
	//printf("Error: cannot sync\n");
	return NULL;
    }
    /*
    // FPS counter
    printf("FPS: %0.1f\n", self->fps);
    if ( ((self->cstart=clock())-self->clast) / CLOCKS_PER_SEC > 1) {
     	self->fps = (float) self->frame_count / ((float) (self->cstart-self->clast) / CLOCKS_PER_SEC);
        self->frame_count=0;
        self->clast=self->cstart;
    }
    self->frame_count++;
    */


    PyObject *result;

    if (self->convertFunc) {
	struct ng_video_buf in_buffer;
	in_buffer.width = self->vm.width;
	in_buffer.height = self->vm.height;
	in_buffer.data = self->map + self->mbuf.offsets[frame];
	in_buffer.size = self->mbuf.size / self->mbuf.frames;
	self->convertFunc(&self->conversion_buffer, &in_buffer);
	result = Py_BuildValue("s#", self->conversion_buffer.data, self->conversion_buffer.size);
	}
    else
	result = Py_BuildValue("s#", self->map + self->mbuf.offsets[frame], self->vm.width * self->vm.height * 3);
    return (result);
}


/**** Colourspace Conversion Functions ****/


void yuv420p_to_rgb24(struct ng_video_buf *out, struct ng_video_buf *in) {
    unsigned char *y, *u, *v, *d;
    unsigned char *us,*vs;
    unsigned int i,j;
    int gray;

    d = out->data;
    y = in->data;
    u = y + in->width * in->height;
    v = u + in->width * in->height / 4;

    for (i = 0; i < in->height; i++) {
	us = u; vs = v;
	for (j = 0; j < in->width; j+=2) {
	    gray   = GRAY(*y);
	    *(d++) = RED(gray, *v);
	    *(d++) = GREEN(gray, *v, *u);
	    *(d++) = BLUE(gray, *u);
	    y++;
	    gray   = GRAY(*y);
	    *(d++) = RED(gray, *v);
	    *(d++) = GREEN(gray, *v, *u);
	    *(d++) = BLUE(gray, *u);
	    y++; u++; v++;
	}
	if (0 == (i % 2)) {
	    u = us; v = vs;
	}
    }
    out->size = d - out->data;
}


void yuv422p_to_rgb24(struct ng_video_buf *out, struct ng_video_buf *in) {
    unsigned char *y, *u, *v, *d;
    unsigned int i,j;
    int gray;

    d = out->data;
    y  = in->data;
    u  = y + in->width * in->height;
    v  = u + in->width * in->height / 2;

    for (i = 0; i < in->height; i++) {
	for (j = 0; j < in->width; j+= 2) {
	    gray   = GRAY(*y);
	    *(d++) = RED(gray,*v);
	    *(d++) = GREEN(gray,*v,*u);
	    *(d++) = BLUE(gray,*u);
	    y++;
	    gray   = GRAY(*y);
	    *(d++) = RED(gray,*v);
	    *(d++) = GREEN(gray,*v,*u);
	    *(d++) = BLUE(gray,*u);
	    y++; u++; v++;
	}
    }
    out->size = d - out->data;
}



PyObject *
setupConversion(videoobject *self, unsigned int from, unsigned int to) {
    if( from != to ) {
	if( (from == VIDEO_PALETTE_YUV420P) && (to == VIDEO_PALETTE_RGB24) ) {
	    self->convertFunc = yuv420p_to_rgb24;
	}
	else if( (from == VIDEO_PALETTE_YUV422P) && (to == VIDEO_PALETTE_RGB24) ) {
	    self->convertFunc = yuv420p_to_rgb24;
	}
	else {
	    PyErr_SetString(V4lError, "Unsupported colorspace conversion");
	    return NULL;
    	}
    }
    color_yuv2rgb_init();
    if( self->conversion_buffer.data )
	free( self->conversion_buffer.data );
    self->conversion_buffer.data = malloc( self->vm.width*self->vm.height*3 );

    Py_INCREF(Py_None);
    return Py_None;
}


void color_yuv2rgb_init(void) {
    int i;

    /* init Lookup tables */
    for (i = 0; i < 256; i++) {
	ng_yuv_gray[i] = i * LUN_MUL >> 8;
	ng_yuv_red[i]  = (RED_ADD    + i * RED_MUL)    >> 8;
	ng_yuv_blue[i] = (BLUE_ADD   + i * BLUE_MUL)   >> 8;
	ng_yuv_g1[i]   = (GREEN1_ADD + i * GREEN1_MUL) >> 8;
	ng_yuv_g2[i]   = (GREEN2_ADD + i * GREEN2_MUL) >> 8;
    }
    for (i = 0; i < CLIP; i++)
	ng_clip[i] = 0;
    for (; i < CLIP + 256; i++)
	ng_clip[i] = i - CLIP;
    for (; i < 2 * CLIP + 256; i++)
	ng_clip[i] = 255;
}



/**** OLD FUNCTIONS ***/
static PyObject *
v4l_setFrequency(v4lobject *self, PyObject *args) {
    unsigned long basefreq;
    unsigned long freq;
    if (!PyArg_ParseTuple(args, "l", &basefreq)) return NULL;
    freq = basefreq * self->fact + 0.5 ;
    if (v4l1_ioctl(self->fd, VIDIOCSFREQ, &freq) < 0) {
	PyErr_SetString(V4lError, "Error setting frequency.");
	return NULL;
    }
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *
v4l_setRawFreq(v4lobject *self, PyObject *args) {
    unsigned long freq;
    if (!PyArg_ParseTuple(args, "l", &freq)) return NULL;
    if (v4l1_ioctl(self->fd, VIDIOCSFREQ, &freq) < 0) {
	PyErr_SetString(V4lError, "Error setting frequency.");
	return NULL;
    }
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *
v4l_getFrequency(v4lobject *self) {
    unsigned long freq;
    unsigned long basefreq;
    if (v4l1_ioctl(self->fd, VIDIOCGFREQ, &freq) < 0) {
	PyErr_SetString(V4lError, "Error retriving frequency.");
	return NULL;
    }
    basefreq = rint(freq / self->fact);
    return Py_BuildValue("l", basefreq);
}

static PyObject *
v4l_mute(radioobject *self, PyObject *args) {
    struct video_audio va;
    if(!PyArg_ParseTuple(args, "")) return NULL;
    va.audio = 0;
    va.flags = VIDEO_AUDIO_MUTE;
    va.volume = 0;

    if (v4l1_ioctl(self->fd, VIDIOCSAUDIO, &va) < 0) {
	PyErr_SetString(V4lError, "Error muting audio.");
	return NULL;
    }
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *
v4l_setVolume(v4lobject *self, PyObject *args) {
    int vol;
    struct video_audio va;
    if(!PyArg_ParseTuple(args, "i", &vol)) return NULL;
    if (vol > 10) vol = 10;
    if (vol < 0) vol = 0;
    va.flags = VIDEO_AUDIO_VOLUME;
    va.audio = 0;
    va.volume = vol * (65535/10);

    if (v4l1_ioctl(self->fd, VIDIOCSAUDIO, &va) < 0) {
	PyErr_SetString(V4lError, "Error setting volume.");
	return NULL;
    }
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *
v4l_getVolume(v4lobject *self) {
    struct video_audio va;
    va.audio = 0;
    if (v4l1_ioctl(self->fd, VIDIOCGAUDIO, &va) < 0) {
	PyErr_SetString(V4lError, "Error retriving volume.");
	return NULL;
    }
    return Py_BuildValue("i", va.volume * 10/65535);
}

static PyObject *
v4l_setMono(v4lobject *self, PyObject *args) {
    if(!PyArg_ParseTuple(args, "")) return NULL;
    struct video_audio va;
    va.audio = 0;
    va.mode = VIDEO_SOUND_MONO;

    if (v4l1_ioctl(self->fd, VIDIOCSAUDIO, &va) < 0) {
	PyErr_SetString(V4lError, "Error setting audio to mono.");
	return NULL;
    }
    Py_INCREF(Py_None);
    return Py_None;
}


static PyObject *
v4l_setStereo(v4lobject *self, PyObject *args) {
    if(!PyArg_ParseTuple(args, "")) return NULL;
    struct video_audio va;
    va.audio = 0;
    va.mode = VIDEO_SOUND_STEREO;

    if (v4l1_ioctl(self->fd, VIDIOCSAUDIO, &va) < 0) {
	PyErr_SetString(V4lError, "Error setting audio to stereo.");
	return NULL;
    }
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *
v4l_getMode(v4lobject *self) {
    struct video_audio va;
    va.audio = 0;
    if (v4l1_ioctl(self->fd, VIDIOCGAUDIO, &va) > 0) {
	PyErr_SetString(V4lError, "Error retriving audio mode.");
	return NULL;
    }
    return Py_BuildValue("i", va.mode);
}


static PyObject *
v4l_setBass(v4lobject *self, PyObject *args) {
    int level;
    if(!PyArg_ParseTuple(args, "i", &level)) return NULL;
    struct video_audio va;
    if (level > 10) level = 10;
    if (level < 0 ) level = 0;
    va.flags = VIDEO_AUDIO_BASS;
    va.audio = 0;
    va.bass = level * (65535/10);

    if (v4l1_ioctl(self->fd, VIDIOCSAUDIO, &va) > 0) {
	PyErr_SetString(V4lError, "Error setting bass level.");
	return NULL;
    }
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *
v4l_setTreble(v4lobject *self, PyObject *args) {
    int level;
    if (!PyArg_ParseTuple(args, "i", &level)) return NULL;
    struct video_audio va;
    if (level > 10) level = 10;
    if (level < 0) level = 0;
    va.flags = VIDEO_AUDIO_TREBLE;
    va.audio = 0;
    va.treble = level * (65535/10);

    if (v4l1_ioctl(self->fd, VIDIOCSAUDIO, &va) > 0) {
	PyErr_SetString(V4lError, "Error setting treble level.");
	return NULL;
    }
    Py_INCREF(Py_None);
    return Py_None;
}


float get_freq_fact(int fd) {
    struct video_tuner t;
    t.tuner = 0; // first tuner?
    if (v4l1_ioctl(fd, VIDIOCGTUNER, &t) == -1 || (t.flags & VIDEO_TUNER_LOW) == 0)
	return .016;
    return 160.0;
}

/* Instance methods table. Used by v4l_getattr() */
static PyMethodDef v4l_methods[] = {
    {"setFrequency", (PyCFunction) v4l_setFrequency, METH_VARARGS, setfreq_doc},
    {"setRawFrequency", (PyCFunction) v4l_setRawFreq, METH_VARARGS, NULL},
    {"getFrequency", (PyCFunction) v4l_getFrequency, METH_NOARGS, getfreq_doc},
    {"mute", (PyCFunction) v4l_mute, METH_VARARGS, mute_doc},
    {"setVolume", (PyCFunction) v4l_setVolume, METH_VARARGS, setvol_doc},
    {"getVolume", (PyCFunction) v4l_getVolume, METH_NOARGS, getvol_doc},
    {"setMono", (PyCFunction) v4l_setMono, METH_VARARGS, setmono_doc},
    {"setStereo", (PyCFunction) v4l_setStereo, METH_VARARGS, setstereo_doc},
    {"getMode", (PyCFunction) v4l_getMode, METH_NOARGS, getmode_doc},
    {"setBass", (PyCFunction) v4l_setBass, METH_VARARGS, setbass_doc},
    {"setTreble", (PyCFunction) v4l_setTreble, METH_VARARGS, settreble_doc},
    { NULL, NULL }
};

static PyMethodDef radio_methods[] = {
    {"setFrequency", (PyCFunction) v4l_setFrequency, METH_VARARGS, setfreq_doc},
    {"getFrequency", (PyCFunction) v4l_getFrequency, METH_NOARGS, getfreq_doc},
    {"mute", (PyCFunction) v4l_mute, METH_VARARGS, mute_doc},
    {"setVolume", (PyCFunction) v4l_setVolume, METH_VARARGS, setvol_doc},
    {"getVolume", (PyCFunction) v4l_getVolume, METH_NOARGS, getvol_doc},
    {"setMono", (PyCFunction) v4l_setMono, METH_VARARGS, setmono_doc},
    {"setStereo", (PyCFunction) v4l_setStereo, METH_VARARGS, setstereo_doc},
    {"getMode", (PyCFunction) v4l_getMode, METH_NOARGS, getmode_doc},
    {"setBass", (PyCFunction) v4l_setBass, METH_VARARGS, setbass_doc},
    {"setTreble", (PyCFunction) v4l_setTreble, METH_VARARGS, settreble_doc},
    { NULL, NULL }
};

static PyMethodDef video_methods[] = {
    {"getCapabilities", (PyCFunction) v4l_getCapabilities, METH_VARARGS, getcapabilities_doc},
    {"getChannel", (PyCFunction) v4l_getChannel, METH_VARARGS, getchannel_doc},
    {"setChannel", (PyCFunction) v4l_setChannel, METH_VARARGS, setchannel_doc},
    {"getChannelExt", (PyCFunction) v4l_getChannelExt, METH_VARARGS, getchannelext_doc},
    {"setFrequency", (PyCFunction) v4l_setFrequency, METH_VARARGS, setfreq_doc},
    {"getFrequency", (PyCFunction) v4l_getFrequency, METH_NOARGS, getfreq_doc},
    {"setupImage", (PyCFunction) v4l_setupImage, METH_VARARGS, setupimage_doc},
    {"getTuner", (PyCFunction) v4l_getTuner, METH_NOARGS, gettuner_doc},
    {"setTuner", (PyCFunction) v4l_setTuner, METH_VARARGS, settuner_doc},
    {"getPicture", (PyCFunction) v4l_getPicture, METH_NOARGS, getpicture_doc},
    {"setPicture", (PyCFunction) v4l_setPicture, METH_VARARGS, setpicture_doc},
    {"setVolume", (PyCFunction) v4l_setVolume, METH_VARARGS, setvol_doc},
    {"getVolume", (PyCFunction) v4l_getVolume, METH_NOARGS, getvol_doc},
    {"mute", (PyCFunction) v4l_mute, METH_VARARGS, mute_doc},
    {"startCapture", (PyCFunction) v4l_startCapture, METH_NOARGS, startcapture_doc},
    {"stopCapture", (PyCFunction) v4l_stopCapture, METH_NOARGS, stopcapture_doc},
    {"getOverlay", (PyCFunction) v4l_getOverlay, METH_NOARGS, getoverlay_doc},
    {"setOverlay", (PyCFunction) v4l_setOverlay, METH_VARARGS, setoverlay_doc},
    {"setupFrameBuffer", (PyCFunction) v4l_setupFrameBuffer, METH_VARARGS, setupframebuffer_doc},
    {"getBuffer", (PyCFunction) v4l_getBuffer, METH_NOARGS, getbuffer_doc},
    {"setSync", (PyCFunction) v4l_setSync, METH_VARARGS, setsync_doc},
    {"getVbi", (PyCFunction) v4l_getVbi, METH_NOARGS, getvbi_doc},
    {"getImage", (PyCFunction) v4l_getImage, METH_VARARGS, getimage_doc},
    {"queueFrame", (PyCFunction) v4l_queueFrame, METH_NOARGS, queueframe_doc},
    {"preQueueFrames", (PyCFunction) v4l_preQueueFrames, METH_NOARGS, prequeueframes_doc},
    { NULL, NULL }
};


/* Basic Operations */

static v4lobject *
new_v4l(int fd) {
    v4lobject *self;
    struct video_channel vc;
    vc.channel = 0;
    if (v4l1_ioctl(fd, VIDIOCGCHAN, &vc) < 0) {
	PyErr_SetString(V4lError, "No V4L device found.");
	return NULL;
    }
    self = PyObject_NEW(v4lobject, &V4LType);
    if (self == NULL) return NULL;
    self->fd = fd;
    self->fact = get_freq_fact(fd);
    return self;
}

static radioobject *
new_radio(int fd) {
    radioobject *self;
    struct video_tuner t;
    t.tuner = 0; //first device?
    // check to see if v4l is working
    if (v4l1_ioctl(fd, VIDIOCGTUNER, &t) < 0) {
	PyErr_SetString(V4lError, "No V4L radio device found.");
	return NULL;
    }
    self = PyObject_NEW(radioobject, &RadioType);
    if (self == NULL) return NULL;
    self->fd = fd;
    self->fact = get_freq_fact(fd);
    return self;
}

static videoobject *
new_video(int fd) {
    videoobject *self;
    struct video_channel vc;
    vc.channel = 0;
    if (v4l1_ioctl(fd, VIDIOCGCHAN, &vc) < 0) {
	PyErr_SetString(V4lError, "No V4L video device found.");
	return NULL;


    }
    self = PyObject_NEW(videoobject, &VideoType);
    if (self == NULL) return NULL;
    self->fd = fd;
    self->fact = get_freq_fact(fd);
    self->map = NULL;
    // Setup some defaults
    self->vm.height = HEIGHT;
    self->vm.width = WIDTH;
    self->vm.format = VIDEO_PALETTE_RGB24;
    self->cstart = 0;
    self->clast = 0;
    self->frame_count = 0;
    self->conversion_buffer.data = 0;
    self->convertFunc = 0;

    return self;
}

/* Release object */
static void
v4l_dealloc(v4lobject *self) {
    v4l1_close(self->fd);
    PyMem_DEL(self);
}

static void
v4l_dealloc_video(videoobject *self) {
    if (self->map != NULL) {
	if (v4l1_munmap(self->map, self->vm.height * self->vm.width * 3) < 0);
	    //printf("Error Unmapping\n");
    }
    if (self->conversion_buffer.data)
	free(self->conversion_buffer.data);
    v4l_dealloc((v4lobject *)self);
}

/* Get an attribute */
static PyObject *
v4l_getattr(v4lobject *self, char *name) {
    if (strcmp(name, "fact") == 0) {
	return Py_BuildValue("d", self->fact); /* self.fact */
    } else if (strcmp(name, "fd") == 0) {
	return Py_BuildValue("i", self->fd); /* self.fd */
    }
    /* Look for a method instead */
    return Py_FindMethod(v4l_methods, (PyObject *)self, name);
}

static PyObject *
v4l_radiogetattr(radioobject *self, char *name) {
    /* Look for a method instead */
    return Py_FindMethod(radio_methods, (PyObject *)self, name);
}

static PyObject *
v4l_videogetattr(videoobject *self, char *name) {
    /* Look for a method instead */
    return Py_FindMethod(video_methods, (PyObject *)self, name);
}

/* repr() function */
static PyObject *
v4l_repr(v4lobject *self) {
    char rbuffer[256];
    sprintf(rbuffer, "<%s, fd = %d, fact = %.2f at %p>", self->ob_type->tp_name, self->fd, self->fact, self);
    return PyString_FromString(rbuffer);
}

/* Type object for v4l objects */
static PyTypeObject V4LType = {
    PyObject_HEAD_INIT(&PyType_Type) /* Required initialization */
    0,
    "v4l.V4L",
    sizeof(v4lobject),
    0,

    /* Standard methods */
    (destructor)  v4l_dealloc,	/* tp+dealloc,	: refcount = 0 	*/
    (printfunc)	  0,		/* tp_print	: print x	*/
    (getattrfunc) v4l_getattr, 	/* tp_getattr	: x.attr	*/
    (setattrfunc) 0,		/* tp_setattr	: x.attr = v	*/
    (cmpfunc)	  0, 		/* tp_compare	: x > y		*/
    (reprfunc)	  v4l_repr,	/* tp_repr	: repr(x)	*/

    /* Type categories */
    0,				/* tp_as_number	: Number methods */
    0,				/* tp_as_sequence : Sequence methods */
    0,		/* tp_hash	: dict[x]	*/
    0,		/* tp_call	: x()		*/
    0 		/* tp_str	: str(x)	*/
};

/* Type object for radio objects */
static PyTypeObject RadioType = {
    PyObject_HEAD_INIT(&PyType_Type) /* Required initialization */
    0,
    "v4l.radio",
    sizeof(radioobject),
    0,

    /* Standard methods */
    (destructor)  v4l_dealloc,	/* tp+dealloc,	: refcount = 0 	*/
    (printfunc)	  0,		/* tp_print	: print x	*/
    (getattrfunc) v4l_radiogetattr, 	/* tp_getattr	: x.attr	*/
    (setattrfunc) 0,		/* tp_setattr	: x.attr = v	*/
    (cmpfunc)	  0, 		/* tp_compare	: x > y		*/
    (reprfunc)	  v4l_repr,	/* tp_repr	: repr(x)	*/

    /* Type categories */
    0,				/* tp_as_number	: Number methods */
    0,				/* tp_as_sequence : Sequence methods */
    0,		/* tp_hash	: dict[x]	*/
    0,		/* tp_call	: x()		*/
    0 		/* tp_str	: str(x)	*/
};

/* Type object for radio objects */
static PyTypeObject VideoType = {
    PyObject_HEAD_INIT(&PyType_Type) /* Required initialization */
    0,
    "v4l.video",
    sizeof(videoobject),
    0,

    /* Standard methods */
    (destructor)  v4l_dealloc_video,	/* tp+dealloc,	: refcount = 0 	*/
    (printfunc)	  0,		/* tp_print	: print x	*/
    (getattrfunc) v4l_videogetattr, 	/* tp_getattr	: x.attr	*/
    (setattrfunc) 0,		/* tp_setattr	: x.attr = v	*/
    (cmpfunc)	  0, 		/* tp_compare	: x > y		*/
    (reprfunc)	  v4l_repr,	/* tp_repr	: repr(x)	*/

    /* Type categories */
    0,				/* tp_as_number	: Number methods */
    0,				/* tp_as_sequence : Sequence methods */
    0,		/* tp_hash	: dict[x]	*/
    0,		/* tp_call	: x()		*/
    0, 		/* tp_str	: str(x)	*/
    0,		/* tp_getattro			*/
    0,		/* tp_setattro			*/
    0,		/* tp_as_buffer			*/
    0,		/* tp_flags     		*/
};

/* Module Level functions */

/* Create a new v4l object as V4L(filename) */

static PyObject *
v4lobject_new(PyObject *self, PyObject *args) {
    int fd;
    char *fname;
    if (!PyArg_ParseTuple(args, "s", &fname)) return NULL;
    if (-1 == (fd = v4l1_open(fname, O_RDWR))) {
	PyErr_SetString(PyExc_IOError, "Unable to open Device.");
	return NULL;
    }
    return (PyObject *) new_v4l(fd);
}

/* Create a new radio object as radio(filename) */

static PyObject *
radioobject_new(PyObject *self, PyObject *args) {
    int fd;
    char *fname;
    if (!PyArg_ParseTuple(args, "s", &fname)) return NULL;
    if (-1 == (fd = v4l1_open(fname, O_RDWR))) {
	PyErr_SetString(PyExc_IOError, "Unable to open Device.");
	return NULL;
    }
    return (PyObject *) new_radio(fd);
}

/* Create a new video object as video(filename) */

static PyObject *
videoobject_new(PyObject *self, PyObject *args) {
    int fd;
    char *fname;
    if (!PyArg_ParseTuple(args, "s", &fname)) return NULL;
    if (-1 == (fd = v4l1_open(fname, O_RDWR))) {
	PyErr_SetString(PyExc_IOError, "Unable to open Device.");
	return NULL;
    }
    return (PyObject *) new_video(fd);
}

/* Module Methods Table */
static struct PyMethodDef v4ltype_methods[] = {
    { "V4L", v4lobject_new, METH_VARARGS, v4l_doc },
    { "radio", radioobject_new, METH_VARARGS, radio_doc },
    { "video", videoobject_new, METH_VARARGS, video_doc },
    { NULL, NULL}
};

/* Module Description doc string */
static char module_doc[] =
"Implementation for V4L (Video4Linux) operations.";


/* Module initialization function */
DL_EXPORT(void)
initv4l(void) {
    PyObject *m, *d;

    /* bind methods to types */
    RadioType.tp_methods = radio_methods;
    VideoType.tp_methods = video_methods;
    V4LType.tp_methods = v4l_methods;


    VideoType.tp_new = (void *) videoobject_new;
    RadioType.tp_new = (void *) radioobject_new;
    V4LType.tp_new = (void *) v4lobject_new;

    if (PyType_Ready(&VideoType) < 0)
	return;

    if (PyType_Ready(&RadioType) < 0)
    	return;

    if (PyType_Ready(&V4LType) < 0)
    	return;

    m = Py_InitModule3("v4l", v4ltype_methods, module_doc);
    d = PyModule_GetDict(m);

    Py_INCREF(&VideoType);
    Py_INCREF(&RadioType);
    Py_INCREF(&V4LType);

    V4lError = PyErr_NewException("v4l.V4lError", NULL, NULL);
    AudioError = PyErr_NewException("v4l.AudioError", NULL, NULL);
    VideoError = PyErr_NewException("v4l.VideoError", NULL, NULL);

    PyDict_SetItemString(d, "V4lError", V4lError);
    PyDict_SetItemString(d, "AudioError", AudioError);
    PyDict_SetItemString(d, "VideoError", VideoError);


    PyModule_AddObject(m, "video", (PyObject *) &VideoType);
    PyModule_AddObject(m, "radio", (PyObject *) &RadioType);
    PyModule_AddObject(m, "v4l", (PyObject *) &V4LType);


    /* Constants */
    PyDict_SetItemString(d, "VIDEO_VC_TUNER", Py_BuildValue("i", VIDEO_VC_TUNER));
    PyDict_SetItemString(d, "VIDEO_VC_AUDIO", Py_BuildValue("i", VIDEO_VC_AUDIO));
    PyDict_SetItemString(d, "VIDEO_TYPE_TV", Py_BuildValue("i", VIDEO_TYPE_TV));
    PyDict_SetItemString(d, "VIDEO_TYPE_CAMERA", Py_BuildValue("i", VIDEO_TYPE_CAMERA));
    PyDict_SetItemString(d, "VID_TYPE_CHROMAKEY", Py_BuildValue("i", VID_TYPE_CHROMAKEY));


    PyDict_SetItemString(d, "VIDEO_TUNER_PAL", Py_BuildValue("i", VIDEO_TUNER_PAL));
    PyDict_SetItemString(d, "VIDEO_TUNER_NTSC", Py_BuildValue("i", VIDEO_TUNER_NTSC));
    PyDict_SetItemString(d, "VIDEO_TUNER_SECAM", Py_BuildValue("i", VIDEO_TUNER_SECAM));
    PyDict_SetItemString(d, "VIDEO_TUNER_LOW", Py_BuildValue("i", VIDEO_TUNER_LOW));

    PyDict_SetItemString(d, "VIDEO_TUNER_NORM", Py_BuildValue("i", VIDEO_TUNER_NORM));
    PyDict_SetItemString(d, "VIDEO_TUNER_STEREO_ON", Py_BuildValue("i", VIDEO_TUNER_STEREO_ON));
    PyDict_SetItemString(d, "VIDEO_TUNER_RDS_ON", Py_BuildValue("i", VIDEO_TUNER_RDS_ON));
    PyDict_SetItemString(d, "VIDEO_TUNER_MBS_ON", Py_BuildValue("i", VIDEO_TUNER_MBS_ON));

    PyDict_SetItemString(d, "VIDEO_MODE_PAL", Py_BuildValue("i", VIDEO_MODE_PAL));
    PyDict_SetItemString(d, "VIDEO_MODE_NTSC", Py_BuildValue("i", VIDEO_MODE_NTSC));
    PyDict_SetItemString(d, "VIDEO_MODE_SECAM", Py_BuildValue("i", VIDEO_MODE_SECAM));
    PyDict_SetItemString(d, "VIDEO_MODE_AUTO", Py_BuildValue("i", VIDEO_MODE_AUTO));

    PyDict_SetItemString(d, "VIDEO_PALETTE_GREY", Py_BuildValue("i", VIDEO_PALETTE_GREY));
    PyDict_SetItemString(d, "VIDEO_PALETTE_HI240", Py_BuildValue("i", VIDEO_PALETTE_HI240));
    PyDict_SetItemString(d, "VIDEO_PALETTE_RGB565", Py_BuildValue("i", VIDEO_PALETTE_RGB565));
    PyDict_SetItemString(d, "VIDEO_PALETTE_RGB24", Py_BuildValue("i", VIDEO_PALETTE_RGB24));
    PyDict_SetItemString(d, "VIDEO_PALETTE_RGB32", Py_BuildValue("i", VIDEO_PALETTE_RGB32));
    PyDict_SetItemString(d, "VIDEO_PALETTE_RGB555", Py_BuildValue("i", VIDEO_PALETTE_RGB555));
    PyDict_SetItemString(d, "VIDEO_PALETTE_YUV422", Py_BuildValue("i", VIDEO_PALETTE_YUV422));
    PyDict_SetItemString(d, "VIDEO_PALETTE_YUYV", Py_BuildValue("i", VIDEO_PALETTE_YUYV));
    PyDict_SetItemString(d, "VIDEO_PALETTE_UYVY", Py_BuildValue("i", VIDEO_PALETTE_UYVY));
    PyDict_SetItemString(d, "VIDEO_PALETTE_YUV420", Py_BuildValue("i", VIDEO_PALETTE_YUV420));
    PyDict_SetItemString(d, "VIDEO_PALETTE_YUV411", Py_BuildValue("i", VIDEO_PALETTE_YUV411));
    PyDict_SetItemString(d, "VIDEO_PALETTE_RAW", Py_BuildValue("i", VIDEO_PALETTE_RAW));
    PyDict_SetItemString(d, "VIDEO_PALETTE_YUV422P", Py_BuildValue("i", VIDEO_PALETTE_YUV422P));
    PyDict_SetItemString(d, "VIDEO_PALETTE_YUV411P", Py_BuildValue("i", VIDEO_PALETTE_YUV411P));
    PyDict_SetItemString(d, "VIDEO_PALETTE_YUV420P", Py_BuildValue("i", VIDEO_PALETTE_YUV420P));
    PyDict_SetItemString(d, "VIDEO_PALETTE_YUV410P", Py_BuildValue("i", VIDEO_PALETTE_YUV410P));
    PyDict_SetItemString(d, "VIDEO_PALETTE_PLANAR", Py_BuildValue("i", VIDEO_PALETTE_PLANAR));
    PyDict_SetItemString(d, "VIDEO_PALETTE_COMPONENT", Py_BuildValue("i", VIDEO_PALETTE_COMPONENT));

    PyDict_SetItemString(d, "VIDEO_AUDIO_MUTE", Py_BuildValue("i", VIDEO_AUDIO_MUTE));
    PyDict_SetItemString(d, "VIDEO_AUDIO_MUTABLE", Py_BuildValue("i", VIDEO_AUDIO_MUTABLE));
    PyDict_SetItemString(d, "VIDEO_AUDIO_VOLUME", Py_BuildValue("i", VIDEO_AUDIO_VOLUME));
    PyDict_SetItemString(d, "VIDEO_AUDIO_BASS", Py_BuildValue("i", VIDEO_AUDIO_BASS));
    PyDict_SetItemString(d, "VIDEO_AUDIO_TREBLE", Py_BuildValue("i", VIDEO_AUDIO_TREBLE));
    PyDict_SetItemString(d, "VIDEO_AUDIO_BALANCE", Py_BuildValue("i", VIDEO_AUDIO_BALANCE));
    PyDict_SetItemString(d, "VIDEO_SOUND_MONO", Py_BuildValue("i", VIDEO_SOUND_MONO));
    PyDict_SetItemString(d, "VIDEO_SOUND_STEREO", Py_BuildValue("i", VIDEO_SOUND_STEREO));
    PyDict_SetItemString(d, "VIDEO_SOUND_LANG1", Py_BuildValue("i", VIDEO_SOUND_LANG1));
    PyDict_SetItemString(d, "VIDEO_SOUND_LANG2", Py_BuildValue("i", VIDEO_SOUND_LANG2));

}

