# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os
import sys
import signal
import time

import opencv
from opencv.cv import *
from opencv.highgui import *

import Image
import ImageQt

from PyQt4.QtCore import *
from PyKDE4.kdecore import ki18n
from PyQt4 import QtGui, QtCore

#from facedetector import FaceDetector
from gui.ScreenWidget import ScreenWidget
from gui.cameraWidget import Ui_cameraWidget

import dbus
class WebcamDetector:
    def __init__(self):
	self.cameradevices = []
	self.cameradevicenums = []
	bus = dbus.SystemBus()

	proxy = bus.get_object('org.freedesktop.Hal', '/org/freedesktop/Hal/Manager')
	iface = dbus.Interface(proxy, dbus_interface='org.freedesktop.Hal.Manager')

	devices = iface.FindDeviceByCapability("video4linux")

	for dev in devices:
	    d_proxy = bus.get_object('org.freedesktop.Hal', dev)
	    d_iface = dbus.Interface(d_proxy, dbus_interface='org.freedesktop.Hal.Device')

	    capa = [h for h in d_iface.GetProperty("info.capabilities") if "." in h]
	    if len(capa) == 1 and capa[0] == "video4linux.video_capture":
		self.cameradevicenums.append(int((d_iface.GetProperty("video4linux.device"))[-1]))
		self.cameradevices.append(d_iface.GetProperty("info.product"))
    def count(self):
    	return len(self.cameradevices)
    def listDevices(self):
	    return (self.cameradevices,self.cameradevicenums)

class FaceDetector:
    cascade_path = "/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml" 		# Haar algoritması için önden yüz verisi
    min_size = cvSize(30,30)	# Minimum yüz boyutları
    image_scale = 1.4		# Görüntüyü küçültme oranı
    # Ardışık aramalarda arama penceresinin boyutunun büyüme katsayısı. 1.2 daha hızlı
    haar_scale = 1.2		
    min_neighbors = 2		# 2 olursa daha hızlı, ama daha başarısız
    haar_flags = CV_HAAR_DO_CANNY_PRUNING		# CV_HAAR_DO_CANNY_PRUNING kullanılırsa işlem hızlanır

    def __init__(self, cam_no = -1):
	# Hafızadan yer al. Parametre olarak 0 verilirse, varsayılan boyutta alan alır(~64 k)
	self.storage = cvCreateMemStorage(0)
        # Bu fonksiyon obsolete ama cvLoad'un değerini HaarClassifierCascade'e cast
        # edemiyoruz diye mecburen kullanıyoruz
        self.cascade = cvLoadHaarClassifierCascade(self.cascade_path, cvSize(1, 1))
	# Kameradan görüntü almak için işlemleri yap. sadece bir kamera varsa veya hangi kameranın
	# kullanılacağı önemli değilse -1 verilebilir
        #capture = cvCreateCameraCapture(cam_no)
	
    def detect(self,camera):
        # Kamera veya görüntüden bir kare al
        frame = cvQueryFrame(camera)
	if not frame:
	    return (None,None)
	cropped = cvCreateImage( cvSize(240, 240), 8, 3)
	src_region = cvGetSubRect(frame, opencv.cvRect(0, 0, 240, 240) )
	cvCopy(src_region, cropped)
	frame = cropped
	# cvQueryFrame ile alınan görüntü değiştirilemeyeceğinden, kopyala
        copy = cvCreateImage(cvSize(frame.width, frame.height), IPL_DEPTH_8U, frame.nChannels)
	
	
	# Eğer kameradan alınan görüntünün orijin noktası sol üst köşe ise(top down), kopyala
        if (frame.origin == IPL_ORIGIN_TL):
            cvCopy(frame, copy)
	# Değilse(bottom up IPL_ORIGIN_BL ise), x ekseni etrafında döndür ve kopyala
        else:
            cvFlip(frame, copy, 0)
        
        # image_scale a göre küçült
        small_img = cvCreateImage(cvSize(cvRound(copy.width / self.image_scale), cvRound(copy.height / self.image_scale)), 8, 1)
	# küçültülmemiş kopyasını yap
        gray = cvCreateImage(cvSize(copy.width, copy.height), 8, 1)
	# grileştir
        cvCvtColor(copy, gray, CV_BGR2GRAY)
	# küçük gri halini small_img'a koy
        cvResize(gray, small_img, CV_INTER_LINEAR)
	# parlaklığını normalleştir ve kontrastı arttır
        cvEqualizeHist(small_img, small_img)
        # storage'ı temizle. bu fonksiyon hafızadan alanı deallocate etmez!
        cvClearMemStorage(self.storage)
        
        # Yüz tanıma işlemi
        t = cvGetTickCount()
        faces = cvHaarDetectObjects(
            small_img, 		# yüzlerin aranacağı görüntü
            self.cascade,	# önceden belirli tanıma verisi
            self.storage,	# sonuçların tutulacağı hafıza bölgesi
	    # aşağıdakilerin açıklaması sınıf tanımlamasının başında
            self.haar_scale,		
            self.min_neighbors,
            self.haar_flags,
	    self.min_size
        )
        t = cvGetTickCount() - t
        #print "detection time = %gms" % (t/(cvGetTickFrequency()*1000.))
        return frame, faces
    def count(self):
        # Tanınan yüz sayısını döndür	
        faces = self.detect()
        if faces:
            count = 0
            for face in faces:
                count += 1
            return count
        else:
            return 0


