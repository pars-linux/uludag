#include<QWidget>
#include<QListWidget>
#include<QVBoxLayout>
#include<QMap>

class Group;

class GroupWidget: public QWidget
{
    Q_OBJECT
    public:
    GroupWidget(Group *g, QWidget *parent);
    protected slots:
    void streamAdded(int index);
    void streamRemoved(int index);
    protected:
    Group *group;
    QVBoxLayout *layout;
    QListWidget *listWidget;
    QSlider* volumeSlider;
    QMap<int, QListWidgetItem *> itemMap;
};
