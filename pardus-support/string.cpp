#include <unicode/unistr.h>

#include <pardus.h>

QString Pardus::upper(const QString& value)
{
  UnicodeString us(value);
  us = us.toUpper();

  return QString((const QChar*)us.getBuffer(),us.length());
}

QString Pardus::lower(const QString& value)
{
  UnicodeString us(value);
  us = us.toLower();

  return QString((const QChar*)us.getBuffer(),us.length());
}
