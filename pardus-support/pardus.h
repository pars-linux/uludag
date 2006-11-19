#ifndef PARDUS_H
#define PARDUS_H

#include <qstring.h>

class Pardus {

 public:
  Pardus();

  static QString lower(const char* value);
  static QString upper(const char* value);

};

#endif
