# -*- coding: utf-8 -*-

import apport.crashdb
import atexit
import gzip
import os
import re
import tempfile

from base64 import b64decode
from bugz.bugzilla import Bugz
from bugz.config import config
from cookiepot import CookiePot
from email.parser import Parser
from StringIO import StringIO
from urlparse import urljoin
from urllib2 import build_opener, HTTPCookieProcessor



# FIXME: importing from apport.crashdb_impl.launchpad creates a requirement
#        of launchpadlib, which is not needed when using the Bugzilla backend
#        perhaps the best choice here is adding common data on crashdb.py
APPORT_FILES = ('Dependencies.txt', 'CoreDump.gz', 'ProcMaps.txt',
        'Traceback.txt', 'Disassembly.txt', 'Registers.txt', 'Stacktrace.txt',
        'ThreadStacktrace.txt', 'DpkgTerminalLog.txt', 'DpkgTerminalLog.gz')

# Helper classes {{{
class Bug(object):
    """
    This class abstracts operations on the ElementTree returned by bugz for a
    bug entry.
    Some attributes as lazilly evaluated to avoid a performance hit every time
    we instantiate a bug object.
    """

    def __init__(self, bug_id, node):
        """
        Constructor.

        bug_id -- The bug ID as specified by Bugzilla
        node -- The ElementTree object returned by bygz.get(id)
        """
        assert bug_id > 0, "The bug ID must be greater than zero"
        assert node, "Can't instantiate Bug without an ElementTree parameter"
        self.bug_id = bug_id
        self._node = node
        self.setup()


    def setup(self):
        """
        Initializes basic data.
        """
        self._comments = None
        self._attachments = None
        self._keywords = None
        self.title = self._node.find('//short_desc').text
        self.create_date = self._node.find('//creation_ts').text
        self.reporter = self._node.find('//reporter').text
        self.status = self._node.find('//bug_status').text
        try:
            self.resolution = self._node.find('//resolution').text
            if self.resolution == 'DUPLICATE':
                self.dup_id = int(self._node.find('//dup_id').text)
        except AttributeError:
            # Use empty string instead of None so we can search for
            # patterns inside bug.resolution easily
            self.resolution = ''
            self.dup_id = 0


    @property
    def description(self):
        """
        Returns the Bug's description by the commiter.
        """
        return self.comments[0]['text']


    @property
    def keywords(self):
        """
        A list of the keywords a bug has.
        """
        if self._keywords is not None:
            return self._keywords

        try:
            keys = self._node.find('//keywords').text
            self._keywords = keys.split(', ')
        except AttributeError:
            self._keywords = []
        return self._keywords


    @property
    def comments(self):
        """
        A list of comments on the bug.
        Each comment is represented as a dictionary with the following keys:
            * author
            * date
            * text
        """
        if self._comments is not None:
            return self._comments

        self._comments = []
        etree = self._node.findall('//long_desc')
        for tree in etree:
            comment = {
                'author': tree.find('.//who').text,
                'date': tree.find('.//bug_when').text,
                'text': tree.find('.//thetext').text,
            }
            self._comments.append(comment)
        return self._comments


    @property
    def attachments(self):
        """
        Returns a list of the bug's attachment.
        Each attachment is represented as a dictionary with the following keys:
            * id
            * date
            * description
            * filename
            * type
        """
        if self._attachments is not None:
            return self._attachments

        self._attachments = []
        etree = self._node.findall('//attachment')
        for tree in etree:
            if tree.attrib['isobsolete'] == '1':
                continue
            attachment = {
                'id': int(tree.find('.//attachid').text),
                'date': tree.find('.//date').text,
                'description': tree.find('.//desc').text,
                'filename': tree.find('.//filename').text,
                'type': tree.find('.//type').text,
            }
            self._attachments.append(attachment)
        return self._attachments
#}}}

