#include <QtGui/QApplication>
#include "tvconfigui.h"

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    TvConfigUI w;
    w.show();
    return a.exec();
}
