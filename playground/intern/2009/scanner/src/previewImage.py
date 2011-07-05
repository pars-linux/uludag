from qt import *
import math

class Move:
    ALL,TOP_LEFT,TOP,TOP_RIGHT,RIGHT,BOTTOM_RIGHT,BOTTOM,BOTTOM_LEFT,LEFT = range(9)

class PreviewImage(QWidget):
    def __init__(self,parent,name=0):
        QWidget.__init__(self,parent,name)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.sizePolicy().hasHeightForWidth()))
        #self.setMinimumSize(QSize(280,410))
        #self.setMaximumSize(QSize(32767,32767))

        self.setBackgroundMode(Qt.NoBackground)

        self.parent = parent
        self.initImage = QImage()
        self.tl_X = self.origtl_X = 0
        self.tl_Y = self.origtl_Y = 0
        self.br_X = self.origbr_X = 0
        self.br_Y = self.origbr_Y = 0
        self.setMouseTracking(True)
        self.pressedButton = None
        self.move = None
        self.scaleFactor = 1
        self.selectionExists = False
        self.needsReposition = False
	self.fitted = True
    
        self.pixmap = QPixmap(self.initImage.width(),self.initImage.height())
    
    def sizeHint(self):
        return QSize(self.initImage.width()*self.scaleFactor,self.initImage.height()*self.scaleFactor)
    
    def paintEvent(self,event):
        rect = QRect(round(event.rect().x()/self.scaleFactor)-4,round(event.rect().y()/self.scaleFactor)-4,round(event.rect().width()/self.scaleFactor)+4,round(event.rect().height()/self.scaleFactor)+4)
        self.pixmap.resize(event.rect().size())
        painter = QPainter(self.pixmap)
        painter.translate(-event.rect().x(),-event.rect().y())
        painter.scale(self.scaleFactor,self.scaleFactor)
        
        
        painter.drawImage(rect.x(),rect.y(),self.initImage,rect.x(),rect.y(),rect.width(),rect.height())
        
        if self.selectionExists and self.tl_X != self.br_X and self.tl_Y != self.br_Y:
            painter.setPen(Qt.white)
            brush = QBrush(QColor(66,66,90),QBrush.Dense4Pattern)
            painter.fillRect(0,0,self.initImage.width()+1,self.tl_Y+1,brush)
            painter.fillRect(0,self.tl_Y,self.tl_X+1,self.initImage.height(),brush)
            painter.fillRect(self.br_X,self.tl_Y,self.initImage.width(),self.initImage.height(),brush)
            painter.fillRect(self.tl_X,self.br_Y,self.br_X+1,self.initImage.height(),brush)
            painter.drawRect(self.tl_X,self.tl_Y,self.br_X-self.tl_X+1,self.br_Y-self.tl_Y+1)
            
    
            painter.setPen(Qt.DotLine)
            painter.drawRect(self.tl_X,self.tl_Y,self.br_X-self.tl_X+1,self.br_Y-self.tl_Y+1)
            
        painter.end()
        bitBlt(self,event.rect().topLeft(),self.pixmap)
        
        if self.needsReposition:
            self.emit(PYSIGNAL("needsReposition"),(int((self.tl_X+self.br_X)/2*self.scaleFactor),int((self.tl_Y+self.br_Y)/2*self.scaleFactor)))
            self.needsReposition = False
        
        
        
    def mousePressEvent(self,event):
        self.pressedButton = event.button()
        if event.button() == Qt.LeftButton:
            x = round(event.x()/self.scaleFactor)
            y = round(event.y()/self.scaleFactor)
            if self.move == None:
                self.tl_X = x
                self.tl_Y = y
                self.br_X = x
                self.br_Y = y
                if self.tl_X < 0: self.tl_X = 0
                elif self.tl_X >= self.initImage.width(): self.tl_X = self.initImage.width() - 1
                if self.tl_Y < 0: self.tl_Y = 0
                elif self.tl_Y >= self.initImage.height(): self.tl_Y = self.initImage.height() - 1
            elif self.move == Move.ALL:
                self.dtl_X = x - self.tl_X
                self.dtl_Y = y - self.tl_Y
                self.dbr_X = self.br_X - x
                self.dbr_Y = self.br_Y - y

    def mouseMoveEvent(self,event):
        if self.pressedButton == Qt.LeftButton:
            x = round(event.x()/self.scaleFactor)
            if x<0: x = 0
            elif x>=self.initImage.width(): x = self.initImage.width() - 1 
               
            y = round(event.y()/self.scaleFactor)
            if y<0: y = 0
            elif y>=self.initImage.height(): y = self.initImage.height() - 1

            if self.move == None:
                self.selectionExists = True
                self.br_X = x
                self.br_Y = y
            elif self.move == Move.ALL:
                if (x - self.dtl_X)<0:
                    x = self.dtl_X

                if (y - self.dtl_Y)<0: 
                    y = self.dtl_Y
                
                if (x + self.dbr_X)>=self.initImage.width():
                    x = self.initImage.width() - self.dbr_X - 1
                
                if (y + self.dbr_Y)>=self.initImage.height():
                    y = self.initImage.height() - self.dbr_Y - 1

                self.tl_X = x - self.dtl_X
                self.tl_Y = y - self.dtl_Y
                self.br_X = x + self.dbr_X
                self.br_Y = y + self.dbr_Y
            elif self.move == Move.TOP_LEFT:
                self.tl_X = x
                self.tl_Y = y
            elif self.move == Move.TOP:
                self.tl_Y = y
            elif self.move == Move.TOP_RIGHT:
                self.tl_Y = y
                self.br_X = x
            elif self.move == Move.RIGHT:
                self.br_X = x
            elif self.move == Move.BOTTOM_RIGHT:
                self.br_X = x
                self.br_Y = y
            elif self.move == Move.BOTTOM:
                self.br_Y = y
            elif self.move == Move.BOTTOM_LEFT:
                self.br_Y = y
                self.tl_X = x
            elif self.move == Move.LEFT:
                self.tl_X = x
            if self.tl_X > self.br_X and self.tl_Y > self.br_Y:
                self.tl_X, self.br_X = self.br_X, self.tl_X
                self.tl_Y, self.br_Y = self.br_Y, self.tl_Y
                if self.move == Move.BOTTOM_RIGHT:
                    self.move = Move.TOP_LEFT
                else:
                    self.move = Move.BOTTOM_RIGHT
            if self.tl_X > self.br_X:
                self.tl_X, self.br_X = self.br_X, self.tl_X
                if self.move == Move.BOTTOM_RIGHT:
                    self.move = Move.BOTTOM_LEFT
                elif self.move == Move.BOTTOM_LEFT:
                    self.move = Move.BOTTOM_RIGHT
                elif self.move == Move.TOP_RIGHT:
                    self.move = Move.TOP_LEFT
                elif self.move == Move.TOP_LEFT:
                    self.move = Move.TOP_RIGHT
                elif self.move == Move.RIGHT:
                    self.move = Move.LEFT
                else:
                    self.move = Move.RIGHT
            if self.tl_Y > self.br_Y:
                self.tl_Y, self.br_Y = self.br_Y, self.tl_Y
                if self.move == Move.BOTTOM_RIGHT:
                    self.move = Move.TOP_RIGHT
                elif self.move == Move.TOP_RIGHT:
                    self.move = Move.BOTTOM_RIGHT
                elif self.move == Move.BOTTOM_LEFT:
                    self.move = Move.TOP_LEFT
                elif self.move == Move.TOP_LEFT:
                    self.move = Move.BOTTOM_LEFT
                elif self.move == Move.BOTTOM:
                    self.move = Move.TOP
                else:
                    self.move = Move.BOTTOM
            self.update()
        elif self.pressedButton == None and self.selectionExists==True:
            x = event.x()
            y = event.y()
            if x > self.tl_X*self.scaleFactor - 3 and x < self.tl_X*self.scaleFactor + 3 and y > self.tl_Y*self.scaleFactor - 3 and y < self.tl_Y*self.scaleFactor + 3:
                self.setCursor(Qt.sizeFDiagCursor)
                self.move = Move.TOP_LEFT
            elif x > self.tl_X*self.scaleFactor - 3 and x < self.tl_X*self.scaleFactor + 3 and y > self.br_Y*self.scaleFactor - 3 and y < self.br_Y*self.scaleFactor + 3:
                self.setCursor(Qt.sizeBDiagCursor)
                self.move = Move.BOTTOM_LEFT
            elif x > self.br_X*self.scaleFactor - 3 and x < self.br_X*self.scaleFactor + 3 and y > self.tl_Y*self.scaleFactor - 3 and y < self.tl_Y*self.scaleFactor + 3:
                self.setCursor(Qt.sizeBDiagCursor)
                self.move = Move.TOP_RIGHT
            elif x > self.br_X*self.scaleFactor - 3 and x < self.br_X*self.scaleFactor + 3 and y > self.br_Y*self.scaleFactor - 3 and y < self.br_Y*self.scaleFactor + 3:
                self.setCursor(Qt.sizeFDiagCursor)
                self.move = Move.BOTTOM_RIGHT
            elif x > self.tl_X*self.scaleFactor - 3 and x < self.tl_X*self.scaleFactor + 3 and y > self.tl_Y*self.scaleFactor and y < self.br_Y*self.scaleFactor:
                self.setCursor(Qt.sizeHorCursor)
                self.move = Move.LEFT
            elif y > self.tl_Y*self.scaleFactor - 3 and y < self.tl_Y*self.scaleFactor + 3 and x > self.tl_X*self.scaleFactor and x < self.br_X*self.scaleFactor:
                self.setCursor(Qt.sizeVerCursor)
                self.move = Move.TOP
            elif x > self.br_X*self.scaleFactor - 3 and x < self.br_X*self.scaleFactor + 3 and y > self.tl_Y*self.scaleFactor and y < self.br_Y*self.scaleFactor:
                self.setCursor(Qt.sizeHorCursor)
                self.move = Move.RIGHT
            elif y > self.br_Y*self.scaleFactor - 3 and y < self.br_Y*self.scaleFactor + 3 and x > self.tl_X*self.scaleFactor and x < self.br_X*self.scaleFactor:
                self.setCursor(Qt.sizeVerCursor)
                self.move = Move.BOTTOM
            elif x > self.tl_X*self.scaleFactor and x < self.br_X*self.scaleFactor and y > self.tl_Y*self.scaleFactor and y < self.br_Y*self.scaleFactor:
                self.setCursor(Qt.sizeAllCursor)
                self.move = Move.ALL
            else:
                self.setCursor(Qt.crossCursor)
                self.move = None
        else:
            self.setCursor(Qt.crossCursor)
            self.move = None

    def mouseReleaseEvent(self,event):
        if self.pressedButton == Qt.LeftButton:
            self.pressedButton = None
            if self.tl_X == self.br_X or self.tl_Y == self.br_Y:
                self.tl_X = 0
                self.tl_Y = 0
                self.br_X = 0
                self.br_Y = 0
                self.selectionExists = False
                self.update()
                self.emit(PYSIGNAL("selectionCreated"),(0,0,0,0))
            else:
                if self.tl_X > self.br_X:
                    self.tl_X, self.br_X = self.br_X, self.tl_X
                if self.tl_Y > self.br_Y:
                    self.tl_Y, self.br_Y = self.br_Y, self.tl_Y

                self.selectionExists = True
                self.update()
                self.emit(PYSIGNAL("selectionCreated"),(float(self.tl_X)/self.initImage.width(),
                                                        float(self.tl_Y)/self.initImage.height(),
                                                        float(self.br_X+1)/self.initImage.width(),
                                                        float(self.br_Y+1)/self.initImage.height()))

    def mouseDoubleClickEvent(self,event):
        if self.selectionExists:
            self.fitSelect()
        else:
            self.fit()

    def setImage(self,image):
        self.initImage = image
        self.fit()

    def zoomactual(self):
	
	width = qApp.desktop().width()
	height = qApp.desktop().height()

        widthImage = self.initImage.width()
        heightImage = self.initImage.height()
        
        sc = float(width) / widthImage
        if sc > float(height)/heightImage:
            sc = float(height)/heightImage
        
        self.scaleFactor = sc
	
	self.updateGeometry()
        self.needsReposition = True
        self.update()
	self.fitted = False
	
    def zoomin(self):
        self.scaleFactor *= 1.1
        self.updateGeometry()
        self.needsReposition = True
        self.update()
	self.fitted = False
        

    def zoomout(self):
        self.scaleFactor *= 0.909
        self.updateGeometry()
        self.needsReposition = True
        self.update()
	self.fitted = False
        

    def fitSelect(self):
        if self.selectionExists:
            width = self.parent.width() - 20
            height = self.parent.height() - 20
            
            widthImage = self.br_X - self.tl_X
            heightImage = self.br_Y - self.tl_Y
            
	    self.fitted = False
	    
	    if (widthImage != 0):
	        sc = float(width) / widthImage
	        if(heightImage != 0):
		    if sc > float(height)/heightImage:
		        sc = float(height)/heightImage
	        self.scaleFactor = sc
 
                self.updateGeometry()
                self.needsReposition = True
                self.update()

    def fit(self):
        width = self.parent.width()
        height = self.parent.height()
        
        widthImage = self.initImage.width()
        heightImage = self.initImage.height()
	self.fitted = True
        
	if (widthImage != 0):
	    sc = float(width) / widthImage
	    if(heightImage != 0):
	        if sc > float(height)/heightImage:
		    sc = float(height)/heightImage
	    self.scaleFactor = sc
            self.update()
            self.updateGeometry()