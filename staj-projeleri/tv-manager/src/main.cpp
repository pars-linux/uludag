#include <QtGui/QApplication>
#include <iostream>
#include "tvconfigui.h"
#include "tv-manager.h"

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    std::cout << "Main Hello"   << std::endl;
    TasmaTv w;
    // TvConfigUI w;
    w.QWidget::show();
    return a.exec();
}
