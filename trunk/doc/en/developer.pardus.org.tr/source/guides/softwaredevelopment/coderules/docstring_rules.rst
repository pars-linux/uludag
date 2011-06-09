.. _docstring-rules:

**Last Modified Date:** |today|

:Author: Mehmet Özdemir

:Version: 0.1


Docstring Rules
===============


.. note::

   This document assumes Pardus developers use Sphinx to create apidoc. While you are writing docstring for your code you ARE EXPECTED TO OBEY writing restructured text conventions.


.. image:: whole_view.png

You can see the cheatsheet: http://developer.pardus.org.tr/guides/softwaredevelopment/coderules/PardusApiDocStandardsCheatSheet.pdf


Below are the code documentation rules in generally we want you to observe:


Function & Method Documentation
-------------------------------

#. One line summary (Synopsis)
    * Synopsis will be put after the first """
    * However, other lines will be the same align
    * Synopsis is a brief description of method/function
    * This is required
#. An extended description
    * Extended description is an optional field
    * If extra information is needed about function/method, we write extended description
        - For example, assume that there is a function takes a parameter whose name is hash. In extended description we may describe which hashes are supported or expected etc.
    * There must be a blank line after synopsis
#. Arguments
    * Argument names and argument types will be listed
    * A simple description would be useful, helpful
    * These properties will be written for every parameter
    * This is required
    * Format::

         :param arg: `description`
         :type arg: `type of the above argument`
    * There must be a blank line after extended description
#. Return value
    * Return value and type should be written
    * A description would be good
    * This is required if there is return value
    * Format::

         :returns: `description`
         :rtype: `type`
    * There must NOT be a blank line after arguments
#. Exceptions
    * Exceptions should be listed
    * Description of the exception should be written
    * Format::

         :raisises `Type of the Exception`: `description`
    * There must NOT be a blank line after return value
#. End sof comment and blank line
    * There must be a blank line after exceptions
    * After the blank line triple " character comes and comment ends
    * After the end of comment symbol there nust be a blank line

**If needed:** (not recommended)

  * Example: A usage sample
  * License: License of the method
  * Algorithm: You can add implementation of the algorithm
  * Notes: You can write additional notes
  * Bugs: If there is any known bug this can be written
  * Authors: Authors of the function/method
  * See Also: Reader is warned to see related functions/methods
  * Comments: Writer comments
  * Warnings: Usage warnings
  * Todo: A todo list
  * Tags: Tags can be written. Like deprecated.


.. note::

   Keep in mind that the above information aims to the users of our function/method. We embed comments and other information in our function's/method's code and this information is for function/method developers. Comments in this section generally starts with # character and a whitespace follows it. Then information is written.


Function & Method Documentation Sample Code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  def addItem(self, id_, name="", description="", mounted=False):
    """This function is used for to add new disk unit items to the list.

    Disk unit items are the items that are plugged to system. They are added to list with related unit information.

    :param id_: Identification of the disk unit
    :type id_: string
    :param name: Name for this disk unit
    :type name: string
    :param description: A description about unit's features. `Like size, mount state etc.`
    :type description: string
    :param mounted: Mount state of the unit. If it is mounted this value must be True, otherwise False
    :type mounted: Boolean
    :returns: **True** if add operation is succesful, otherwise returns **False**
    :rtype: Boolean
    :raises UnitNotExistException: If id not exists raise UnitNotExistException (Salladim)

    """

    if mounted:
      if ctx.Pds.session == ctx.pds.Kde4:
        icon = KIcon("drive-harddisk", None, ["emblem-mounted"])
      else:
        icon = QtGui.QIcon(KIconLoader.loadOverlayed('drive-harddisk', ["emblem-mounted"], 32))
    else:
      icon = KIcon("drive-harddisk")

    type_ = "disk"

    # Build widget and widget item
    widget = self.makeItemWidget(id_, name, description, type_, icon, mounted)
    widgetItem = ItemListWidgetItem(self.listItems, widget)

    # Delete is unnecessary
    widget.hideDelete()

    # Add to list
    self.listItems.setItemWidget(widgetItem, widget)


.. image:: method_sample.png



Module Documentation
--------------------

#. Synopsis
    * Brief description of the module
    * This line should start below the """
#. Module author
    * Format::

         .._  moduleauthor:: pars <admins@pardus.org.tr>
    * There must be a blank line after synopsis
#. End of module information
    * Finish module documentation with triple " and put a blank line after that


Module Documentation Sample Code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  """
  This module provides a widget that lists the disk items with a fancy view...

  .. moduleauthor:: pars <admins@pardus.org.tr>

  """

.. warning::

   Unknown directive type "module".
   Unknown directive type "moduleauthor".
   http://packages.python.org/an_example_pypi_project/sphinx.html#full-code-example


Variable & Attribute Documentation
----------------------------------

#. Description
    * What is that attribute, why you defined that?


Variable & Attribute Documentation Sample Code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  """ Holds the current index value for a ListElement """
  index = 0


Class Documentation
-------------------

#. One line summary (Synopsis)
    * Synopsis is a brief description of class. What does it represents?
    * Synopsis will be put after the first """
    * However, other lines will be the same align
#. An extended description
    * If class needs an extended description this can be written but this is not an obligation
    * There must be a blank line after synopsis
#. Main Jobs
    * What that class do mainly; which main operations are supplied?
    * If you believe giving main operation names useful, write them here. For example, a class may have lots of function but developer may wanna see main public functions and their tasks briefly. (This is not an obligation.)
    * There must be a blank line after extended description (or synopsis if there is no extended description)
    * Format::

         **Job Definition**: `Job description`


Class Documentation Sample Code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    class EntryView(QScrollView):
        """Holds the rule entries and shows them like a list view

        This class is a simple listview implementation. It behaves like a 
        listview when entries are added, deleted or selected. The main
        difference from a listview is this class stores custom widget
        elements instead of listviewitems.

        ** Item Addition**: add a new item to view
        ** Item Deletion**: delete an existing item from view
        ** Handling Item Events**: handle item events

        """

.. note::

  * One line summary (synopsis) property was removed because a good function name should already do this job (Gökmen Göksel)
  * Examples are removed because we dont think to use doctest and importng examples to apidoc from external sources make our code more readable (Bahadır Kandemir)
    - We will use unit testing so doctest examples make our code dirty. However, code samples will be in apidoc because it is so important.
  * We should avoid unnecessary descriptions when writing explanations in code. Sphinx supplies us to extend our documentation, it combines docstring and external documents

