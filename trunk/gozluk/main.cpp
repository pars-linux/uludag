#include <qapplication.h>

#include "anapencere.h"


int main(int argc, char **argv)
{
	QApplication uyg(argc, argv);
	anaPencere k;
	k.show();
	
	uyg.setMainWidget(&k);
	return uyg.exec();
}
