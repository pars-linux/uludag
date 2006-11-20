#include <unicode/unistr.h>

#include <pardus.h>

QString Pardus::upper(const QString& value)
{
  UnicodeString us(FALSE /* Not NUL-terminated */, (const UChar *)value.unicode(), (int32_t)value.length());
  us = us.toUpper();

  return QString((const QChar*)us.getBuffer(),us.length());
}

QString Pardus::lower(const QString& value)
{
  UnicodeString us(FALSE /* Not NUL-terminated */, (const UChar *)value.unicode(), (int32_t)value.length());
  us = us.toLower();

  return QString((const QChar*)us.getBuffer(),us.length());
}
