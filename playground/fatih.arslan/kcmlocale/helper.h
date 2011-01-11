#include <kauth.h>
#define WriteLocaleError 1

using namespace KAuth;

class Helper : public QObject
{
    Q_OBJECT

    public slots:
        ActionReply managelocale(QVariantMap args);

    private:
        bool writeLocale(const QString &locale);
        ActionReply createReply(int code, const QVariantMap *returnData = 0);

};
