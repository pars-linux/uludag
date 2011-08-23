# -*- coding: utf-8 -*

'''

test0 -> correct xml

test1 -> pisi.source.name not exist
test2 -> pisi.source.packager not exist
test3 -> pisi.source.packager.name not exist
test4 -> history not exist

'''

import pisi

tests = [
    (str, 'source'),
    (None, 'source.name'),
    (str, 'source.packager'),
    (None, 'source.packager.name'),
    (str, 'package')
    ]

def autoxml_test(xml_file, use_ondemand):
    values = {}
    errors = set()
    error_types = {}

    for i in xrange(len(tests)):
        try:
            a = pisi.metadata.MetaData()
            a.read(xml_file, use_ondemand=use_ondemand)
        except Exception, e:
            for arg in e.args:
                if arg.find(xml_file) < 0:
                    errors.add(arg)
                    error_types[-1] = e.args
            continue

        test_function, test_attr = tests[i]

        try:
            y = a
            for s in test_attr.split('.'):
                if len(s) > 0:
                    y = getattr(y, s)

            if test_function:
                values[i] = test_function(y)
            else:
                values[i] = y

        except Exception, e:
            errors = errors.union(e.args)
            error_types[i] = e.args

    return values, errors, error_types

def compare_tests(xml_file):
    '''
    compare tests with use_ondemand and without use_ondemand
    '''

    a_values, a_errors, a_error_types = autoxml_test(xml_file, False)
    b_values, b_errors, b_error_types = autoxml_test(xml_file, True)

    v = a_values==b_values
    e = a_errors==b_errors
    error_count = len(a_errors) + len(b_errors)
    if error_count == 0:
        print "a_values == b_values: %s" % (a_values==b_values)
    print "a_errors == b_errors: %s" % (a_errors==b_errors)
    print "len(a_errors):", len(a_errors)
    print "len(b_errors):", len(b_errors)

    if not e:
        print "\na diff b: "
        print a_errors.difference(b_errors)
        print "\nb diff a: "
        print b_errors.difference(a_errors)

        print "\na: "
        print a_error_types
        print "\nb: "
        print b_error_types
    elif not v and error_count == 0:
        print a_values
        print "\n"
        print b_values

        
def compare_full(xml_file):
    '''
    compare all attributes with use_ondemand and without use_ondemand
    '''

    # TODO: ---
    pass

test_files = []
for i in range(5):
    test_files.append('test_xml/test%s.xml' % i)
    
if __name__ == '__main__':
    for test_file in test_files:
        print test_file
        compare_tests(test_file)
        print ""