## kamera işlemimiz sürekli olarak ekrana görüntüyü basıyor...

class camThread(QtCore.QThread):
    def __init__(self,cam):
        QtCore.QThread.__init__(self)
        self.camera = cam
        self.camTimer = QTimer(self)
        QtCore.QObject.connect(self.camTimer, SIGNAL("timeout()"), self.update)
    def stopThread(self):
        self.camTimer.stop()
        #self.quit(self)
    def run(self):
        #alttaki iki satir calismiyor, calissa program daha hizli isleyecek..
    	cvSetCaptureProperty(self.camera, CV_CAP_PROP_FRAME_WIDTH, 320)
    	cvSetCaptureProperty(self.camera, CV_CAP_PROP_FRAME_HEIGHT, 240)
    	self.detector = FaceDetector()
        self.camTimer.start(40) #25 fps olarak varsayilmis. TODO: fps yi ogren ona gore yap
    	self.exec_()
    def update(self):
        frame, faces = self.detector.detect(self.camera)
    	if not frame:
    	    self.emit(QtCore.SIGNAL("noimage"))
    	    return
    	originalFrame = cvCloneImage(frame)
    	#processedImage = cvCloneImage(frame)
    	#copy = cvCloneImage(frame)
    	#processedImage = cvCreateImage(cvSize(64,48), 8, copy.nChannels)
    	#cvResize(copy, processedImage, CV_INTER_LINEAR)
    	scale = self.detector.image_scale
    	thickness = 1	
    	if faces:
            for face in faces:
                #yuzun etrafina cizilecek dikdortgenin koselerin koordinatlarini bul
                x = int(face.x * scale)- thickness
                y = int(face.y * scale)- thickness
                x2 = int((face.x + face.width) * scale) + thickness
                y2 = int((face.y + face.height) * scale) + thickness
                p1 = cvPoint(x, y)
                p2 = cvPoint(x2, y2)
                #kirmizi dikdortgen
                cvRectangle(frame, p1, p2, CV_RGB(255,0,0), thickness, 8, 0)
        self.emit(QtCore.SIGNAL("image"), (originalFrame ,frame))

