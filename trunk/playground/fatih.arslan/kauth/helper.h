#include <kauth.h>
#define WriteKeyboardError 1

using namespace KAuth;

class Helper : public QObject
{
    Q_OBJECT

    public slots:
        ActionReply managekeyboard(QVariantMap args);

    private:
        bool writeKeyboard(const QString &layouts, const QString &variants);
        ActionReply createReply(int code, const QVariantMap *returnData = 0);

};
