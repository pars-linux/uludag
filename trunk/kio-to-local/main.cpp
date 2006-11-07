#include <qfileinfo.h>

#include <kapplication.h>
#include <kaboutdata.h>
#include <kcmdlineargs.h>
#include <kurl.h>
#include <kio/netaccess.h>
#include <kmessagebox.h>
#include <kprocess.h>

static const char description[] = "External KIO support for non-KDE programs";
static const char version[] = "0.5";
static KCmdLineOptions options[] =
{
    { "+program", "Program to run", 0 },
    { "+url", "URL to process", 0 },
    KCmdLineLastOption
};

void runProgramWithURL(const QString& program, const QString& url)
{
  KProcess proc;
  proc << program;
  proc << url.local8Bit();
  proc.start(KProcess::Block);
}

int main(int argc, char **argv)
{
    KAboutData about("kio-to-local","kio-to-local" , version, description,
                     KAboutData::License_GPL, "", 0, 0, "ismail@pardus.org.tr");
    about.addAuthor("İsmail Dönmez","Author","ismail@pardus.org.tr",
                    "http://www.pardus.org.tr");
    KCmdLineArgs::init(argc, argv, &about);
    KCmdLineArgs::addCmdLineOptions(options);
    KApplication app;
    KCmdLineArgs *args = KCmdLineArgs::parsedArgs();

    switch(args->count())
      {
      case 0:
        KCmdLineArgs::usage("Command and URL expected.\n");
        break;
      case 1:
        KCmdLineArgs::usage("URL expected.\n");
        break;
      case 2:
        {
          const QString program = args->arg(0);
          const KURL target = args->url(1);

          if (target.isLocalFile())
            {
              const KURL url = KIO::NetAccess::mostLocalURL(target,0);
              runProgramWithURL(program, url.path());
            }
          else // A remote URL or kioslave
            {
              QString original, destination;

              original = QString("/tmp/%1").arg(target.fileName());
              destination = original;

              unsigned int i = 1;
              // Protect against symlink attacks
              while(QFileInfo(destination).isSymLink())
                {

                  destination = original.section(".",-2,0) + "_"
                    + QString::number(i) + "." + original.section(".",-1);
                  ++i;
                }

              if (KIO::NetAccess::download(target, destination, NULL))
                {
                  runProgramWithURL(program, destination);
                }
              else
                {
                  const QString error = KIO::NetAccess::lastErrorString();
                  if (!error.isEmpty())
                    KMessageBox::error(NULL, error);

                  KIO::NetAccess::removeTempFile(destination);
                  return 1;
                }
            }
          break;
        }
      default:
        KCmdLineArgs::usage("Only one command and one URL expected.\n");
        break;
      }

    return 0;
}
