import sys

from PyQt4 import QtCore, QtGui
import QtPoppler


class PDFDisplay(QtGui.QWidget):
    def __init__(self, doc):
        QtGui.QWidget.__init__(self, None)
        self.doc = doc
        self.pixmap = None
        self.currentPage = 0
        self.display()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        if self.pixmap is not None:
            painter.drawPixmap(0, 0, self.pixmap)
        else:
            print "No Pixmap"

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Down:
            if self.currentPage + 1 < self.doc.numPages():
                self.currentPage += 1
                self.display()
        elif event.key() == QtCore.Qt.Key_Up:
            if self.currentPage > 0:
                self.currentPage -= 1
                self.display()
        elif (event.key() == QtCore.Qt.Key_Q):
            sys.exit(0)
    
    def display(self):
        if self.doc is not None:
            page = self.doc.page(self.currentPage)
            if page:
                self.pixmap = None
                self.pixmap = page.splashRenderToPixmap()
                self.update()
                #delete page;
        else:
            print "doc not loaded"


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    d = QtPoppler.Poppler.Document.load(sys.argv[1])
    disp = PDFDisplay(d)
    disp.show()
    sys.exit(app.exec_())