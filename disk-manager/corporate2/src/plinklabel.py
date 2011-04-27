#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
.. module:: plinklabel

.. moduleauthor:: Mehmet Özdemir <mehmet@pardus.org.tr>

.. Exported Classes:

    * :PLinkLabel: A simple QLabel class with text properties like a link, mouse over properties etc.

"""



#qlabel
from qt import *
#kglobal settings
from kdecore import *

class PLinkLabel(QLabel):
    """We use this as a public class example class.

    You never call this class before calling :func:`public_fn_with_sphinxy_docstring`.

    .. note::

       An example of intersphinx is this: you **cannot** use :mod:`pickle` on this class.

    """


    def __init__(self, parent, name=0, flags=0):
        QLabel.__init__(self, parent, name, flags)
        self.color = KGlobalSettings.linkColor()
        self.setPaletteForegroundColor(self.color)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.method = None
        # bold, italic etc. options will be added.
        # method may take arguments

    def mousePressEvent(self, event):
        """This function does something.

        Args:
           name (str):  The name to use.

        Kwargs:
           state (bool): Current state to be in.

        Returns:
           int.  The return code::

              0 -- Success!
              1 -- No good.
              2 -- Try again.

        Raises:
           AttributeError, KeyError

        A really great idea.  A way you might use me is

        >>> print public_fn_with_googley_docstring(name='foo', state=None)
        0

        BTW, this always returns 0.  **NEVER** use with :class:`MyPublicClass`.

        """
        if self.method:
            self.method()

    def setLinkText(self, text):
        """Sets a link label's text property which is inherited from QLabel.

        :param self: Self object
        :type self: PLinkLabel
        :param text: Text value for updating the label's text property.
        :type text: string

        """
        #:rtype: bool
        #:return: If set operation is succesful return `True` else return `False`
        self.setText(text)

