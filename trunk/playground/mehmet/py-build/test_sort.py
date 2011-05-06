#!/usr/bin/python
# -*- coding: utf-8 -*-

class TestSort:
    def setup_method(self, method):
        self.alist = [5, 2, 3, 1, 4]
        print "alist in setup_method:", self.alist

    def test_ascending_sort(self):
        print "alist in test_ascending_sort, before sort:", self.alist
        self.alist.sort()
        print "alist in test_ascending_sort, after sort:", self.alist
        assert self.alist == [1, 2, 3, 4, 5]

    def test_custom_sort(self):
        def int_compare(x, y):
            x = int(x)
            y = int(y)
            return x - y
        self.alist.sort(int_compare)
        assert self.alist == [1, 2, 3, 4, 5]

        b = ["1", "10", "2", "20", "100"]
        b.sort()
        assert b == ['1', '10', '100', '2', '20']
        b.sort(int_compare)
        assert b == ['1', '2', '10', '20', '100']

    def test_sort_reverse(self):
        self.alist.sort()
        self.alist.reverse()
        assert self.alist == [5, 4, 3, 2, 1]

    def test_sort_exception(self):
        import py.test
        py.test.raises(NameError, "self.alist.sort(int_compare)")
        py.test.raises(ValueError, self.alist.remove, 6)
