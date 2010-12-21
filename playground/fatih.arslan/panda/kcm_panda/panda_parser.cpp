
/*
  Copyright (c) 1997 Christian Czezatke (e9025461@student.tuwien.ac.at)
                1998 Bernd Wuebben <wuebben@kde.org>
                2000 Matthias Elter <elter@kde.org>
                2001 Carsten PFeiffer <pfeiffer@kde.org>

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
*/
#include <panda_parser.h>
#include <kdebug.h>

#include <X11/Xlib.h>
#include <X11/Xutil.h>

// OpenGL includes
#include <GL/gl.h>
#include <GL/glext.h>
#include <GL/glx.h>


void PandaParser::getGlStrings()
{
  GLXContext ctx;
  char *displayName = NULL;
  int scrnum = 0;

  const int attribSingle[] = {
    GLX_RGBA,
    GLX_RED_SIZE, 1,
    GLX_GREEN_SIZE, 1,
    GLX_BLUE_SIZE, 1,
    None };
  const int attribDouble[] = {
    GLX_RGBA,
    GLX_RED_SIZE, 1,
    GLX_GREEN_SIZE, 1,
    GLX_BLUE_SIZE, 1,
    GLX_DOUBLEBUFFER,
    None };

  Display *dpy = XOpenDisplay(displayName);
  unsigned long mask;
  XVisualInfo *visinfo;
  Window root, win;
  XSetWindowAttributes attr;

  root = DefaultRootWindow(dpy);

  visinfo = glXChooseVisual(dpy, scrnum, const_cast<int*>(attribSingle));
  if (!visinfo) {
     visinfo = glXChooseVisual(dpy, scrnum, const_cast<int*>(attribDouble));
     if (!visinfo) {
       kDebug() << "Error: couldn't find RGB GLX visual\n";
       return ;
     }
  }

  attr.colormap = XCreateColormap(dpy, root, visinfo->visual, AllocNone);
  attr.event_mask = StructureNotifyMask | ExposureMask;
  mask = CWBackPixel | CWBorderPixel | CWColormap | CWEventMask;
  win = XCreateWindow(dpy, root, 0, 0, 600, 600, 0, visinfo->depth, InputOutput, visinfo->visual, mask, &attr);

  ctx = glXCreateContext( dpy, visinfo, NULL, GL_TRUE);

  if (glXMakeCurrent(dpy, win, ctx)) {
    glVendor = (const char *) glGetString(GL_VENDOR);
    glRenderer = (const char *) glGetString(GL_RENDERER);
    glVersion = (const char *) glGetString(GL_VERSION);
  }

}
