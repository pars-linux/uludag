#include <iostream>
#include <qapplication.h>
#include <qstring.h>

#include "debug.h"

using namespace std;

void Debug::printDebug(const QString &msg)
{
    cerr << DEBUGCOLOR << "DEBUG: " << msg << DEFAULTCOLOR << endl;
}

void Debug::printWarning(const QString &msg)
{
    cerr << WARNINGCOLOR << "WARNING: " << msg << DEFAULTCOLOR << endl;
}

void Debug::printError(const QString &msg)
{
    cerr << ERRORCOLOR << "ERROR: " << msg << DEFAULTCOLOR << endl;
}
