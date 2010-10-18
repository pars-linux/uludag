#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <GL/glx.h>
#include <stdio.h>

int main(void)
{
        int nDoubleBuffer = 0;
        int nHaveGL = 0;
    Display *pDisplay = 0;
        XVisualInfo* pVInfos = 0;
    XVisualInfo aVI;
    int nVisuals;
    int i;

    pDisplay = XOpenDisplay(NULL);

        pVInfos = XGetVisualInfo(pDisplay, VisualNoMask, &aVI, &nVisuals );

    for (i = 0; i < nVisuals; ++i)
    {
        glXGetConfig( pDisplay, &pVInfos[i], GLX_USE_GL, &nHaveGL );
        glXGetConfig( pDisplay, &pVInfos[i], GLX_DOUBLEBUFFER, 
            &nDoubleBuffer );
    }

    XCloseDisplay(pDisplay);
    fprintf(stderr, "All OK\n");
}

