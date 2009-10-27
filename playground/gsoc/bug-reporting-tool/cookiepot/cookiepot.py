#!/usr/bin/python
# -*- coding: utf-8 -*-

import cookielib
import os
import re
import sqlite3
import tempfile

from cStringIO import StringIO


class CookiePot(object):
    """The CookiePot class centralizes methods to extract cookie info from
    the most common web browsers out there.
    """

    def __init__(self, domain_pattern=''):
        """Contructor.
        If desired, `default_pattern` may be given to fetch only cookies from
        a specific domain.
        """
        self.pattern = domain_pattern


    def _extract_cookies(self, cookies):
        """Extracts `Cookie` objects from `CookieJar._cookies` dictionaries.
        """
        ck_list = []
        for i in cookies.values():
            for j in i.values():
                ck_list += j.values()
        return ck_list


    def _profile_walker(self, path, filename):
        """Walks a browser `pathname` searching for a `cookiefile`.

        Note that this is not a recursive find. It is assumed that the
        cookies may be located at /`pathname`/PROFILE_NAME/`cookiefile`.
        """
        try:
            for f in os.listdir(path):
                fullpath = os.path.join(path, f)
                if os.path.isdir(fullpath):
                    if filename in os.listdir(fullpath):
                        yield os.path.join(fullpath, filename)
        except OSError:
            pass


    def seamonkey_cookies(self, pattern=None, path='~/.mozilla/default',
                          cookie_file='cookies.txt'):
        """Fetches cookies stored on SeaMonkey profiles in the user home.
        """
        if pattern is None:
            pattern = self.pattern

        dom = re.compile(".*%s.*" % re.escape(pattern), re.I)
        base_path = os.path.expanduser(path)
        cookies = []
        for txt in self._profile_walker(base_path, cookie_file):
            cj = cookielib.MozillaCookieJar(txt)
            cj.load()
            cookies += self._extract_cookies(cj._cookies)
        return [c for c in cookies if dom.search(c.domain)]


    def flock_cookies(self, pattern=None):
        """Fetches cookies stored on Flock profiles in the user home.
        """
        return self.firefox_cookies(pattern, '~/.flock/browser')


    def firefox_cookies(self, pattern=None, path='~/.mozilla/firefox',
                        cookie_file='cookies.sqlite'):
        """Fetches cookies stored on Firefox3 profiles in the user home.

        Credits: Noah Fontes nfontes AT cynigram DOT com
        """
        if pattern is None:
            pattern = self.pattern
        base_path = os.path.expanduser(path)

        match = '%%%s%%' % pattern
        operation = ('select host, path, isSecure, expiry, name, value from'
                     ' moz_cookies where host like ?')
        fmt = "%s\t%s\t%s\t%s\t%s\t%s\t%s\n"
        ftstr = ["FALSE","TRUE"]
        cookies = []
        for db in self._profile_walker(base_path, cookie_file):
            connection = sqlite3.connect(db, timeout=1)
            cursor = connection.cursor()
            try:
                cursor.execute(operation, [match])
            except sqlite3.OperationalError:
                # Firefox 3.5 workaround {{{
                # Since this version, the cookies database is locked whenever
                # Firefox is open.
                connection.close()
                database_file = file(db)
                tmp = tempfile.NamedTemporaryFile()
                tmp.write(database_file.read())
                tmp.flush()
                tmp.seek(0)
                database_file.close()
                connection = sqlite3.connect(tmp.name)
                cursor = connection.cursor()
                cursor.execute(operation, [match])
                tmp.close() # }}}

            out = StringIO()
            out.write("# Netscape HTTP Cookie File\n")
            for item in cursor.fetchall():
                out.write(fmt % (item[0], ftstr[item[0].startswith('.')],
                                 item[1], ftstr[item[2]], item[3], item[4],
                                 item[5]))
            connection.close()
            out.seek(0)

            cookie_jar = cookielib.MozillaCookieJar()
            cookie_jar._really_load(out, None, True, True)
            cookies += self._extract_cookies(cookie_jar._cookies)
        return cookies


    def get_cookies(self, pattern=None):
        """Returns every available cookie from CookiePot's known sources.
        """
        if pattern is None:
            pattern = self.pattern

        cookies = []
        cookies += self.firefox_cookies(pattern)
        cookies += self.flock_cookies(pattern)
        cookies += self.seamonkey_cookies(pattern)

        #TODO: implement other browser extractors
        return cookies


    def make_lwp_cookiejar(self, filename=None, pattern=None):
        """Creates a `LWPCookieJar` object with every known cookie.
        The `filename` parameter is used for the cookiejar creation and is
        relative to the cwd, if set.
        """
        if pattern is None:
            pattern = self.pattern

        cookies = self.get_cookies(pattern)
        cj = cookielib.LWPCookieJar(filename)
        for cookie in cookies:
            cj.set_cookie(cookie)
        return cj


if __name__ == '__main__':
    import sys
    cookiepot = CookiePot()
    cj = None
    if len(sys.argv) == 1:
        cj = cookiepot.make_lwp_cookiejar()
    else:
        cj = cookiepot.make_lwp_cookiejar('ck.txt', sys.argv[1])
    print cj
