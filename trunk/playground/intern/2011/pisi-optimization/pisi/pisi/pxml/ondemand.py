# -*- coding: utf-8 -*-

class OnDemandNode(object):
    def __init__(self, decode, node, where):
        self.decode_function = decode
        self.node = node
        self.error_function = None
        self.where = where

    def decode(self):
        # print "decoding", self.where # debuginfo
        errs = []

        r = self.decode_function(self.node, errs, self.where, True)

        if self.error_function:
            # print "checking", self.where # debuginfo
            errs.extend(self.error_function(r, self.where))

        if errs:
            raise Error(*errs)

        return r

class OnDemandList(list):

    def __init__(self):
        super(OnDemandList, self).__init__()
        self.undecoded_count = 0
        self.errors_item_function = None

    def __getitem__(self, y):
        item = super(OnDemandList, self).__getitem__(y)

        if isinstance(item, OnDemandNode):
            item.error_function = self.errors_item_function
            item = item.decode()
            super(OnDemandList, self).__setitem__(y, item)
            self.undecoded_count -= 1

        return item

    def decodeall_run_f(self, y, f):
        print "decodeall: ", f
        self.decodeAll()
        if isinstance(y, OnDemandList):
            y.decodeAll()

        return super(OnDemandList, self).__getattribute__(f)(y)

    def append(self, y):
        if isinstance(y, OnDemandNode):
            self.undecoded_count += 1

        return super(OnDemandList, self).append(y)

    def count(self, y):
        self.decodeAll()
        return super(OnDemandList, self).count(y)

    def extend(self, i):
        return decodeall_run_f(i, 'extend')

    def index(self, value, start = None, stop = None):
        # FIXME : ???
        print "index", value, start, stop
        self.decodeAll()
        return super(OnDemandList, self).index(value, start, stop)

    # def insert(self, index, o):

    def pop(self, index = None):
        a = super(OnDemandList, self).pop(index)
        if isinstance(a, OnDemandNode):
            a = a.decode()
        return a

    def remove(self, value):
        self.decodeAll()
        return super(OnDemandList, self).remove(value)

    def sort(self, cmp = None, key=None, reverse=False):
        self.decodeAll()
        return super(OnDemandList, self).sort(cmp, key, reverse)

    def __add__(self, y):
        self.decodeall_run_f(y, '__add__')

    def __contains__(self, y):
        if self.undecoded_count > 0:
            self.decodeAll()
        return super(OnDemandList, self).__contains__(y)

    def __delitem__(self, y):
        if not self.isDecoded(y):
            self.undecoded_count -= 1
        return super(OnDemandList, self).__delitem__(y)

    def __delslice__(self, i, j):
        # TODO: test yap, bu fonksiyon __delitem__ i kullanıyor olabilir.
        for x in range(i, j):
            if not self.isDecoded(x):
                self.undecoded_count -= 1

        return super(OnDemandList, self).__delslice__(i, j)

    def __eq__(self, y):
        if isinstance(y, list):
            return self.decodeall_run_f(y, '__eq__')

        return False

    def __ge__(self, y):
        return self.decodeall_run_f(y, '__ge__')

    def __getslice__(self, i, j):
        # TODO: test yap, ...
        # Decode slice
        for x in range(i, j):
            self.__getitem__(x)
        return super(OnDemandList, self).__getslice__(i, j)

    def __gt__(self, y):
        return self.decodeall_run_f(y, '__gt__')

    def __iadd__(self, y):
        return self.decodeall_run_f(y, '__iadd__')

    def __imul__(self, y):
        return self.decodeall_run_f(y, '__imul__')

    def __iter__(self):
        for i in xrange(len(self)):
            yield self.__getitem__(i)

    def __le__(self, y):
        return self.decodeall_run_f(y, '__le__')

    def __lt__(self, y):
        return self.decodeall_run_f(y, '__lt__')

    def __mul__(self, y):
        return self.decodeall_run_f(y, '__mul__')

    def __ne__(self, y):
        if isinstance(y, list):
            return self.decodeall_run_f(y, '__ne__')

        return True

    def __reduce__(self):
        # print "reduce"
        self.decodeAll()
        if hasattr(self, 'errors_item_function'):
            delattr(self, 'errors_item_function')
        return super(OnDemandList, self).__reduce__()

    def __reduce_ex__(self, protocol):
        # print "reduce_ex"
        self.decodeAll()
        if hasattr(self, 'errors_item_function'):
            delattr(self, 'errors_item_function')
        return super(OnDemandList, self).__reduce_ex__(protocol)

    # __repr__(self)

    def __reversed__(self):
        for i in xrange(len(self)-1, -1, -1):
            yield self.__getitem__(i)

    def __rmul__(self, y):
        return self.decodeall_run_f(y, '__rmul')

    def __setitem__(self, i, y):
        if not self.isDecoded(i):
            self.undecoded_count -= 1

        if isinstance(y, OnDemandNode):
            self.undecoded_count += 1

        return super(OnDemandList, self).__setitem__(i, y)

    def isDecoded(self, y):
        return not isinstance(y, OnDemandNode)

    def safeIter(self):
        class iterator(object):
            def __init__(self, obj):
                self.obj = obj
                self.index = -1

            def __iter__(self):
                return self

            def next(self):
                self.index+=1
                if self.index >= len(self.obj):
                    raise StopIteration
                # print len(self.obj), self.index #

                while not self.obj.isDecoded(self.index):
                    self.index += 1
                    if self.index >= len(self.obj):
                        raise StopIteration

                return self.obj[self.index]

        return iterator(self)

    def decodeAll(self):
        if self.undecoded_count > 0:
            for x in xrange(len(self)):
                self.__getitem__(x)
