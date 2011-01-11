#include <QtCore/QString>

class GlInfo

{
public:

    void getGlStrings();
    const char *glVendor;
    const char *glRenderer;
    const char *glVersion;

};

