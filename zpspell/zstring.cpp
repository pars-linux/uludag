#include <iostream>
#include <sstream>
#include <algorithm>

#include "zstring.h"

ZString::ZString(const string& str, int offset )
    : _str(str), _offset(offset),
      _status(Z_UNKNOWN)
{}


/* set */
void ZString::setStatus( enum Z_CHECK_RESULT status )
{
    _status = status;
}

void ZString::setSuggestions( const vector<string>& suggestions)
{
    _suggestions = suggestions;
}

void ZString::addSuggestion( const string& suggestion )
{
    _suggestions.push_back( suggestion );
}

/* get */
int ZString::offset() const
{
    return _offset;
}

const string& ZString::str() const
{
    return _str;
}

enum Z_CHECK_RESULT ZString::status() const
{
    return _status;
}

int ZString::suggestionCount() const
{
    return _suggestions.size();
}

const string ZString::suggestionString() const
{
/*
    stringstream sstr;

    copy( _suggestions.begin(), _suggestions.end(),
          ostream_iterator<string>(sstr, ", "));
    return sstr.str();
*/

    stringstream sstr;

    vector<string>::const_iterator it = _suggestions.begin();
    int len = _suggestions.size();
    for (int i=0 ; i < len ; ++i, ++it ) {
        sstr << *it;
        if ( i < len-1 ) {
            sstr << ", ";
        }
    }

    return sstr.str();
}

const vector<string>& ZString::suggestions() const
{
    return _suggestions;
}



