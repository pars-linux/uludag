#include <iostream>
using namespace std;

#include <qfileinfo.h>

#include <kapplication.h>
#include <kaboutdata.h>
#include <kcmdlineargs.h>
#include <klocale.h>
#include <kurl.h>
#include <kio/netaccess.h>
#include <kmessagebox.h>

static const char description[] = I18N_NOOP("KIO URL to Local URL Converter");

static const char version[] = "0.3";

static KCmdLineOptions options[] =
{
    { "+[URL]", I18N_NOOP( "URL to process" ), 0 },
    KCmdLineLastOption
};

int main(int argc, char **argv)
{
    KAboutData about("kio-to-local","Enables non-KDE apps to use KIO" , version, description, KAboutData::License_GPL, "", 0, 0, "ismail@pardus.org.tr");
    about.addAuthor("İsmail Dönmez",I18N_NOOP("Author"),"ismail@pardus.org.tr","http://www.pardus.org.tr");
    KCmdLineArgs::init(argc, argv, &about);
    KCmdLineArgs::addCmdLineOptions(options);
    KApplication app;
    KCmdLineArgs *args = KCmdLineArgs::parsedArgs();
    
    if( args->count() )
    {
      const KURL target = args->url(0);

      if (target.isLocalFile())
        {
          KURL url = KIO::NetAccess::mostLocalURL(target,0);
          cout << url.path().local8Bit() << endl;
        }
      else
        {
          QString original = QString("/tmp/%1").arg(target.fileName());
          QString destination = original;
     
          unsigned int i=1;
          while(QFileInfo(destination).isSymLink()) // Protect against symlink attacks
            { 
              
              destination = original.section(".",-2,0) + "_" + QString::number(i) + "." + original.section(".",-1);
              ++i;
            }
                            
          if (KIO::NetAccess::download(target, destination, NULL))
            {
              cout << destination.local8Bit() << endl;
            }
          else
            {
              QString error =  KIO::NetAccess::lastErrorString();
              if (!error.isEmpty())
                KMessageBox::error(NULL, error);

              KIO::NetAccess::removeTempFile(destination);
              return 1;
            }
        }
    }

    return 0;
}
