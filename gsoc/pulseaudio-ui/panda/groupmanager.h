#include <QObject>
#include <QHash>
#include <QMap>

namespace QtPulseAudio
{
    class StreamManager;
    class Stream;
};

class Group;

class GroupManager: public QObject
{
    Q_OBJECT
    public:
    GroupManager(QtPulseAudio::StreamManager *manager, QObject *parent);
    public slots:
    void streamReady();
    void addStream(int index);
    void removeStream(int index);
    QList<QString> groupNames();
    Group *group(const QString &name);
    signals:
    void groupCreated(QString name);
    void groupRemoved(QString name);
    protected:
    void createGroup(const QString &name);
    void dispatchStream(QtPulseAudio::Stream *s);
    QMap<QString, Group *> groups;
    QMap<int, QString> streamGroup;
    QtPulseAudio::StreamManager *manager;
    
};
