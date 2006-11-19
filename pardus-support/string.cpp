#include <unicode/unistr.h>
#include <unicode/locid.h>

#include <pardus.h>

QString Pardus::upper(const char* value)
{
  UnicodeString us(value);
  us = us.toUpper(Locale(getenv("LC_ALL")));

  char charBuf[100];
  us.extract(0, us.length(), charBuf, sizeof(charBuf)-1, 0);
  charBuf[sizeof(charBuf)-1] = 0;

  return QString(charBuf);
}

QString Pardus::lower(const char* value)
{
  UnicodeString us(value);
  us = us.toLower(Locale(getenv("LC_ALL")));

  char charBuf[100];
  us.extract(0, us.length(), charBuf, sizeof(charBuf)-1, 0);
  charBuf[sizeof(charBuf)-1] = 0;

  return QString(charBuf);
}
