#!/usr/bin/env python

# Author: Andrew Wilson

#Boa:App:BoaApp
 
from wxPython.wx import *
import v4l
 
WIDTH=640
HEIGHT=480
 
[wxID_WXFRAME_MAIN] = map(lambda _init_ctrls: wxNewId(), range(1))
 
class wxFrame_Main(wxFrame):
    def _init_ctrls(self, prnt):
        wxFrame.__init__(self, id=wxID_WXFRAME_MAIN, name='wxFrame_Main',
              parent=prnt, pos=wxPoint(0,0), size=wxSize(WIDTH, HEIGHT),
              style=wxDEFAULT_FRAME_STYLE, title='wxPyV4L')
        self.SetClientSize(wxSize(WIDTH, HEIGHT))
        self.Center(wxBOTH)
        EVT_IDLE(self, self.OnWxframe1Idle)  ##where the frames get written
 
    def __init__(self, parent):
        self._init_ctrls(parent)

	self.vid = v4l.video('/dev/video')
	cap = self.vid.getCapabilities()
	print "Device Name: %s" % cap[0]
	print "Type: %d" % cap[1]
	print "Channels: %d" % cap[2]
	print "Audios: %d" % cap[3]
	print "Maximum Width: %d" % cap[4]
	print "Maximum Height: %d" % cap[5]
	print "Minimum Width: %d" % cap[6]
	print "Minimum Height: %d" % cap[7]
	self.vid.setupImage(WIDTH, HEIGHT)
	print self.vid.getChannel(1) # TV
	 
        self.vid.preQueueFrames()
        self.nextFrame = 0;
        self.vid.mute()
 
        self.im = wxEmptyImage(WIDTH,HEIGHT)
        self.bitmap = wxEmptyBitmap(WIDTH,HEIGHT)  
 
    def OnWxframe1Idle(self, event):    
        ##update the frames
        self.im.SetData(self.vid.getImage(self.nextFrame))        
        self.bitmap = self.im.ConvertToBitmap()
        self.nextFrame = self.vid.queueFrame()  
 
        ##now draw the image to the screen
        self.dc=wxBufferedPaintDC(self,self.bitmap)
        self.dc.DrawBitmap(self.bitmap,0,0,False)
        event.RequestMore()  ##this forces it to update!!
 
class BoaApp(wxApp):
    def OnInit(self):
        wxInitAllImageHandlers()
        self.main = wxFrame_Main(None) ##.create(None)
        self.main.Show();
        return True
 
def main():
    application = BoaApp(0)
    application.MainLoop()
 
if __name__ == '__main__':
    main()
