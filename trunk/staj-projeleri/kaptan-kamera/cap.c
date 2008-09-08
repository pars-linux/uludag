/********************************************************
 *                                                      *
 * Written by Onur Kücük                                *
 *                                                      *
 * Captures frame from cam that uses v4l1 driver        *
 *                                                      *
 ********************************************************/
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <sys/mman.h>
#include <time.h>

// #include <errno.h>

#include "SDL/SDL.h"
#include <linux/videodev.h>

#define 	mywidth 320 
#define 	myheight 240 


static struct	video_capability  capability;
static struct	video_picture picture;
static int 	fd = -1;
static struct 	video_mbuf gb_buffers = { 2*mywidth*myheight*3, 0, {0,mywidth*myheight*3 }};
static char 	*map = NULL;
static struct 	video_mmap my_buf;

struct video_channel vch;

clock_t		cstart=0;
clock_t		clast=0;
float		fps;
int		frame_count=0;


SDL_Surface *screen;
SDL_Surface *offscreen;
SDL_Event event; 


void palette_name(char *palet_tipi_str, int palette_number) {

	printf("\n gelen palet numarasi %i \n\n", palette_number);
	switch (palette_number) {
	case VIDEO_PALETTE_GREY:    strcpy( palet_tipi_str, "VIDEO_PALETTE_GREY");
				    break;
	case VIDEO_PALETTE_HI240:   strcpy( palet_tipi_str, "VIDEO_PALETTE_HI240");
				    break;
	case VIDEO_PALETTE_RGB565:  strcpy( palet_tipi_str, "VIDEO_PALETTE_RGB565");
				    break;
	case VIDEO_PALETTE_RGB24:   strcpy( palet_tipi_str, "VIDEO_PALETTE_RGB24");
				    break;
	case VIDEO_PALETTE_RGB32:   strcpy( palet_tipi_str, "VIDEO_PALETTE_RGB32");
				    break;
	case VIDEO_PALETTE_RGB555:  strcpy( palet_tipi_str, "VIDEO_PALETTE_RGB555");
				    break;
	case VIDEO_PALETTE_YUV422:  strcpy( palet_tipi_str, "VIDEO_PALETTE_YUV422");
				    break;
	case VIDEO_PALETTE_YUYV:    strcpy( palet_tipi_str, "VIDEO_PALETTE_YUYV");
				    break;
	case VIDEO_PALETTE_UYVY:    strcpy( palet_tipi_str, "VIDEO_PALETTE_UYVY");
				    break;
	case VIDEO_PALETTE_YUV420:  strcpy( palet_tipi_str, "VIDEO_PALETTE_YUV420");
				    break;
	case VIDEO_PALETTE_YUV411:  strcpy( palet_tipi_str, "VIDEO_PALETTE_YUV411");
				    break;
	case VIDEO_PALETTE_RAW:     strcpy( palet_tipi_str, "VIDEO_PALETTE_RAW");
				    break;
	case VIDEO_PALETTE_YUV422P: strcpy( palet_tipi_str, "VIDEO_PALETTE_YUV422P");
				    break;
	case VIDEO_PALETTE_YUV420P: strcpy( palet_tipi_str, "VIDEO_PALETTE_YUV420P");
				    break;
	case VIDEO_PALETTE_YUV411P: strcpy( palet_tipi_str, "VIDEO_PALETTE_YUV411P");
				    break;
	case VIDEO_PALETTE_YUV410P: strcpy( palet_tipi_str, "VIDEO_PALETTE_YUV410P");
				    break;
	default:                    strcpy( palet_tipi_str, "unknown");
				    break;
	
	}
}


void copytoscreen(char* tmap) {
	int loop=0;
	do{
		SDL_PollEvent(&event);
		if (event.type == SDL_KEYDOWN) {
			close(fd);
			SDL_Quit();
			exit(0);
		}
		// usleep(20);
	} while(loop++<20);
	offscreen = SDL_CreateRGBSurfaceFrom((void *) tmap, mywidth, myheight, 24, mywidth*3, 0xFF0000, 0x00FF00, 0x0000FF, 0x000000);
	SDL_BlitSurface(offscreen, NULL, screen, NULL);
	SDL_UpdateRect(screen, 0, 0, 0, 0);
	SDL_FreeSurface(offscreen);
}


