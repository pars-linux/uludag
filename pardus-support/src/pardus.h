#ifndef PARDUS_H
#define PARDUS_H

#include <qstring.h>

class Pardus {

 public:
  Pardus();

  static QString lower(const QString& value);
  static QString upper(const QString& value);

};

#endif
