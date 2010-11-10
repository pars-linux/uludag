#include <kauth.h>

using namespace KAuth;

class Helper : public QObject
{
    Q_OBJECT

    public slots:
        ActionReply managekeyboard(QVariantMap args);

    private:
        bool writeKeyboard(const QString &variants, const QString &layouts);
        ActionReply createReply(int code, const QVariantMap *returnData = 0);

};
