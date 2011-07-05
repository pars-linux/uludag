#include "plasma-tutorial2.h"

#include <QPainter>
#include <QFontMetrics>
#include <QSizeF>
#include <QGraphicsLinearLayout>
#include <QDBusInterface>
#include <QIcon>
#include <QToolButton>
#include <QTextCodec>
 
#include <plasma/theme.h>
#include <plasma/widgets/lineedit.h>
#include <plasma/widgets/pushbutton.h>


//aşağıdaki kodları hata ayıkalama yapmak istiyorsanız açabilirsiniz
#include <iostream>
using namespace std;

 
PlasmaTutorial1::PlasmaTutorial1(QObject *parent, const QVariantList &args)
     : Plasma:: PopupApplet(parent, args), askiyaAl_pushButton(0), kapat_pushButton(0), yb_pushButton(0), ekraniKilitle_pushButton(0)//, dg_pushButton(0)  
     //işaretçilere 0 veya başka bir değer ata
{
    //setPopupIcon("calculator"); 
    setBackgroundHints(DefaultBackground); //standart arka plan
    
    resize(200, 200);   
}

void PlasmaTutorial1::askiyaAlma()
{
  QDBusInterface i(
		"org.freedesktop.Hal", //sol sutundaki kisim
		"/org/freedesktop/Hal/devices/computer",//sagdaki bolulu kisim
		"org.freedesktop.Hal.Device.SystemPowerManagement", //arayüz
		QDBusConnection::systemBus()
	);
  i.call("Suspend", 0);  //Suspend yöntemin adıdır.
}

void PlasmaTutorial1::bilgisayariKapat()
{
  QDBusInterface i(
		"org.freedesktop.Hal", //sol sutundaki kisim
		"/org/freedesktop/Hal/devices/computer",//sagdaki bolulu kisim
		"org.freedesktop.Hal.Device.SystemPowerManagement", //arayüz
		QDBusConnection::systemBus()
	);
  i.call("Shutdown");  //Suspend yöntemin adıdır.
}

void PlasmaTutorial1::yenidenBaslat()
{
  QDBusInterface i(
		"org.freedesktop.Hal", //sol sutundaki kisim
		"/org/freedesktop/Hal/devices/computer",//sagdaki bolulu kisim
		"org.freedesktop.Hal.Device.SystemPowerManagement", //arayüz
		QDBusConnection::systemBus()
	);
  i.call("Reboot");  //Suspend yöntemin adıdır.
}

void PlasmaTutorial1::ekraniKilitle()
{
  QDBusInterface i(
		"org.kde.screensaver", //sol sutundaki kisim
		"/ScreenSaver",//sagdaki bolulu kisim
		"org.freedesktop.ScreenSaver", //arayüz
		QDBusConnection::sessionBus()
	);
  i.call("Lock");  
}
 
PlasmaTutorial1::~PlasmaTutorial1()
{
    if (hasFailedToLaunch()) {} 
    else {}
}
 
//GUI elemanlarını buraya ekle. Sadece çok temel şeyleri normal yapıcıya ekle
void PlasmaTutorial1::init()
{
  QTextCodec::setCodecForLocale( QTextCodec::codecForName("UTF-8") );//aşağıdaki üç satır türkçe karakterler için
  QTextCodec::setCodecForTr( QTextCodec::codecForName("UTF-8") );
  QTextCodec::setCodecForCStrings ( QTextCodec::codecForName("UTF-8") );

  QGraphicsLinearLayout *layout = new QGraphicsLinearLayout(this);
  layout->setOrientation(Qt::Vertical);
 
  kapat_pushButton = new Plasma::PushButton(this);
  kapat_pushButton->setIcon(KIcon("system-shutdown"));
  kapat_pushButton->setText("Bilgisayarı kapat");
  
  yb_pushButton = new Plasma::PushButton(this);
  yb_pushButton->setIcon(KIcon("system-reboot"));
  yb_pushButton->setText("Yeniden başlat");
  
  askiyaAl_pushButton=new Plasma::PushButton(this);
  askiyaAl_pushButton->setIcon(KIcon("system-suspend-hibernate"));
  askiyaAl_pushButton->setText("Askıya al");
  
  ekraniKilitle_pushButton = new Plasma::PushButton(this);
  ekraniKilitle_pushButton->setIcon(KIcon("system-lock-screen"));
  ekraniKilitle_pushButton->setText("Ekranı kilitle");
  

  layout->addItem(kapat_pushButton);
  layout->addItem(yb_pushButton); 
  layout->addItem(askiyaAl_pushButton);
  layout->addItem(ekraniKilitle_pushButton); 
  
  QObject::connect(askiyaAl_pushButton, SIGNAL(clicked()), this, SLOT(askiyaAlma()));
  QObject::connect(kapat_pushButton, SIGNAL(clicked()), this, SLOT(bilgisayariKapat()));
  QObject::connect(yb_pushButton, SIGNAL(clicked()), this, SLOT(yenidenBaslat()));
  QObject::connect(ekraniKilitle_pushButton, SIGNAL(clicked()), this, SLOT(ekraniKilitle()));
}

K_EXPORT_PLASMA_APPLET(kapatac, PlasmaTutorial1) //applet'i .desktop dosyası ile bağdaştırmak için.
 
#include "plasma-tutorial2.moc"
