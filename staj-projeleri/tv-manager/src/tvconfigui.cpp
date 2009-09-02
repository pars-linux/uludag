#include "tvconfigui.h"
#include "ui_tvconfigui.h"

TvConfigUI::TvConfigUI(QWidget *parent)
    : QWidget(parent), ui(new Ui::TvConfigUI)
{
    ui->setupUi(this);
}

TvConfigUI::~TvConfigUI()
{
    delete ui;
}
