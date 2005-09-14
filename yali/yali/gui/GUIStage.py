# -*- coding: utf-8 -*-

from qt import *

from yali.steps import Stages

##
# Stage widget
class Widget(QListView):

    _stages = None
    _color_current = "#000000"
    _color_inactive = "#999999"

    def __init__(self, *args):
        apply(QListView.__init__, (self,) + args)

        self._stages = Stages()

# do we need to show stage number? Currently we don't
#        self.addColumn(QString.null) # image
        self.addColumn(QString.null) # stage name
        self.header().hide()

        self.setSizePolicy( QSizePolicy(QSizePolicy.Minimum,
                                        QSizePolicy.Minimum))
        self.setFrameStyle(self.WinPanel |self.Plain)
        
        #TESTING
#        self.setFixedHeight(70)
        f = self.font()
        f.setBold(True)
        self.setFont(f)


    ##
    # add a new stage
    # @param num(int): stage number
    # @param text(string): stage text
    def addStage(self, num, text):
        # add a listview item...
        i = StageItem(self, num, text)

        self._stages.addStage(num, i)

        # FIXME: use an update() function
        self.setCurrent(self._stages.getCurrentIndex())
        self.setColumnWidth( 0, self.columnWidth( 0 ) + 10 );

    ##
    # set the current stage
    # @param num(int): stage number to be the current.
    def setCurrent(self, num):
        if num == self._stages.getCurrentIndex():
            return

        self._stages.setCurrent(num)

        self.__update()


    ##
    # update the view. mark current item...
    def __update(self):
        c = self._stages.getCurrent()

        for i in self._stages.getAllItems():
            if i == c:
                i.setPixmap(0, QPixmap("pics/right_arrow.png"))
            else:
                i.setPixmap(0, QPixmap("pics/dot.png"))
#        self.setCurrentItem(i)
#        i.setText(0, "Test test")
#        i.repaint()


##
# Stage item
class StageItem(QListViewItem):

    _num = None

    def __init__(self, parent, num, text, *args):
        apply(QLabel.__init__, (self, parent, text) + args)
        
        self._num = num

    
    ##
    # get the stage number
    def getNumber(self):
        return self._num