class CrashDatabase(apport.crashdb.CrashDatabase):
    """
    Bugzilla implementation of crash database interface.
    """

    def __init__(self, auth, bugpattern_baseurl, options):
        """
        Constructor.

        auth_file -- authentication credentials
        bugpattern_baseurl -- base url for searching bug patterns
        options -- dictionary with settings from crashdb.conf
        """
        apport.crashdb.CrashDatabase.__init__(self, auth, bugpattern_baseurl,
                                              options)
        self.distro = options.get('distro')
        self.options = options
        self.auth = auth
        self.arch_tag = 'need-%s-retrace' % apport.packaging.get_system_architecture()

        self._bugzilla = None
        self._baseurl = None
        self.username = None
        self.password = None


    @property
    def bugzilla(self):
        """
        Return Bugzilla instance.
        TODO: check whether we should use cookies or not
        """
        if self._bugzilla is not None:
            return self._bugzilla

        self._baseurl = self.options.get('baseurl')
        self._bugzilla = Bugz(self._baseurl)
        cj = CookiePot().make_lwp_cookiejar(self._bugzilla.cookiejar.filename,
                                            self._bugzilla.host)
        self._bugzilla.cookiejar = cj
        self._bugzilla.opener = build_opener(HTTPCookieProcessor(cj))
        if self.username is None or self.password is None:
            if not self._bugzilla.try_auth():
                self._bugzilla = None
                raise apport.crashdb.NeedsCredentials, self.distro
        else:
            self._bugzilla = Bugz(self._baseurl, self.username, self.password)
            try:
                self._bugzilla.auth()
            except RuntimeError:
                # Happens when the username/password pair is invalid.
                raise apport.crashdb.NeedsCredentials, self.distro
        return self._bugzilla


    def set_credentials(self, username, password):
        """Sets username and password to be used on log-in."""
        self.username = username
        self.password = password


    def upload(self, report, progress_callback = None):
        '''Upload given problem report return a handle for it.

        This should happen noninteractively.

        If the implementation supports it, and a function progress_callback is
        passed, that is called repeatedly with two arguments: the number of
        bytes already sent, and the total number of bytes to send. This can be
        used to provide a proper upload progress indication on frontends.'''
        data = {}
        data.update(self.options['default_options'])

        # PyBugz mandatory args
        product = data.pop('product')
        component = data.pop('component')
        title = report.get('Title', report.standard_title())
        description = ''

        # generating mime (from launchpad.py)#{{{
        # set reprocessing tags
        hdr = {}
        hdr['Tags'] = 'apport-%s' % report['ProblemType'].lower()
        a = report.get('PackageArchitecture')
        if not a or a == 'all':
            a = report.get('Architecture')
        if a:
            hdr['Tags'] += ' ' + a
        if 'CoreDump' in report and a:
            hdr['Tags'] += ' need-%s-retrace' % a
        # set dup checking tag for Python crashes
        elif report.has_key('Traceback'):
            hdr['Tags'] += ' need-duplicate-check'

        # write MIME/Multipart version into temporary file
        mime = tempfile.NamedTemporaryFile()
        report.write_mime(mime, extra_headers=hdr)
        mime.flush()
        mime.seek(0)
        #}}}
        # Reding MIME data and uploading each file {{{
        #FIXME: there should be a standard way of getting this
        message = Parser().parse(mime)
        attachables = []
        for item in message.walk():
            filename = item.get_filename()
            # If "Content-Disposition" is inline, filename will be None
            if filename is not None:
                bdata = b64decode(item.get_payload())
                filetype = item.get_content_type()
                attachable = (filename, filetype, bdata)
                attachables.append(attachable)
            else:
                # Bug description is `inline`
                try:
                    description += b64decode(item.get_payload())
                except:
                    pass
        mime.close() # }}}

        # optional args
        if 'keywords' in data:
            data['keywords'] += hdr['Tags']
        else:
            data['keywords'] = hdr['Tags']
        #data.pop('keywords')

        bug_id = self.bugzilla.post(product, component, title, description,
                                    **data)
        if bug_id == 0:
            raise RuntimeError, "Error uploading bug!"

        for filename, filetype, data in attachables:
            tmp = tempfile.NamedTemporaryFile()
            tmp.write(data)
            tmp.flush()
            tmp.seek(0)
            result = self.bugzilla.attach(bug_id, filename, '', tmp.name,
                                          filetype, filename)
            if not result:
                raise RuntimeError, "Error uploading attachment"
            tmp.close()

        return bug_id


    def get_comment_url(self, report, handle):
        '''Return an URL that should be opened after report has been uploaded
        and upload() returned handle.

        Should return None if no URL should be opened (anonymous filing without
        user comments); in that case this function should do whichever
        interactive steps it wants to perform.'''

        url = '%s?id=%s' % (urljoin(self._baseurl, config.urls['show']),
                            handle)
        return url


    def download(self, bug_id):
        '''Download the problem report from given ID and return a Report.'''

        report = apport.Report()
        bug_etree = self.bugzilla.get(bug_id)
        bug = Bug(bug_id, bug_etree)

        # from launchpad crashdb
        # parse out fields from summary
        m = re.search(r'(ProblemType:.*)$', bug.description, re.S)
        if not m:
            m = re.search(r'^--- \r?$[\r\n]*(.*)', bug.description, re.M | re.S)
        assert m, 'bug description must contain standard apport format data'

        description = m.group(1).encode('UTF-8').replace('\xc2\xa0', ' ')

        if '\r\n\r\n' in description:
            # this often happens, remove all empty lines between top and
            # 'Uname'
            if 'Uname:' in description:
                # this will take care of bugs like LP #315728 where stuff
                # is added after the apport data
                (part1, part2) = description.split('Uname:', 1)
                description = part1.replace('\r\n\r\n', '\r\n') + 'Uname:' \
                    + part2.split('\r\n\r\n', 1)[0]
            else:
                description = description.replace('\r\n\r\n', '\r\n')

        report.load(StringIO(description))

        when = bug.create_date
        if 'Date' not in report:
            report['Date'] = when

        if 'ProblemType' not in report:
            if 'apport-bug' in bug.keywords:
                report['ProblemType'] = 'Bug'
            elif 'apport-crash' in bug.keywords:
                report['ProblemType'] = 'Crash'
            elif 'apport-kernelcrash' in bug.keywords:
                report['ProblemType'] = 'KernelCrash'
            elif 'apport-package' in bug.keywords:
                report['ProblemType'] = 'Package'
            else:
                raise ValueError, 'cannot determine ProblemType from tags: '\
                        + str(bug.keywords)

        for attachment in bug.attachments:
            if attachment['filename'] in APPORT_FILES:
                key, ext = os.path.splitext(attachment['filename'])
                att = self.bugzilla.attachment(attachment['id'])
                if att is None:
                    raise RuntimeError, 'Error downloading attachment'
                if ext == '.txt':
                    report[key] = att['fd'].read()
                elif ext == '.gz':
                    #report[key] = gzip.GzipFile(fileobj=att['fd']).read()
                    report[key] = att['fd'].read()
                else:
                    raise RuntimeError, 'Unable to read %s file' % ext
        return report


    def update(self, bug_id, report, comment):
        '''Update the given report ID with the retraced results from the report
        (Stacktrace, ThreadStacktrace, StacktraceTop; also Disassembly if
        desired) and an optional comment.'''

        bug_etree = self.bugzilla.get(bug_id)
        bug = Bug(bug_id, bug_etree)

        comment += '\n\nStacktraceTop:' + report['StacktraceTop'].decode('utf-8',
            'replace').encode('utf-8')

        # FIXME: too much duplicated code. Itter over a list, perhaps?
        if report['Stacktrace']: # don't attach empty files
            tmp = tempfile.NamedTemporaryFile()
            s = report['Stacktrace'].decode('ascii', 'replace').encode('ascii', 'replace')
            tmp.write(s)
            tmp.flush()
            tmp.seek(0)
            self.bugzilla.attach(bug_id, 'Stacktrace.txt (retraced)',
                                 comment, tmp.name,
                                 filename_override='Stacktrace.txt')
            tmp.close()

        if report['ThreadStacktrace']:
            tmp = tempfile.NamedTemporaryFile()
            s = report['ThreadStacktrace'].decode('ascii', 'replace').encode('ascii', 'replace')
            tmp.write(s)
            tmp.flush()
            tmp.seek(0)
            self.bugzilla.attach(bug_id, 'ThreadStacktrace.txt (retraced)',
                                 '', tmp.name,
                                 filename_override='ThreadStacktrace.txt')
            tmp.close()

        if report.has_key('StacktraceSource') and report['StacktraceSource']:
            tmp = tempfile.NamedTemporaryFile()
            s = report['StacktraceSource'].decode('ascii', 'replace').encode('ascii', 'replace')
            tmp.write(s)
            tmp.flush()
            tmp.seek(0)
            self.bugzilla.attach(bug_id, 'StacktraceSource.txt (retraced)',
                                 '', tmp.name,
                                 filename_override='StacktraceSource.txt')
            tmp.close()

        # ensure it's assigned to the right package
        # TODO: implement-me
        #if report.has_key('SourcePackage') and \
        #        '+source' not in str(bug.bug_tasks[0].target):
        #    try:
        #        bug.bug_tasks[0].transitionToTarget(target=
        #                self.lp_distro.getSourcePackage(name=report['SourcePackage']))
        #    except HTTPError:
        #        pass # LP#342355 workaround

        # remove core dump if stack trace is usable
        if report.has_useful_stacktrace():
            for a in bug.attachments:
                if a['filename'] == 'CoreDump.gz':
                    # Setting the attachment as obsolete is the closest to
                    # deleting it we can get with bugzilla
                    params = {
                        'isobsolete': 1,
                    }
                    self.bugzilla.modify_attachment(a['id'], bug_id,**params)


    def get_distro_release(self, bug_id):
        '''Get 'DistroRelease: <release>' from the given report ID and return
        it.'''

        bug_etree = self.bugzilla.get(bug_id)
        bug = Bug(bug_id, bug_etree)
        m = re.search('DistroRelease: ([-a-zA-Z0-9.+/ ]+)', bug.description)
        if m:
            return m.group(1)
        raise ValueError, 'URL does not contain DistroRelease: field'


    def get_unretraced(self):
        '''Return an ID set of all crashes which have not been retraced yet and
        which happened on the current host architecture.'''

        bugs = self.bugzilla.search('', keywords=self.arch_tag)
        if bugs is None:
            return []
        return set([int(bug['bugid']) for bug in bugs])


    def get_dup_unchecked(self):
        '''Return an ID set of all crashes which have not been checked for
        being a duplicate.

        This is mainly useful for crashes of scripting languages such as
        Python, since they do not need to be retraced. It should not return
        bugs that are covered by get_unretraced().'''

        bugs = self.bugzilla.search('', keywords='need-duplicate-check')
        if bugs is None:
            return []
        return set([int(bug['bugid']) for bug in bugs])


    def get_unfixed(self):
        '''Return an ID set of all crashes which are not yet fixed.

        The list must not contain bugs which were rejected or duplicate.

        This function should make sure that the returned list is correct. If
        there are any errors with connecting to the crash database, it should
        raise an exception (preferably IOError).'''

        bugs = self.bugzilla.search('', keywords='apport-crash')
        if bugs is None:
            return []
        return set([int(bug['bugid']) for bug in bugs])


    def get_fixed_version(self, bug_id):
        '''Return the package version that fixes a given crash.

        Return None if the crash is not yet fixed, or an empty string if the
        crash is fixed, but it cannot be determined by which version. Return
        'invalid' if the crash report got invalidated, such as closed a
        duplicate or rejected.

        This function should make sure that the returned result is correct. If
        there are any errors with connecting to the crash database, it should
        raise an exception (preferably IOError).'''

        bug_etree = self.bugzilla.get(bug_id)
        bug = Bug(bug_id, bug_etree)
        invalid_resolutions = ['DUPLICATE', 'WONTFIX', 'INVALID']
        if bug.resolution == 'FIXED':
            #TODO: check if there's a way to know the solved version
            return ''
        elif bug.resolution in invalid_resolutions:
            return 'invalid'
        else:
            return None


    def duplicate_of(self, bug_id):
        '''Return master ID for a duplicate bug.

        If the bug is not a duplicate, return None.
        '''
        bug_etree = self.bugzilla.get(bug_id)
        bug = Bug(bug_id, bug_etree)
        if bug.dup_id == 0:
            return None
        else:
            return bug.dup_id


    def close_duplicate(self, bug_id, master):
        '''Mark a crash id as duplicate of given master ID.

        If master is None, id gets un-duplicated.
        '''
        if master is not None:
            self.bugzilla.modify(bug_id, duplicate=master,
                                 resolution='DUPLICATE')
        else:
            self.bugzilla.modify(bug_id, status='REOPENED')


    def mark_regression(self, bug_id, master):
        '''Mark a crash id as reintroducing an earlier crash which is
        already marked as fixed (having ID 'master').'''

        regression_keyword = 'regression-retracer'
        bug_etree = self.bugzilla.get(bug_id)
        bug = Bug(bug_id, bug_etree)
        kws = bug.keywords
        if regression_keyword not in kws:
            kws.append(regression_keyword)
            self.bugzilla.modify(bug_id, keywords=' '.join(kws))


    def mark_retraced(self, bug_id):
        '''Mark crash id as retraced.'''

        bug_etree = self.bugzilla.get(bug_id)
        bug = Bug(bug_id, bug_etree)
        kws = bug.keywords
        if self.arch_tag in kws:
            kws.remove(self.arch_tag)
            args = {
                'keywords': ' '.join(kws),
            }
            self.bugzilla.modify(bug_id, **args)


    def mark_retrace_failed(self, bug_id, invalid_msg=None):
        '''Mark crash id as 'failed to retrace'.

        If invalid_msg is given, the bug should be closed as invalid with given
        message, otherwise just marked as a failed retrace.

        This can be a no-op if you are not interested in this.'''

        if invalid_msg is not None:
            self.bugzilla.modify(bug_id, status='RESOLVED',
                                 resolution='INVALID', comment=invalid_msg)
        else:
            bug_etree = self.bugzilla.get(bug_id)
            bug = Bug(bug_id, bug_etree)
            kws = bug.keywords
            kws.append('apport-failed-retrace')
            new_kws = ' '.join(kws)
            self.bugzilla.modify(bug_id, keywords=new_kws)


    def _mark_dup_checked(self, bug_id, report):
        '''Mark crash id as checked for being a duplicate

        This is an internal method that should not be called from outside.'''

        bug_etree = self.bugzilla.get(bug_id)
        bug = Bug(bug_id, bug_etree)
        kws = bug.keywords
        try:
            kws.remove('need-duplicate-check')
            new_kws = ' '.join(kws)
            self.bugzilla.modify(bug_id, keywords=new_kws)
        except ValueError:
            # This happens when the bug doesn't have the
            # need-duplicate-check keyword
            pass


