#include <QtGui/QApplication>
#include <QTranslator>
#include <QLocale>
#include <iostream>
#include "tvconfigui.h"
#include "tv-manager.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    QTranslator translator;
    translator.load(QString("tvManager_") + QLocale::system().name());
    app.installTranslator(&translator);
    TasmaTv w;
    // TvConfigUI w;
    w.show();
    return app.exec();
}
