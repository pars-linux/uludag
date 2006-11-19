#include <unicode/unistr.h>
#include <unicode/locid.h>

#include <pardus.h>

QString Pardus::upper(const char* value, const char* language)
{
  if (!language)
    language = getenv("LC_CTYPE");

  UnicodeString us(value);
  us = us.toUpper(Locale(language));

  unsigned long long len = us.length();

  if (len*8 > 1<<32 - 1)
    len = 1<<32 - 1;
  else
    len = len*8;

  char charBuf[len];
  us.extract(0, us.length(), charBuf, sizeof(charBuf)-1, 0);
  charBuf[sizeof(charBuf)-1] = 0;

  return QString(charBuf);
}

QString Pardus::lower(const char* value, const char* language)
{
  if (!language)
    language = getenv("LC_CTYPE");

  UnicodeString us(value);
  us = us.toLower(Locale(language));

  unsigned long long len = us.length();

  if (len*8 > 1<<32 - 1)
    len = 1<<32 - 1;
  else
    len = len*8;

  char charBuf[len];
  us.extract(0, us.length(), charBuf, sizeof(charBuf)-1, 0);
  charBuf[sizeof(charBuf)-1] = 0;

  return QString(charBuf);
}
