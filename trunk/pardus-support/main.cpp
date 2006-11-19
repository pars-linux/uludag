#include "pardus.h"
#include <iostream>

using namespace std;

int main()
{
  cout << "TÜRKİYE == " << Pardus::upper("türkiye") << endl;
  cout << "türkıye == " << Pardus::lower("TURKIYE") << endl;

  return 0;
}