int main(void)
{
   char my_video_dev[20]  = "/dev/video0";

   
   if (-1 == (fd = open(my_video_dev, O_RDWR))) {
	printf("Error opening device: %s\n", my_video_dev);
	goto error;
   }

   if (-1 == ioctl(fd,VIDIOCGCAP,&capability)) {
	printf("Error: ioctl(fd,VIDIOCGCAP,&capability)\n");
	goto error;
   }

	printf("\n -----[  VIDIOCGCAP returns ]-----\n");
	printf(" name:      %s\n", capability.name);
	printf(" type:      %i\n", capability.type);
	printf(" channels:  %i\n", capability.channels);
	printf(" audios:    %i\n", capability.audios);
	printf(" maxwidth:  %i\n", capability.maxwidth);
	printf(" maxheight: %i\n", capability.maxheight);
	printf(" minwidth:  %i\n", capability.minwidth);
	printf(" minheight: %i\n", capability.minheight);

	
   if (-1 == ioctl(fd,VIDIOCGPICT,&picture)) {
	printf("Error: ioctl(fd,VIDIOCGCPICT,&capability)\n");
	goto error;
   }

	printf("\n -----[  VIDIOCGPICT returns ]-----\n");
	printf(" brightness: %i\n", picture.brightness);
	printf(" hue:        %i\n", picture.hue);
	printf(" colour:     %i\n", picture.colour);
	printf(" contrast:   %i\n", picture.contrast);
	printf(" whiteness:  %i\n", picture.whiteness);
	printf(" depth:      %i\n", picture.depth);

	char static palet_tipi_str[64];
	palette_name(palet_tipi_str, picture.palette);
	printf(" palette:    %s\n\n", palet_tipi_str);

	

   vch.channel = 0;
   // vch.norm = VIDEO_MODE_PAL;
   
   if(-1 == ioctl(fd, VIDIOCSCHAN,&vch)) {
        perror("Setting channel\n");
	goto error;
   }
   
   fcntl(fd,F_SETFD,FD_CLOEXEC);
   if (-1 == ioctl(fd,VIDIOCGMBUF,&gb_buffers)) {
	printf("Error: Error getting buffers\n");
	goto error;
   }

   map = mmap(0,gb_buffers.size,PROT_READ|PROT_WRITE,MAP_SHARED,fd,0); 
   if (map == NULL) {
	printf("Error: Mmap returned NULL\n");
	goto error;
   }

   // Set up out capture to use the correct resolution
   
   my_buf.width = mywidth;
   my_buf.height = myheight;
   my_buf.format = VIDEO_PALETTE_RGB24;

   // Set up out video output

   SDL_Init(SDL_INIT_VIDEO);
   screen = SDL_SetVideoMode(mywidth, myheight, 24, SDL_SWSURFACE);
   if ( screen == NULL ) {
	fprintf(stderr, "Couldn't set video mode: %s\n",
	SDL_GetError());
	exit(1);
   }
   SDL_WM_SetCaption("Oy oy oy teve pirogrami", NULL);

   // Tell the capture card to fill frame 0
   
   my_buf.frame = 0;
   if (-1 == ioctl(fd, VIDIOCMCAPTURE, &my_buf)) { 
	printf(" ilk my_buf.frame=0 da hata olustu\n");
	// printf("Error: Grabber chip can't sync (no station tuned in?)\n"); 
	goto error;
   }

   // This is the infinate loop
   // We basically:
   //	capture frame 1
   //   sync frame 0
   //   process frame 0
   //	capture frame 0 
   //   sync frame 1
   //   process frame 1
   // For more information, read the programming how-to that came with xawtv
   
   do {

	my_buf.frame = 1;
	if (-1 == ioctl(fd, VIDIOCMCAPTURE, &my_buf)) {
		printf(" loop icinde frame=1 \n");
		// printf("Error: Grabber chip can't sync (no station tuned in?)\n"); 
		goto error;
	}
 
	my_buf.frame = 0;
	if (-1 == ioctl(fd, VIDIOCSYNC, &my_buf.frame)) {
		 printf("Error on sync!\n"); 
		goto error;
	}

	copytoscreen(map);

	my_buf.frame = 0;
	if (-1 == ioctl(fd, VIDIOCMCAPTURE, &my_buf)) {
		printf(" loop icinde frame=0 \n");
		// printf("Error: Grabber chip can't sync (no station tuned in?)\n"); 
		goto error;
	}

	my_buf.frame = 1;
	if (-1 == ioctl(fd, VIDIOCSYNC, &my_buf.frame)) {
		printf("Error on sync!\n"); 
		goto error;
	}

	copytoscreen(map + gb_buffers.offsets[1]);
	SDL_PollEvent(&event);
   } while (event.type != SDL_KEYDOWN);

   error:

	SDL_Quit();
   	return EXIT_SUCCESS;

}



