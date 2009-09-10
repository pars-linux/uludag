#include <iostream>
#include "tvconfigui.h"
//#include "ui_tvconfigui.h"

TvConfigUI::TvConfigUI(QWidget *parent) : QWidget(*parent)
//    : QWidget(parent), ui(new Ui::TvConfigUI)
{
    std::cout << "tv-configui signaling" << std::endl;
    // ui->setupUi(this);
    setupUi(this);
    std::cout << "tv-configui awakened" << std::endl;
}

TvConfigUI::~TvConfigUI()
{
    // delete ui;
}
