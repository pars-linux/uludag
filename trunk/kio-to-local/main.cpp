#include <kapplication.h>
#include <kaboutdata.h>
#include <kcmdlineargs.h>
#include <kurl.h>
#include <kio/netaccess.h>
#include <kmessagebox.h>
#include <kprocess.h>
#include <ktempfile.h>

static const char description[] = "External KIO support for non-KDE programs";
static const char version[] = "0.6";
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
          const KURL target = KIO::NetAccess::mostLocalURL(args->url(1), NULL);

          if (target.isLocalFile())
            {
              runProgramWithURL(program, target.path());
            }
          else // A remote URL or a kioslave
            {
              const QString prefix = target.fileName().section('.',0,0)+'-';
              const QString extension = '.'+target.fileName().section('.',1,1);

              KTempFile tempFile(prefix,extension);
              tempFile.setAutoDelete(true);

              QString destination = tempFile.name();

              if (KIO::NetAccess::download(target, destination, NULL))
                {
                  runProgramWithURL(program, destination);
                }
              else
                {
                  const QString error = KIO::NetAccess::lastErrorString();
                  if (!error.isEmpty())
                    KMessageBox::error(NULL, error);

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
