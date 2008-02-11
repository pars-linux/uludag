#define DEBUGCOLOR "\033[32m"
#define WARNINGCOLOR "\033[33m"
#define ERRORCOLOR "\033[01;31m"
#define DEFAULTCOLOR "\033[0m"

class Debug
{
    public:
        static void printDebug(const QString &msg);
        static void printWarning(const QString &msg);
        static void printError(const QString &msg);
};