if __name__ == '__main__':
    import unittest, urllib2, cookielib

    crashdb = None
    segv_report = None
    python_report = None

    class _Tests(unittest.TestCase):
        # this assumes that a source package 'coreutils' exists and builds a
        # binary package 'coreutils'
        test_package = 'coreutils'
        test_srcpackage = 'coreutils'
        known_test_id = 12
        known_test_id2 = 13

        #
        # Generic tests, should work for all CrashDB implementations
        #

        def setUp(self):
            global crashdb
            if not crashdb:
                crashdb = self._get_instance()
            self.crashdb = crashdb

            # create a local reference report so that we can compare
            # DistroRelease, Architecture, etc.
            self.ref_report = apport.Report()
            self.ref_report.add_os_info()
            self.ref_report.add_user_info()

        def _file_segv_report(self):
            '''File a SEGV crash report.

            Return crash ID.
            '''
            r = apport.report._ApportReportTest._generate_sigsegv_report()
            r.add_package_info(self.test_package)
            r.add_os_info()
            r.add_gdb_info()
            r.add_user_info()
            self.assertEqual(r.standard_title(), 'crash crashed with SIGSEGV in f()')

            handle = self.crashdb.upload(r)
            self.assert_(handle)
            url = self.crashdb.get_comment_url(r, handle)
            self.assert_(url)
            return handle


        def test_1_report_segv(self):
            '''upload() and get_comment_url() for SEGV crash

            This needs to run first, since it sets segv_report.
            '''
            global segv_report
            id = self._file_segv_report()
            segv_report = id

        def test_1_report_python(self):
            '''upload() and get_comment_url() for Python crash

            This needs to run early, since it sets python_report.
            '''
            r = apport.Report('Crash')
            r['ExecutablePath'] = '/bin/foo'
            r['Traceback'] = '''Traceback (most recent call last):
  File "/bin/foo", line 67, in fuzz
    print weird
NameError: global name 'weird' is not defined'''
            r.add_package_info(self.test_package)
            r.add_os_info()
            r.add_user_info()
            self.assertEqual(r.standard_title(), 'foo crashed with NameError in fuzz()')

            handle = self.crashdb.upload(r)
            self.assert_(handle)
            url = self.crashdb.get_comment_url(r, handle)
            self.assert_(url)

            global python_report
            python_report = handle

        def test_2_download(self):
            '''download()'''

            r = self.crashdb.download(segv_report)
            self.assertEqual(r['ProblemType'], 'Crash')
            self.assertEqual(r['DistroRelease'], self.ref_report['DistroRelease'])
            self.assertEqual(r['Architecture'], self.ref_report['Architecture'])
            self.assertEqual(r['Uname'], self.ref_report['Uname'])
            self.assertEqual(r.get('NonfreeKernelModules'),
                self.ref_report.get('NonfreeKernelModules'))
            self.assertEqual(r.get('UserGroups'), self.ref_report.get('UserGroups'))

            self.assertEqual(r['Signal'], '11')
            self.assert_(r['ExecutablePath'].endswith('/crash'))
            self.assertEqual(r['SourcePackage'], self.test_srcpackage)
            self.assert_(r['Package'].startswith(self.test_package + ' '))
            self.assert_('f (x=42)' in r['Stacktrace'])
            self.assert_('f (x=42)' in r['StacktraceTop'])
            self.assert_('f (x=42)' in r['ThreadStacktrace'])
            self.assert_(len(r['CoreDump']) > 1000)
            self.assert_('Dependencies' in r)
            self.assert_('Disassembly' in r)
            self.assert_('Registers' in r)

        def test_3_update(self):
            '''update()'''

            r = self.crashdb.download(segv_report)
            self.assert_('CoreDump' in r)
            self.assert_('Dependencies' in r)
            self.assert_('Disassembly' in r)
            self.assert_('Registers' in r)
            self.assert_('Stacktrace' in r)
            self.assert_('ThreadStacktrace' in r)

            # updating with an useless stack trace retains core dump
            r['StacktraceTop'] = '?? ()'
            r['Stacktrace'] = 'long\ntrace'
            r['ThreadStacktrace'] = 'thread\neven longer\ntrace'
            self.crashdb.update(segv_report, r, 'I can has a better retrace?')
            r = self.crashdb.download(segv_report)
            self.assert_('CoreDump' in r)
            self.assert_('Dependencies' in r)
            self.assert_('Disassembly' in r)
            self.assert_('Registers' in r)
            self.assert_('Stacktrace' in r) # TODO: ascertain that it's the updated one
            self.assert_('ThreadStacktrace' in r)

            # updating with an useful stack trace removes core dump
            r['StacktraceTop'] = 'read () from /lib/libc.6.so\nfoo (i=1) from /usr/lib/libfoo.so'
            r['Stacktrace'] = 'long\ntrace'
            r['ThreadStacktrace'] = 'thread\neven longer\ntrace'
            self.crashdb.update(segv_report, r, 'good retrace!')
            r = self.crashdb.download(segv_report)
            self.failIf('CoreDump' in r)
            self.assert_('Dependencies' in r)
            self.assert_('Disassembly' in r)
            self.assert_('Registers' in r)
            self.assert_('Stacktrace' in r)
            self.assert_('ThreadStacktrace' in r)

            # test various situations which caused crashes
            r['Stacktrace'] = '' # empty file
            r['ThreadStacktrace'] = '"]\xb6"\n' # not interpretable as UTF-8, LP #353805
            self.crashdb.update(segv_report, r, 'tests')

        def test_get_distro_release(self):
            '''get_distro_release()'''

            self.assertEqual(self.crashdb.get_distro_release(segv_report),
                    self.ref_report['DistroRelease'])

        def test_duplicates(self):
            '''duplicate handling'''

            # initially we have no dups
            self.assertEqual(self.crashdb.duplicate_of(segv_report), None)
            self.assertEqual(self.crashdb.get_fixed_version(segv_report), None)

            # dupe our segv_report and check that it worked; then undupe it
            self.crashdb.close_duplicate(segv_report, self.known_test_id)
            self.assertEqual(self.crashdb.duplicate_of(segv_report), self.known_test_id)

            # this should be a no-op
            self.crashdb.close_duplicate(segv_report, self.known_test_id)
            self.assertEqual(self.crashdb.duplicate_of(segv_report), self.known_test_id)

            self.assertEqual(self.crashdb.get_fixed_version(segv_report), 'invalid')
            self.crashdb.close_duplicate(segv_report, None)
            self.assertEqual(self.crashdb.duplicate_of(segv_report), None)
            self.assertEqual(self.crashdb.get_fixed_version(segv_report), None)

            # this should have removed attachments; note that Stacktrace is
            # short, and thus inline
            #XXX: this won't happen in Bugzilla
            #r = self.crashdb.download(segv_report)
            #self.failIf('CoreDump' in r)
            #self.failIf('Dependencies' in r)
            #self.failIf('Disassembly' in r)
            #self.failIf('Registers' in r)

            # now try duplicating to a duplicate bug; this should automatically
            # transition to the master bug
            #XXX: this won't happen also
            #TODO: check whether to implement this on close_duplicate() or not
            #self.crashdb.close_duplicate(self.known_test_id,
            #        self.known_test_id2)
            #self.crashdb.close_duplicate(segv_report, self.known_test_id)
            #self.assertEqual(self.crashdb.duplicate_of(segv_report),
            #        self.known_test_id2)

            self.crashdb.close_duplicate(self.known_test_id, None)
            self.crashdb.close_duplicate(self.known_test_id2, None)
            self.crashdb.close_duplicate(segv_report, None)

            # this should be a no-op
            self.crashdb.close_duplicate(self.known_test_id, None)
            self.assertEqual(self.crashdb.duplicate_of(self.known_test_id), None)

            self.crashdb.mark_regression(segv_report, self.known_test_id)
            self._verify_marked_regression(segv_report)

        def test_marking_segv(self):
            '''processing status markings for signal crashes'''

            # mark_retraced()
            unretraced_before = self.crashdb.get_unretraced()
            self.assert_(segv_report in unretraced_before)
            self.failIf(python_report in unretraced_before)
            self.crashdb.mark_retraced(segv_report)
            unretraced_after = self.crashdb.get_unretraced()
            self.failIf(segv_report in unretraced_after)
            self.assertEqual(unretraced_before,
                    unretraced_after.union(set([segv_report])))
            self.assertEqual(self.crashdb.get_fixed_version(segv_report), None)

            # mark_retrace_failed()
            self._mark_needs_retrace(segv_report)
            self.crashdb.mark_retraced(segv_report)
            self.crashdb.mark_retrace_failed(segv_report)
            unretraced_after = self.crashdb.get_unretraced()
            self.failIf(segv_report in unretraced_after)
            self.assertEqual(unretraced_before,
                    unretraced_after.union(set([segv_report])))
            self.assertEqual(self.crashdb.get_fixed_version(segv_report), None)

            # mark_retrace_failed() of invalid bug
            self._mark_needs_retrace(segv_report)
            self.crashdb.mark_retraced(segv_report)
            self.crashdb.mark_retrace_failed(segv_report, "I don't like you")
            unretraced_after = self.crashdb.get_unretraced()
            self.failIf(segv_report in unretraced_after)
            self.assertEqual(unretraced_before,
                    unretraced_after.union(set([segv_report])))
            self.assertEqual(self.crashdb.get_fixed_version(segv_report),
                    'invalid')

        def test_marking_python(self):
            '''processing status markings for interpreter crashes'''

            unchecked_before = self.crashdb.get_dup_unchecked()
            self.assert_(python_report in unchecked_before)
            self.failIf(segv_report in unchecked_before)
            self.crashdb._mark_dup_checked(python_report, self.ref_report)
            unchecked_after = self.crashdb.get_dup_unchecked()
            self.failIf(python_report in unchecked_after)
            self.assertEqual(unchecked_before,
                    unchecked_after.union(set([python_report])))
            self.assertEqual(self.crashdb.get_fixed_version(python_report),
                    None)

        def test_update_invalid(self):
            '''updating a invalid crash

            This simulates a race condition where a crash being processed gets
            invalidated by marking it as a duplicate.
            '''
            id = self._file_segv_report()

            r = self.crashdb.download(id)

            self.crashdb.close_duplicate(id, segv_report)

            # updating with an useful stack trace removes core dump
            r['StacktraceTop'] = 'read () from /lib/libc.6.so\nfoo (i=1) from /usr/lib/libfoo.so'
            r['Stacktrace'] = 'long\ntrace'
            r['ThreadStacktrace'] = 'thread\neven longer\ntrace'
            self.crashdb.update(id, r, 'good retrace!')

            r = self.crashdb.download(id)
            self.failIf('CoreDump' in r)

        def test_get_fixed_version(self):
            '''get_fixed_version() for fixed bugs

            Other cases are already checked in test_marking_segv() (invalid
            bugs) and test_duplicates (duplicate bugs) for efficiency.
            '''
            self._mark_report_fixed(segv_report)
            fixed_ver = self.crashdb.get_fixed_version(segv_report)
            self.assertNotEqual(fixed_ver, None)
            #FIXME: not yet implemented
            #self.assert_(fixed_ver[0].isdigit())
            self._mark_report_new(segv_report)
            self.assertEqual(self.crashdb.get_fixed_version(segv_report), None)

        # Bugzilla implementation
        @classmethod
        def _get_instance(klass):
            url = 'http://localhost/bugzilla/'
            defaultopts = {
                'product': 'FoodReplicator',
                'component': 'SpiceDispenser',
                'version': '1.0',
                #'url': '',
                #'assigned_to': '',
                #'cc': '',
                #'keywords': '',
                #'version': '1.0',
                #'dependson': '',
                #'blocked': '',
                #'priority': 'P2',
                #'severity': 'minor',
            }

            return CrashDatabase(None,None,{'baseurl': url,
                                            'default_options': defaultopts})

        def _mark_needs_retrace(self, id):
            '''Mark a report ID as needing retrace.'''

            bug = self.crashdb.bugzilla.get(id)
            b = Bug(id, bug)
            kws = b.keywords
            if self.crashdb.arch_tag not in kws:
                kws.append(self.crashdb.arch_tag)
                self.crashdb.bugzilla.modify(id, keywords=' '.join(kws))

        def _mark_needs_dupcheck(self, id):
            '''Mark a report ID as needing duplicate check.'''

            bug = self.crashdb.bugzilla.get(id)
            b = Bug(id, bug)
            kws = b.keywords
            if 'need-duplicate-check' not in kws:
                kws.append('need-duplicate-check')
                self.crashdb.bugzilla.modify(id, keywords=' '.join(kws))

        def _mark_report_fixed(self, id):
            '''Close a report ID as "fixed".'''

            self.crashdb.bugzilla.modify(id, status='RESOLVED',
                                         resolution='FIXED')

        def _mark_report_new(self, id):
            '''Reopen a report ID as "new".'''

            self.crashdb.bugzilla.modify(id, status='REOPENED')

        def _verify_marked_regression(self, id):
            '''Verify that report ID is marked as regression.'''

            bug = self.crashdb.bugzilla.get(id)
            b = Bug(id, bug)
            self.assert_('regression-retracer' in b.keywords)

    unittest.main()
