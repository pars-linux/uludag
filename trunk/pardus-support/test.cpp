#include <qstring.h>
#include <pardus.h>
#include <iostream>

using namespace std;

int main()
{
  QString test1, test2;

  test1 = "türkiye";
  test2 = "TURKIYE";

  cout << "TÜRKİYE == " << Pardus::upper(test1,"tr") << endl;
  cout << "turkıye == " << Pardus::lower(test2,"tr") << endl;

  return 0;
}