class Widget(QtGui.QWidget, ScreenWidget):
    title = ki18n("Camera")
    desc = ki18n("Welcome to Kaptan Wizard :)")
    
    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_cameraWidget()
        self.ui.setupUi(self)	
        self.detector = WebcamDetector()
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.isCaptureFlag = False
        self.isTaken = False
        #populate cameras combo box. if there is only one camera, don't show the combobox.
        self.ui.cameraCombo.hide()
        if (self.detector.count() > 1): ####DEGISECEK
            cams = self.detector.listDevices()[0]
            for cam in cams:
                self.ui.cameraCombo.addItem(cam)
            self.ui.cameraCombo.show()
        self.camindex = (self.detector.listDevices()[1][0])	
        #create camera
        self.camera = cvCreateCameraCapture(self.camindex)
        #signal/slot connections
        QtGui.QWidget.connect(self.ui.captureButton,QtCore.SIGNAL("clicked(bool)"),self.takePhoto)
        QtGui.QWidget.connect(self.ui.cameraCombo,QtCore.SIGNAL("currentIndexChanged(int)"), self.slotCameraChanged)
	
    def slotCameraChanged(self,index):
        self.terminateCam()
        self.camindex = (self.detector.listDevices()[1][index])
        #self.camera = None
        #self.camera = cvCreateCameraCapture(self.camindex)
        self.initializeCam()
	
    def takePhoto(self):
        if self.isCaptureFlag:
            self.isCaptureFlag = False
            self.isTaken = True
            #change the image from Ipl to PIL for being able to use it in Qt
            self.image = ImageQt.ImageQt(opencv.adaptors.Ipl2PIL(self.originalFrame).transpose(Image.FLIP_LEFT_RIGHT))
            self.ui.displayLabel.setPixmap(QtGui.QPixmap.fromImage(self.image))
            #resize photo for avatar
            processedImage = cvCreateImage(cvSize(60,60), 8, self.originalFrame.nChannels)
            cvResize(self.originalFrame, processedImage, CV_INTER_LINEAR)
            #find homedir
            homedir = os.path.expanduser("~")
            #save the image
            ImageQt.ImageQt(opencv.adaptors.Ipl2PIL(processedImage).transpose(Image.FLIP_LEFT_RIGHT)).save(homedir + "/kaptantmp.png")
            os.rename(homedir + "/kaptantmp.png",homedir + "/.face.icon")
            
            self.ui.captureButton.setText(ki18n("Recapture").toString())

            self.terminateCam()
        else:
            self.isCaptureFlag = True
            self.isTaken = False
            #self.camera = cvCreateCameraCapture(self.camindex)
            self.initializeCam()
            self.ui.captureButton.setText(ki18n("Capture").toString())

    def initializeCam(self):
        #print("caminitializeCam",self.camera)
        self.camThread = camThread(self.camera)
        self.connect(self.camThread, QtCore.SIGNAL("image"), self.showImage)
        self.connect(self.camThread, QtCore.SIGNAL("noimage"), self.handleCameraProblem)
        self.connect(self,QtCore.SIGNAL('kapan'),self.camThread.stopThread)
        self.camThread.start()	

    def handleCameraProblem(self):
        self.terminateCam()
        self.ui.displayLabel.setText(ki18n("A Problem has occurred. Either your camera is unrecognized or there is a transmisson error").toString())
	
    def showImage(self, image):
        try:
            self.originalFrame = image[0]
            resizedImage = image[1]
    
            self.image = ImageQt.ImageQt(opencv.adaptors.Ipl2PIL(resizedImage).transpose(Image.FLIP_LEFT_RIGHT))

            self.ui.displayLabel.setPixmap(QtGui.QPixmap.fromImage(self.image))
        except TypeError:
            print("No CAM")
            self.terminateCam()

    def shown(self):
        if not self.isTaken and not self.isCaptureFlag:
            self.initializeCam()
            self.isCaptureFlag = True
        pass
    
    def terminateCam(self):
        #cvReleaseCapture(self.camindex)
        self.emit(QtCore.SIGNAL("kapan"))
        if self.camThread:
            self.camThread.terminate()
        self.camThread = None
    def execute(self):
        if not self.isTaken:
            self.terminateCam()
            self.isCaptureFlag = False

        return True
