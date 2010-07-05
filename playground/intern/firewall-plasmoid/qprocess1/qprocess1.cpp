#This program was written to learn how to use qprocess in qt framework
#Baris Akkurt
#qprocess library gives us a chance to execute unix command in a cpp program
#qprocess is similar to c's system() function and python's os.system() function

#include <QProcess>
#include <QObject>
#include <iostream>
#include <QStringList>

int main()
{
   /*
    QObject *parent;
    QString program = "konsole";
    QStringList arguments;
    arguments << "ls" << "-l";

    QProcess *myProcess = new QProcess(parent);
    myProcess->start(program, arguments);
    return 0;*/
    
    /*
    QProcess gzip;
    gzip.start("bash -c");
    //assert(gzip.waitForStarted());
    gzip.write("ls");
    gzip.closeWriteChannel();
    QByteArray result = gzip.readAll();
    
    std::cout << result.data() ;
    
    gzip.close();*/

    QString a="ls";
    QStringList b;
    b<<"-l";
    QProcess::execute(a,b);

}
