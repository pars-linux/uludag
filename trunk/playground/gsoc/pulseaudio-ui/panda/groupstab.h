#include<QWidget>
#include<QVBoxLayout>
#include<QScrollArea>

class GroupManager;

class GroupsTab: public QWidget
{
    Q_OBJECT
    public:
    GroupsTab(GroupManager *manager, QWidget *parent);
    protected slots:
    void createGroup(QString name);
    void removeGroup(QString name);
    protected:
    GroupManager *manager;
    QScrollArea *scrollArea;
    QVBoxLayout *scrolledLayout;
    QWidget *scrolledWidget;
    QVBoxLayout *layout;
};