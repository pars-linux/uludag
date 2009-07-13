#include <QObject>
#include <QSet>

#include "../bindings/stream.h"

class GroupManager;

class Group: public QObject
{
    Q_OBJECT
    public:
    Group(QtPulseAudio::StreamManager *s, GroupManager *parent);
    QString streamTitle(int index);
    QString streamIcon(int index);
    QString streamInfo(int index);
    
    public slots:
    void addStream(int index);
    void removeStream(int index);
    //void streamChanged();
    void setVolume(int volume);
    signals:
    void streamAdded(int index);
    void streamRemoved(int index);
    protected:
    QSet<int> indexes;
    QtPulseAudio::StreamManager *manager;
};
