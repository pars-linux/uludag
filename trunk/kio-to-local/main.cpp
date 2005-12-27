#include <iostream>
using namespace std;

#include <kapplication.h>
#include <kaboutdata.h>
#include <kcmdlineargs.h>
#include <klocale.h>
#include <kurl.h>
#include <kio/netaccess.h>

static const char description[] = I18N_NOOP("KIO URL to Local URL Converter");

static const char version[] = "0.1";

static KCmdLineOptions options[] =
{
    { "+[URL]", I18N_NOOP( "URL to convert" ), 0 },
    KCmdLineLastOption
};

int main(int argc, char **argv)
{
    KAboutData about("kio-to-local","KIO URL to Local URL Converter" , version, description, KAboutData::License_GPL, "", 0, 0, "ismail@uludag.org.tr");
    about.addAuthor("İsmail Dönmez",I18N_NOOP("Author"),"ismail@uludag.org.tr","http://www.uludag.org.tr");
    KCmdLineArgs::init(argc, argv, &about);
    KCmdLineArgs::addCmdLineOptions(options);
    KApplication app;
    KCmdLineArgs *args = KCmdLineArgs::parsedArgs();
    
    if( args->count() )
    {
        KURL url = KIO::NetAccess::mostLocalURL(args->url(0),0);
        cout << url.path().local8Bit() << endl;
    }

    return 0;
}
