#ifndef TVCONFIGUI_H
#define TVCONFIGUI_H

#include <QtGui/QWidget>

namespace Ui
{
    class TvConfigUI;
}

class TvConfigUI : public QWidget
{
    //Q_OBJECT

public:
    TvConfigUI(QWidget *parent = 0);
    ~TvConfigUI();

private:
    Ui::TvConfigUI *ui;
};

#endif // TVCONFIGUI_H
