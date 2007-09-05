from qt import *

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
        self.initImage = self.image = QImage()
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
    
        self.pixmap = QPixmap(self.image.width(),self.image.height())
    
    def sizeHint(self):
        return self.image.size()
    
    def paintEvent(self,event):
        rect = event.rect()
        self.pixmap.resize(rect.size())
        painter = QPainter(self.pixmap)
        painter.translate(-rect.x(),-rect.y())
        painter.drawImage(rect.topLeft(),self.image,rect)
        
        if self.selectionExists and self.tl_X != self.br_X and self.tl_Y != self.br_Y:
            painter.setPen(Qt.white)
            painter.fillRect(0,0,self.image.width(),self.tl_Y,QBrush(QColor(66,66,90),QBrush.Dense5Pattern))
            painter.fillRect(0,self.tl_Y,self.tl_X,self.image.height(),QBrush(QColor(66,66,90),QBrush.Dense5Pattern))
            painter.fillRect(self.br_X,self.tl_Y,self.image.width(),self.image.height(),QBrush(QColor(66,66,90),QBrush.Dense5Pattern))
            painter.fillRect(self.tl_X,self.br_Y,self.br_X,self.image.height(),QBrush(QColor(66,66,90),QBrush.Dense5Pattern))
            painter.drawRect(self.tl_X,self.tl_Y,self.br_X-self.tl_X+1,self.br_Y-self.tl_Y+1)
            
    
            painter.setPen(Qt.DotLine)
            painter.drawRect(self.tl_X,self.tl_Y,self.br_X-self.tl_X+1,self.br_Y-self.tl_Y+1)
            
        painter.end()
        bitBlt(self,rect.topLeft(),self.pixmap)
        
        if self.needsReposition:
            self.emit(PYSIGNAL("needsReposition"),(int((self.tl_X+self.br_X)/2),int((self.tl_Y+self.br_Y)/2)))
            self.needsReposition = False
        
        
        
    def mousePressEvent(self,event):
        self.pressedButton = event.button()
        if event.button() == Qt.LeftButton:
            if self.move == None:
                self.tl_X = event.x()
                self.tl_Y = event.y()
                self.br_X = event.x()
                self.br_Y = event.y()
                if self.tl_X < 0: self.tl_X = 0
                elif self.tl_X > self.image.width(): self.tl_X = self.image.width()-1
                if self.tl_Y < 0: self.tl_Y = 0
                elif self.tl_Y > self.image.height(): self.tl_Y = self.image.height()-1
            elif self.move == Move.ALL:
                self.dtl_X = event.x() - self.tl_X
                self.dtl_Y = event.y() - self.tl_Y
                self.dbr_X = self.br_X - event.x()
                self.dbr_Y = self.br_Y - event.y()

    def mouseMoveEvent(self,event):
        if self.pressedButton == Qt.LeftButton:
            x = event.x()
            if x<0: x = 0
            elif x>=self.image.width(): x = self.image.width() - 1 
               
            y = event.y()
            if y<0: y = 0
            elif y>=self.image.height(): y = self.image.height() - 1

            if self.move == None:
                self.selectionExists = True
                self.br_X = x
                self.br_Y = y
            elif self.move == Move.ALL:
                if (x - self.dtl_X)<0:
                    x = self.dtl_X

                if (y - self.dtl_Y)<0: 
                    y = self.dtl_Y
                
                if (x + self.dbr_X)>=self.image.width():
                    x = self.image.width() - self.dbr_X - 1
                
                if (y + self.dbr_Y)>=self.image.height():
                    y = self.image.height() - self.dbr_Y - 1

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
            self.update()
        elif self.pressedButton == None and self.selectionExists==True:
            if event.x() > self.tl_X - 3 and event.x() <     self.tl_X + 3 and event.y() > self.tl_Y - 3 and event.y() < self.tl_Y + 3:
                self.setCursor(Qt.sizeFDiagCursor)
                self.move = Move.TOP_LEFT
            elif event.x() > self.tl_X - 3 and event.x() < self.tl_X + 3 and event.y() > self.br_Y - 3 and event.y() < self.br_Y + 3:
                self.setCursor(Qt.sizeBDiagCursor)
                self.move = Move.BOTTOM_LEFT
            elif event.x() > self.br_X - 3 and event.x() < self.br_X + 3 and event.y() > self.tl_Y - 3 and event.y() < self.tl_Y + 3:
                self.setCursor(Qt.sizeBDiagCursor)
                self.move = Move.TOP_RIGHT
            elif event.x() > self.br_X - 3 and event.x() < self.br_X + 3 and event.y() > self.br_Y - 3 and event.y() < self.br_Y + 3:
                self.setCursor(Qt.sizeFDiagCursor)
                self.move = Move.BOTTOM_RIGHT
            elif event.x() > self.tl_X - 3 and event.x() < self.tl_X + 3 and event.y() > self.tl_Y and event.y() < self.br_Y:
                self.setCursor(Qt.sizeHorCursor)
                self.move = Move.LEFT
            elif event.y() > self.tl_Y - 3 and event.y() < self.tl_Y + 3 and event.x() > self.tl_X and event.x() < self.br_X:
                self.setCursor(Qt.sizeVerCursor)
                self.move = Move.TOP
            elif event.x() > self.br_X - 3 and event.x() < self.br_X + 3 and event.y() > self.tl_Y and event.y() < self.br_Y:
                self.setCursor(Qt.sizeHorCursor)
                self.move = Move.RIGHT
            elif event.y() > self.br_Y - 3 and event.y() < self.br_Y + 3 and event.x() > self.tl_X and event.x() < self.br_X:
                self.setCursor(Qt.sizeVerCursor)
                self.move = Move.BOTTOM
            elif event.x() > self.tl_X and event.x() < self.br_X and event.y() > self.tl_Y and event.y() < self.br_Y:
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
                self.tl_X = self.origtl_X = 0
                self.tl_Y = self.origtl_Y = 0
                self.br_X = self.origbr_X = 0
                self.br_Y = self.origbr_Y = 0
                self.selectionExists = False
                self.update()
                self.emit(PYSIGNAL("selectionCreated"),(0,0,0,0))
            else:
                if self.tl_X > self.br_X:
                    self.tl_X, self.br_X = self.br_X, self.tl_X
                if self.tl_Y > self.br_Y:
                    self.tl_Y, self.br_Y = self.br_Y, self.tl_Y

                self.origtl_X = self.tl_X / self.scaleFactor
                self.origtl_Y = self.tl_Y / self.scaleFactor
                self.origbr_X = self.br_X / self.scaleFactor
                self.origbr_Y = self.br_Y / self.scaleFactor
                self.selectionExists = True
                self.update()
                self.emit(PYSIGNAL("selectionCreated"),(float(self.origtl_X)/self.initImage.width(),float(self.origtl_Y)/self.initImage.height(),float(self.origbr_X+1)/self.initImage.width(),float(self.origbr_Y+1)/self.initImage.height()))

    def mouseDoubleClickEvent(self,event):
        self.fit()

    def setImage(self,image):
        self.initImage = image
        self.fit()

    def zoomactual(self):
        self.scaleFactor = 1;
        
        self.tl_X = self.origtl_X
        self.tl_Y = self.origtl_Y
        self.br_X = self.origbr_X
        self.br_Y = self.origbr_Y
        
        self.image = QImage(self.initImage)
        self.updateGeometry()
        self.update()

    def zoomin(self):
        self.scaleFactor *= 1.1
        
        self.tl_X *= 1.1
        self.tl_Y *= 1.1
        self.br_X *= 1.1
        self.br_Y *= 1.1
        
        self.image = self.initImage.smoothScale(self.initImage.width()*self.scaleFactor,self.initImage.height()*self.scaleFactor,QImage.ScaleMax)
        self.update()
        self.updateGeometry()

    def zoomout(self):
        self.scaleFactor *= 0.909
        
        self.tl_X *= 0.909
        self.tl_Y *= 0.909
        self.br_X *= 0.909
        self.br_Y *= 0.909
        
        self.image = self.initImage.smoothScale(self.initImage.width()*self.scaleFactor,self.initImage.height()*self.scaleFactor,QImage.ScaleMax)
        self.update()
        self.updateGeometry()

    def fitSelect(self):
        if self.selectionExists:
            width = self.parent.width() - 20
            height = self.parent.height() - 20
            
            widthImage = self.origbr_X - self.origtl_X
            heightImage = self.origbr_Y - self.origtl_Y
            
            sc = float(width) / widthImage
            if sc > float(height)/heightImage:
                sc = float(height)/heightImage
            
            self.scaleFactor = sc
            
            self.tl_X = self.origtl_X * self.scaleFactor
            self.tl_Y = self.origtl_Y * self.scaleFactor
            self.br_X = self.origbr_X * self.scaleFactor
            self.br_Y = self.origbr_Y * self.scaleFactor
            
            self.image = self.initImage.smoothScale(self.initImage.width()*self.scaleFactor,self.initImage.height()*self.scaleFactor,QImage.ScaleMin)
            self.updateGeometry()
            self.needsReposition = True
            self.update()
        

    def fit(self):
        width = self.parent.width()
        height = self.parent.height()
        
        widthImage = self.initImage.width()
        heightImage = self.initImage.height()
        
        sc = float(width) / widthImage
        if sc > float(height)/heightImage:
            sc = float(height)/heightImage
        
        self.scaleFactor = sc
        
        self.tl_X = self.origtl_X * self.scaleFactor
        self.tl_Y = self.origtl_Y * self.scaleFactor
        self.br_X = self.origbr_X * self.scaleFactor
        self.br_Y = self.origbr_Y * self.scaleFactor
        
        self.image = self.initImage.smoothScale(self.initImage.width()*self.scaleFactor,self.initImage.height()*self.scaleFactor,QImage.ScaleMin)
        self.update()
        self.updateGeometry()