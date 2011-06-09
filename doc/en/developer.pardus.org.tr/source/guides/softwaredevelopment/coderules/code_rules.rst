.. _language-rules:

**Last Modified Date:** |today|

:Author: Bahadır Kandemir, Çağlar Kilimci

:Version: 0.1


Code Rules
==========

This document provides a set of coding rules for Pardus Development, its based on the Google's Python Coding Standards Document.
You can see the cheatsheet: http://developer.pardus.org.tr/guides/softwaredevelopment/coderules/PythonStyleCheatSheet.pdf

Python Language Rules
~~~~~~~~~~~~~~~~~~~~~

pychecker
---------

Run pychecker over your code.

**Definition:** PyChecker is a tool for finding bugs in Python source code. It finds problems that are typically caught by a compiler for less dynamic languages like C and C++. It is similar to lint. Because of the dynamic nature of Python, some warnings may be incorrect; however, spurious warnings should be fairly infrequent.

**Pros:** Catches easy-to-miss errors like typos, use-vars-before-assignment, etc.

**Cons:** pychecker isn't perfect. To take advantage of it, we'll need to sometimes: a) Write around it b) Suppress its warnings c) Improve it or d) Ignore it.

**Decision:**

Make sure you run pychecker on your code.

For information on how to run pychecker, see the `pychecker homepage <http://http://pychecker.sourceforge.net/>`_

To suppress warnings, you can set a module-level variable named "__pychecker__" to suppress appropriate warnings. For example::
  
    __pychecker__ = 'no-callinit no-classattr'

Suppressing in this way has the advantage that we can easily search for suppressions and revisit them.

You can get a list of pychecker warnings by doing pychecker --help.

Unused argument warnings can be suppressed by using "_" as the identifier for the unused argument or prefixing the argument name with "unused\_". In situations where changing the argument names is infeasible, you can mention them at the beginning of the function. For example::
  
    def foo(a, unused_b, unused_c, d=None, e=None):
        (d, e) = (d, e)  # Silence pychecker
        return a

Ideally, pychecker would be extended to ensure that such "unused declarations" were true.


Imports
-------

Use imports for packages and modules only.

**Definition:** Reusability mechanism for sharing code from one module to another.

**Pros:** The namespace management convention is simple. The source of each identifier is indicated in a consistent way; x.Obj says that object Obj is defined in module x.

**Cons:** Module names can still collide. Some module names are inconveniently long.

**Decision:**

- Use import x for importing packages and modules. 
- Use from x import y where x is the package prefix and y is the module name with no prefix. 
- Use from x import y as z if two modules named z are to be imported or if y is an inconveniently long name.

For example the module sound.effects.echo may be imported as follows::
  
    from sound.effects import echo
    ...
    echo.EchoFilter(input, output, delay=0.7, atten=4)

Do not use relative names in imports. Even if the module is in the same package, use the full package name. This helps prevent unintentionally importing a package twice.


Packages
--------

Import each module using the full pathname location of the module.

**Pros:** Avoids conflicts in module names. Makes it easier to find modules.

**Cons:** Makes it harder to deploy code because you have to replicate the package hierarchy.

**Decision:** All new code should import each module by its full package name.

Imports should be as follows::
  
    # Reference in code with complete name.
    import sound.effects.echo
    
    # Reference in code with just module name (preferred).
    from sound.effects import echo


Exceptions
----------

Exceptions are allowed but must be used carefully.

**Definition:** Exceptions are a means of breaking out of the normal flow of control of a code block to handle errors or other exceptional conditions.

**Pros:** The control flow of normal operation code is not cluttered by error-handling code. It also allows the control flow to skip multiple frames when a certain condition occurs, e.g., returning from N nested functions in one step instead of having to carry-through error codes.

**Cons:** May cause the control flow to be confusing. Easy to miss error cases when making library calls.

**Decision:**

Exceptions must follow certain conditions:

- Raise exceptions like this: raise MyException("Error message") or raise MyException. Do not use the two-argument form (raise MyException, "Error message") or deprecated string-based exceptions (raise "Error message").

- Modules or packages should define their own domain-specific base exception class, which should inherit from the built-in Exception class. The base exception for a module should be called Error::
    
    class Error(Exception):
        pass

- Never use catch-all except: statements, or catch Exception or StandardError, unless you are re-raising the exception or in the outermost block in your thread (and printing an error message). Python is very tolerant in this regard and **except:** will really catch everything including Python syntax errors. It is easy to hide real bugs using **except:**.

- Minimize the amount of code in a try/except block. The larger the body of the try, the more likely that an exception will be raised by a line of code that you didn't expect to raise an exception. In those cases, the try/except block hides a real error.

- Use the finally clause to execute code whether or not an exception is raised in the try block. This is often useful for cleanup, i.e., closing a file.


Global variables
----------------

Avoid global variables.

**Definition:** Variables that are declared at the module level.

**Pros:** Occasionally useful.

**Cons:** Has the potential to change module behavior during the import, because assignments to module-level variables are done when the module is imported.

**Decision:**

Avoid global variables in favor of class variables. Some exceptions are:

- Default options for scripts.
- Module-level constants. For example: PI = 3.14159. Constants should be named using all caps with underscores; see Naming below.
- It is sometimes useful for globals to cache values needed or returned by functions.
- If needed, globals should be made internal to the module and accessed through public module level functions; see Naming below.


Nested/Local/Inner Classes and Functions
----------------------------------------

Nested/local/inner classes and functions are fine.

**Definition:** A class can be defined inside of a method, function, or class. A function can be defined inside a method or function. Nested functions have read-only access to variables defined in enclosing scopes.

**Pros:** Allows definition of utility classes and functions that are only used inside of a very limited scope. Very `ADT <http://http://en.wikipedia.org/wiki/Abstract_data_type>`_-y.

**Cons:** Instances of nested or local classes cannot be pickled.

**Decision:** They are fine.


List Comprehensions
-------------------

Okay to use for simple cases.

**Definition:** List comprehensions and generator expressions provide a concise and efficient way to create lists and iterators without resorting to the use of map(), filter(), or lambda.

**Pros:** Simple list comprehensions can be clearer and simpler than other list creation techniques. Generator expressions can be very efficient, since they avoid the creation of a list entirely.

**Cons:** Complicated list comprehensions or generator expressions can be hard to read.

**Decision:** Okay to use for simple cases. Each portion must fit on one line: mapping expression, for clause, filter expression. Multiple for clauses or filter expressions are not permitted. Use loops instead when things get more complicated.

No::
  
    result = [(x, y) for x in range(10) for y in range(5) if x * y > 10]
    
    return ((x, y, z)
            for x in xrange(5)
            for y in xrange(5)
            if x != y
            for z in xrange(5)
            if y != z)

Yes::
  
    result = []
    for x in range(10):
        for y in range(5):
            if x * y > 10:
                result.append((x, y))
  
    for x in xrange(5):
        for y in xrange(5):
            if x != y:
                for z in xrange(5):
                    if y != z:
                        yield (x, y, z)
  
    return ((x, complicated_transform(x))
            for x in long_generator_function(parameter)
            if x is not None)
  
    squares = [x * x for x in range(10)]
  
    eat(jelly_bean for jelly_bean in jelly_beans
        if jelly_bean.color == 'black')


Default Iterators and Operators
-------------------------------

Use default iterators and operators for types that support them, like lists, dictionaries, and files.

**Definition:**

Container types, like dictionaries and lists, define default iterators and membership test operators ("in" and "not in").

**Pros:** The default iterators and operators are simple and efficient. They express the operation directly, without extra method calls. A function that uses default operators is generic. It can be used with any type that supports the operation.

**Cons:** You can't tell the type of objects by reading the method names (e.g. has_key() means a dictionary). This is also an advantage.

**Decision:** Use default iterators and operators for types that support them, like lists, dictionaries, and files. The built-in types define iterator methods, too. Prefer these methods to methods that return lists, except that you should not mutate a container while iterating over it.

Yes::
  
    for key in adict: ...
    if key not in adict: ...
    if obj in alist: ...
    for line in afile: ...
    for k, v in dict.iteritems(): ...

No::
  
     for key in adict.keys(): ...
     if not adict.has_key(key): ...
     for line in afile.readlines(): ...


Generators
----------

Use generators as needed.

**Definition:** A generator function returns an iterator that yields a value each time it executes a yield statement. After it yields a value, the runtime state of the generator function is suspended until the next value is needed.

**Pros:** Simpler code, because the state of local variables and control flow are preserved for each call. A generator uses less memory than a function that creates an entire list of values at once.

**Cons:** None.

**Decision:** Fine. Use "Yields:" rather than "Returns:" in the doc string for generator functions.


Lambda Functions
----------------

Okay for one-liners.

**Definition:** Lambdas define anonymous functions in an expression, as opposed to a statement. They are often used to define callbacks or operators for higher-order functions like map() and filter().

**Pros:** Convenient.

**Cons:** Harder to read and debug than local functions. The lack of names means stack traces are more difficult to understand. Expressiveness is limited because the function may only contain an expression.

**Decision:** Okay to use them for one-liners. If the code inside the lambda function is any longer than 60–80 chars, it's probably better to define it as a regular (nested) function.

For common operations like multiplication, use the functions from the operator module instead of lambda functions. For example, prefer operator.mul to lambda x, y: x * y.


Default Argument Values
-----------------------

Okay in most cases.

**Definition:** You can specify values for variables at the end of a function's parameter list, e.g., def foo(a, b=0):. If foo is called with only one argument, b is set to 0. If it is called with two arguments, b has the value of the second argument.

**Pros:** Often you have a function that uses lots of default values, but—rarely—you want to override the defaults. Default argument values provide an easy way to do this, without having to define lots of functions for the rare exceptions. Also, Python does not support overloaded methods/functions and default arguments are an easy way of "faking" the overloading behavior.

**Cons:** Default arguments are evaluated once at module load time. This may cause problems if the argument is a mutable object such as a list or a dictionary. If the function modifies the object (e.g., by appending an item to a list), the default value is modified.

**Decision:**

Okay to use with the following caveats:

- Do not use mutable objects as default values in the function or method definition.
    
    Yes::
        
        def foo(a, b=None):
            if b is None:
                b = []

    No::
        
        def foo(a, b=[]):
            ...

- Calling code must use named values for arguments with a default value. This helps document the code somewhat and helps prevent and detect interface breakage when more arguments are added.

    Usage::
        
        def foo(a, b=1):
            ...

    Yes::
        
        foo(1)
        foo(1, b=2)

    No::
        
        foo(1, 2)


Properties
----------

Use properties for accessing or setting data where you would normally have used simple, lightweight accessor or setter methods.

**Definition:** A way to wrap method calls for getting and setting an attribute as a standard attribute access when the computation is lightweight.

**Pros:** Readability is increased by eliminating explicit get and set method calls for simple attribute access. Allows calculations to be lazy. Considered the Pythonic way to maintain the interface of a class. In terms of performance, allowing properties bypasses needing trivial accessor methods when a direct variable access is reasonable. This also allows accessor methods to be added in the future without breaking the interface.

**Cons:** Properties are specified after the getter and setter methods are declared, requiring one to notice they are used for properties farther down in the code (except for readonly properties created with the @property decorator - see below). Must inherit from object. Can hide side-effects much like operator overloading. Can be confusing for subclasses.

**Decision:**

Use properties in new code to access or set data where you would normally have used simple, lightweight accessor or setter methods. Read-only properties should be created with the @property decorator.

Inheritance with properties can be non-obvious if the property itself is not overridden. Thus one must make sure that accessor methods are called indirectly to ensure methods overridden in subclasses are called by the property (using the Template Method DP).

Yes::
     
     import math
    
     class Square(object):
         """A square with two properties: a writable area and a read-only perimeter.

         To use:
         >>> sq = Square(3)
         >>> sq.area
         9
         >>> sq.perimeter
         12
         >>> sq.area = 16
         >>> sq.side
         4
         >>> sq.perimeter
         16
         """

         def __init__(self, side):
             self.side = side

         def __get_area(self):
             """Calculates the 'area' property."""
             return self.side ** 2

         def ___get_area(self):
             """Indirect accessor for 'area' property."""
             return self.__get_area()

         def __set_area(self, area):
             """Sets the 'area' property."""
             self.side = math.sqrt(area)

         def ___set_area(self, area):
             """Indirect setter for 'area' property."""
             self._SetArea(area)

         area = property(___get_area, ___set_area,
                         doc="""Gets or sets the area of the square.""")

         @property
         def perimeter(self):
             return self.side * 4


True/False evaluations
----------------------

Use the "implicit" false if at all possible.

**Definition:** Python evaluates certain values as false when in a boolean context. A quick "rule of thumb" is that all "empty" values are considered false so 0, None, [], {}, "" all evaluate as false in a boolean context.

**Pros:** Conditions using Python booleans are easier to read and less error-prone. In most cases, they're also faster.

**Cons:** May look strange to C/C++ developers.

**Decision:**

Use the "implicit" false if at all possible, e.g., if foo: rather than if foo != []:. There are a few caveats that you should keep in mind though:

- Never use == or != to compare singletons like None. Use is or is not.
- Beware of writing if x: when you really mean if x is not None:—e.g., when testing whether a variable or argument that defaults to None was set to some other value. The other value might be a value that's false in a boolean context!
- Never compare a boolean variable to False using ==. Use if not x: instead. If you need to distinguish False from None then chain the expressions, such as if not x and x is not None:.
- For sequences (strings, lists, tuples), use the fact that empty sequences are false, so if not seq: or if seq: is preferable to if len(seq): or if not len(seq):.
- When handling integers, implicit false may involve more risk than benefit (i.e., accidentally handling None as 0). You may compare a value which is known to be an integer (and is not the result of len()) against the integer 0.
    
    Yes::
        
        if not users:
            print 'no users'
        
        if foo == 0:
            self.handle_zero()
        
        if i % 10 == 0:
            self.handle_multiple_of_ten()

    No::
        
        if len(users) == 0:
            print 'no users'
        
        if foo is not None and not foo:
            self.handle_zero()
    
        if not i % 10:
            self.handle_multiple_of_ten()

Note that '0' (i.e., 0 as string) evaluates to true.


Deprecated Language Features
----------------------------

Use string methods instead of the string module where possible. Use function call syntax instead of apply. Use list comprehensions and for loops instead of filter, map, and reduce.

**Definition:** Current versions of Python provide alternative constructs that people find generally preferable.

**Decision:**

We do not use any Python version which does not support these features, so there is no reason not to use the new styles.

No::
    
    words = string.split(foo, ':')
    
    map(lambda x: x[1], filter(lambda x: x[2] == 5, my_list))
    
    apply(fn, args, kwargs)

Yes::
    
    words = foo.split(':')

    [x[1] for x in my_list if x[2] == 5]

    fn(*args, **kwargs)


Lexical Scoping
---------------

Okay to use.

**Definition:**

A nested Python function can refer to variables defined in enclosing functions, but can not assign to them. Variable bindings are resolved using lexical scoping, that is, based on the static program text. Any assignment to a name in a block will cause Python to treat all references to that name as a local variable, even if the use precedes the assignment. If a global declaration occurs, the name is treated as a global variable.

An example of the use of this feature is::
    
    def get_adder(summand1):
        """Returns a function that adds numbers to a given number."""
        def adder(summand2):
            return summand1 + summand2
    
        return adder

**Pros:** Often results in clearer, more elegant code. Especially comforting to experienced Lisp and Scheme (and Haskell and ML and …) programmers.

**Cons:**

Can lead to confusing bugs. Such as this example based on `PEP-0227 <http://http://www.python.org/dev/peps/pep-0227/>`_::
    
    i = 4
    def foo(x):
        def bar():
            print i,
        # ...
        # A bunch of code here
        # ...
        for i in x:  # Ah, i *is* local to Foo, so this is what Bar sees
            print i,
        bar()

So foo([1, 2, 3]) will print 1 2 3 3, not 1 2 3 4.

**Decision:** Okay to use.


Function and Method Decorators
------------------------------

Use decorators judiciously when there is a clear advantage.

**Definition:**

`Decorators for Functions and Methods <http://http://www.python.org/doc/2.4.3/whatsnew/node6.html>`_ (a.k.a "the @ notation"). The most common decorators are @classmethod and @staticmethod, for converting ordinary methods to class or static methods. However, the decorator syntax allows for user-defined decorators as well. Specifically, for some function my_decorator, this::
    
    class C(object):
        @my_decorator
        def method(self):
            # method body ...

is equivalent to::
    
    class C(object):
        def method(self):
            # method body ...
        method = my_decorator(method)

**Pros:** Elegantly specifies some transformation on a method; the transformation might eliminate some repetitive code, enforce invariants, etc.

**Cons:** Decorators can perform arbitrary operations on a function's arguments or return values, resulting in surprising implicit behavior. Additionally, decorators execute at import time. Failures in decorator code are pretty much impossible to recover from.

**Decision:**

Use decorators judiciously when there is a clear advantage. Decorators should follow the same import and naming guidelines as functions. Decorator pydoc should clearly state that the function is a decorator. Write unit tests for decorators.

Avoid external dependencies in the decorator itself (e.g. don't rely on files, sockets, database connections, etc.), since they might not be available when the decorator runs (at import time, perhaps from pychecker or other tools). A decorator that is called with valid parameters should (as much as possible) be guaranteed to succeed in all cases.

Decorators are a special case of "top level code" - see main for more discussion.


Threading
---------

Do not rely on the atomicity of built-in types.

While Python's built-in data types such as dictionaries appear to have atomic operations, there are corner cases where they aren't atomic (e.g. if __hash__ or __eq__ are implemented as Python methods) and their atomicity should not be relied upon. Neither should you rely on atomic variable assignment (since this in turn depends on dictionaries).

Use the Queue module's Queue data type as the preferred way to communicate data between threads. Otherwise, use the threading module and its locking primitives. Learn about the proper use of condition variables so you can use threading.Condition instead of using lower-level locks.


Power Features
--------------

Avoid these features.

**Definition:** Python is an extremely flexible language and gives you many fancy features such as metaclasses, access to bytecode, on-the-fly compilation, dynamic inheritance, object reparenting, import hacks, reflection, modification of system internals, etc.

**Pros:** These are powerful language features. They can make your code more compact.

**Cons:** It's very tempting to use these "cool" features when they're not absolutely necessary. It's harder to read, understand, and debug code that's using unusual features underneath. It doesn't seem that way at first (to the original author), but when revisiting the code, it tends to be more difficult than code that is longer but is straightforward.

**Decision:** Avoid these features in your code.


Python Style Rules
~~~~~~~~~~~~~~~~~~

Semicolons
----------

Do not terminate your lines with semi-colons and do not use semi-colons to put two commands on the same line.


Line length
-----------

Maximum line length is 80 characters.

**Exception:** lines importing modules may end up longer than 80 characters only if using Python 2.4 or earlier.

Make use of Python's `implicit line joining inside parentheses, brackets and braces <http://http://www.python.org/doc/ref/implicit-joining.html>`_. If necessary, you can add an extra pair of parentheses around an expression.

Yes::
    
    foo_bar(self, width, height, color='black', design=None, x='foo',
             emphasis=None, highlight=0)
    
    if (width == 0 and height == 0 and
        color == 'red' and emphasis == 'strong'):

When a literal string won't fit on a single line, use parentheses for implicit line joining.

::
    
    x = ('This will build a very long long '
           'long long long long long long string')

Make note of the indentation of the elements in the line continuation examples above; see the indentation section for explanation.


Parentheses
-----------

Use parentheses sparingly.

Do not use them in return statements or conditional statements unless using parentheses for implied line continuation. (See above.) It is however fine to use parentheses around tuples.

Yes::

     if foo:
         bar()
     while x:
         x = bar()
     if x and y:
         bar()
     if not x:
         bar()
     return foo
     for (x, y) in dict.items(): ...

No::

     if (x):
         bar()
     if not(x):
         bar()
     return (foo)

Indentation
-----------

Indent your code blocks with 4 spaces.

Never use tabs or mix tabs and spaces. In cases of implied line continuation, you should align wrapped elements either vertically, as per the examples in the line length section; or using a hanging indent of 4 spaces, in which case there should be no argument on the first line.

Yes::

       # Aligned with opening delimiter
       foo = long_function_name(var_one, var_two,
                                var_three, var_four)

       # 4-space hanging indent; nothing on first line
       foo = long_function_name(
           var_one, var_two, var_three,
           var_four)

No::

       # Stuff on first line forbidden
       foo = long_function_name(var_one, var_two,
           var_three, var_four)

       # 2-space hanging indent forbidden
       foo = long_function_name(
         var_one, var_two, var_three,
         var_four)

Blank Lines
-----------

Two blank lines between top-level definitions, one blank line between method definitions.

Two blank lines between top-level definitions, be they function or class definitions. One blank line between method definitions and between the class line and the first method. Use single blank lines as you judge appropriate within functions or methods.

Whitespace
----------

Follow standard typographic rules for the use of spaces around punctuation.

No whitespace inside parentheses, brackets or braces.

Yes::

       spam(ham[1], {eggs: 2}, [])

No::

       spam( ham[ 1 ], { eggs: 2 }, [ ] )

No whitespace before a comma, semicolon, or colon. Do use whitespace after a comma, semicolon, or colon except at the end of the line.

Yes::

       if x == 4:
              print x, y
       x, y = y, x

No::

       if x == 4 :
              print x , y
       x , y = y , x

No whitespace before the open paren/bracket that starts an argument list, indexing or slicing.

Yes::

       spam(1)

No::

       spam (1)

Yes::

       dict['key'] = list[index]

No::

       dict ['key'] = list [index]

Surround binary operators with a single space on either side for assignment (=), comparisons (==, <, >, !=, <>, <=, >=, in, not in, is, is not), and Booleans (and, or, not). Use your better judgment for the insertion of spaces around arithmetic operators but always be consistent about whitespace on either side of a binary operator.

Yes::

       x == 1

No::

       x<1

Don't use spaces around the '=' sign when used to indicate a keyword argument or a default parameter value.

Yes::

       def complex(real, imag=0.0): return magic(r=real, i=imag)

No::

       def complex(real, imag = 0.0): return magic(r = real, i = imag)

Don't use spaces to vertically align tokens on consecutive lines, since it becomes a maintenance burden (applies to :, #, =, etc.):

Yes::

       foo = 1000  # comment
       long_name = 2  # comment that should not be aligned

       dictionary = {
             "foo": 1,
             "long_name": 2,
       }

No::

       foo       = 1000  # comment
       long_name = 2     # comment that should not be aligned

       dictionary = {
              "foo"      : 1,
       "long_name": 2,
       }

Shebang Line
------------

All .py files (except __init__.py package files) should begin with a #!/usr/bin/python<version> shebang line.

Always use the most specific version that you can to ensure compatibility. For examples, if your program uses a language feature that that first appeared in Python 2.4, use /usr/bin/python2.4 (or something newer) instead of /usr/bin/python2. Otherwise, your program might not behave the way you expect it to, because the interpreter uses an older version of the language.

Comments
--------

Be sure to use the right style for module, function, method and in-line comments.

Doc Strings
-----------

Python has a unique commenting style using doc strings. A doc string is a string that is the first statement in a package, module, class or function. These strings can be extracted automatically through the __doc__ member of the object and are used by pydoc. (Try running pydoc on your module to see how it looks.) Our convention for doc strings is to use the three double-quote format for strings. A doc string should be organized as a summary line (one physical line) terminated by a period, question mark, or exclamation point, followed by a blank line, followed by the rest of the doc string starting at the same cursor position as the first quote of the first line. There are more formatting guidelines for doc strings below.

Modules
-------

Every file should contain the following items, in order:

- a copyright statement (for example, Copyright 2008 Google Inc.)

- a license boilerplate. Choose the appropriate boilerplate for the license used by the project (for example, Apache 2.0, BSD, LGPL, GPL)

- an author line to identify the original author of the file

Functions and Methods
---------------------

Any function or method which is not both obvious and very short needs a doc string. Additionally, any externally accessible function or method regardless of length or simplicity needs a doc string. The doc string should include what the function does and have detailed descriptions of the input and output. It should not, generally, describe how it does it unless it's some complicated algorithm. For tricky code block/inline comments within the code are more appropriate. The doc string should give enough information to write a call to the function without looking at a single line of the function's code. Args should be individually documented, an explanation following after a colon, and should use a uniform hanging indent of 2 or 4 spaces. The doc string should specify the expected types where specific types are required. A "Raises:" section should list all exceptions that can be raised by the function. The doc string for generator functions should use "Yields:" rather than "Returns:".

::

    def fetch_bigtable_rows(big_table, keys, other_silly_variable=None):
        """Fetches rows from a Bigtable.
    
        Retrieves rows pertaining to the given keys from the Table instance
        represented by big_table.  Silly things may happen if
        other_silly_variable is not None.
    
        Args:
            big_table: An open Bigtable Table instance.
            keys: A sequence of strings representing the key of each table row
                to fetch.
            other_silly_variable: Another optional variable, that has a much
                longer name than the other args, and which does nothing.
    
        Returns:
            A dict mapping keys to the corresponding table row data
            fetched. Each row is represented as a tuple of strings. For
            example:
    
            {'Serak': ('Rigel VII', 'Preparer'),
             'Zim': ('Irk', 'Invader'),
             'Lrrr': ('Omicron Persei 8', 'Emperor')}
    
            If a key from the keys argument is missing from the dictionary,
            then that row was not found in the table.
    
        Raises:
            IOError: An error occurred accessing the bigtable.Table object.
        """
    pass

Classes
-------

Classes should have a doc string below the class definition describing the class. If your class has public attributes, they should be documented here in an Attributes section and follow the same formatting as a function's Args section.

::

    class SampleClass(object):
        """Summary of class here.
    
        Longer class information....
        Longer class information....
    
        Attributes:
            likes_spam: A boolean indicating if we like SPAM or not.
            eggs: An integer count of the eggs we have laid.
        """
    
        def __init__(self, likes_spam=False):
            """Inits SampleClass with blah."""
            self.likes_spam = likes_spam
            self.eggs = 0
    
        def public_method(self):
            """Performs operation blah."""

Block and Inline Comments
-------------------------

The final place to have comments is in tricky parts of the code. If you're going to have to explain it at the next `code review <http://http://en.wikipedia.org/wiki/Code_review>`_, you should comment it now. Complicated operations get a few lines of comments before the operations commence. Non-obvious ones get comments at the end of the line.

::

    # We use a weighted dictionary search to find out where i is in
    # the array.  We extrapolate position based on the largest num
    # in the array and the array size and then do binary search to
    # get the exact number.

    if i & (i-1) == 0:        # true iff i is a power of 2

To improve legibility, these comments should be at least 2 spaces away from the code.

On the other hand, never describe the code. Assume the person reading the code knows Python (though not what you're trying to do) better than you do.

::

    # BAD COMMENT: Now go through the b array and make sure whenever i occurs
    # the next element is i+1

Classes
-------

If a class inherits from no other base classes, explicitly inherit from object. This also applies to nested classes.

No::

    class SampleClass:
        pass


    class OuterClass:

        class InnerClass:
            pass

Yes::

    class SampleClass(object):
         pass


     class OuterClass(object):

         class InnerClass(object):
             pass


     class ChildClass(ParentClass):
         """Explicitly inherits from another class already."""

Inheriting from object is needed to make properties work properly, and it will protect your code from one particular potential incompatibility with Python 3000. It also defines special methods that implement the default semantics of objects including __new__, __init__, __delattr__, __getattribute__, __setattr__, __hash__, __repr__, and __str__.

Strings
-------

Use the % operator for formatting strings, even when the parameters are all strings. Use your best judgement to decide between + and % though.

No::

    x = '%s%s' % (a, b)  # use + in this case
    x = imperative + ', ' + expletive + '!'
    x = 'name: ' + name + '; score: ' + str(n)

Yes::

    x = a + b
    x = '%s, %s!' % (imperative, expletive)
    x = 'name: %s; score: %d' % (name, n)

Avoid using the + and += operators to accumulate a string within a loop. Since strings are immutable, this creates unnecessary temporary objects and results in quadratic rather than linear running time. Instead, add each substring to a list and ''.join the list after the loop terminates (or, write each substring to a cStringIO.StringIO buffer).

No::

    employee_table = '<table>'
    for last_name, first_name in employee_list:
        employee_table += '<tr><td>%s, %s</td></tr>' % (last_name, first_name)
    employee_table += '</table>'

Yes::

     items = ['<table>']
     for last_name, first_name in employee_list:
         items.append('<tr><td>%s, %s</td></tr>' % (last_name, first_name))
     items.append('</table>')
     employee_table = ''.join(items)

Use """ for multi-line strings rather than '''. Note, however, that it is often cleaner to use implicit line joining since multi-line strings do not flow with the indentation of the rest of the program:

No::

        print """This is pretty ugly.
    Don't do this.
    """

Yes::

    print ("This is much nicer.\n"
             "Do it this way.\n")

TODO Comments
-------------

Use TODO comments for code that is temporary, a short-term solution, or good-enough but not perfect.

TODOs should include the string TODO in all caps, followed by your name, e-mail address, or other identifier in parentheses. A colon is optional. A comment explaining what there is to do is required. The main purpose is to have a consistent TODO format searchable by the person adding the comment (who can provide more details upon request). A TODO is not a commitment to provide the fix yourself.

::

    # TODO(kl@gmail.com): Drop the use of "has_key".
    # TODO(Zeke) change this to use relations.

If your TODO is of the form "At a future date do something" make sure that you either include a very specific date ("Fix by November 2009") or a very specific event ("Remove this code when all clients can handle XML responses.").

Imports formatting
------------------

Imports should be on separate lines.

E.g.:

Yes::

     import os
     import sys

No::

    import os, sys

Imports are always put at the top of the file, just after any module comments and doc strings and before module globals and constants. Imports should be grouped with the order being most generic to least generic:

- standard library imports

- third-party imports

- application-specific imports

Within each grouping, imports should be sorted lexicographically, ignoring case, according to each module's full package path.

::

    import foo
    from foo import bar
    from foo.bar import baz
    from foo.bar import Quux
    from Foob import ar

Statements
----------

Generally only one statement per line.

However, you may put the result of a test on the same line as the test only if the entire statement fits on one line. In particular, you can never do so with try/except since the try and except can't both fit on the same line, and you can only do so with an if if there is no else.

Yes::

  if foo: bar(foo)

No::

  if foo: bar(foo)
  else:   baz(foo)

  try:               bar(foo)
  except ValueError: baz(foo)

  try:
      bar(foo)
  except ValueError: baz(foo)

Access Control

If an accessor function would be trivial you should use public variables instead of accessor functions to avoid the extra cost of function calls in Python. When more functionality is added you can use property to keep the syntax consistent.

On the other hand, if access is more complex, or the cost of accessing the variable is significant, you should use function calls (following the Naming guidelines) such as get_foo() and set_foo(). If the past behavior allowed access through a property, do not bind the new accessor functions to the property. Any code still attempting to access the variable by the old method should break visibly so they are made aware of the change in complexity.

Naming
------

module_name, package_name, ClassName, method_name, ExceptionName, function_name, GLOBAL_VAR_NAME, instance_var_name, function_parameter_name, local_var_name.

**Names to Avoid**

- single character names except for counters or iterators

- dashes (-) in any package/module name

- __double_leading_and_trailing_underscore__ names (reserved by Python)

**Naming Convention**

- "Internal" means internal to a module or protected or private within a class.

- Prepending a single underscore (_) has some support for protecting module variables and functions (not included with import * from). Prepending a double underscore (__) to an instance variable or method effectively serves to make the variable or method private to its class (using name mangling).

- Place related classes and top-level functions together in a module. Unlike Java, there is no need to limit yourself to one class per module.

- Use CapWords for class names, but lower_with_under.py for module names. Although there are many existing modules named CapWords.py, this is now discouraged because it's confusing when the module happens to be named after a class. ("wait -- did I write import StringIO or from StringIO import StringIO?")

**Guidelines derived from Guido's Recommendations**


+----------------------------+--------------------+-------------------------------------------------------------------+
| **Type**                   | **Public**         | **Internal**                                                      |
+----------------------------+--------------------+-------------------------------------------------------------------+
| Packages                   | lower_with_under   |                                                                   |
+----------------------------+--------------------+-------------------------------------------------------------------+
| Modules                    | lower_with_under   | _lower_with_under                                                 |
+----------------------------+--------------------+-------------------------------------------------------------------+
| Classes                    | CapWords           | _CapWords                                                         |
+----------------------------+--------------------+-------------------------------------------------------------------+
| Exceptions                 | CapWords           |                                                                   |
+----------------------------+--------------------+-------------------------------------------------------------------+
| Functions                  | lower_with_under() | _lower_with_under()                                               |
+----------------------------+--------------------+-------------------------------------------------------------------+
| Global/Class Constants     | CAPS_WITH_UNDER    | _CAPS_WITH_UNDER                                                  |
+----------------------------+--------------------+-------------------------------------------------------------------+
| Global/Class Variables     | lower_with_under   | _lower_with_under                                                 |
+----------------------------+--------------------+-------------------------------------------------------------------+
| Instance Variables         | lower_with_under   | _lower_with_under (protected) or __lower_with_under (private)     |
+----------------------------+--------------------+-------------------------------------------------------------------+
| Method Names               | lower_with_under() | _lower_with_under() (protected) or __lower_with_under() (private) |
+----------------------------+--------------------+-------------------------------------------------------------------+
| Function/Method Parameters | lower_with_under   |                                                                   |
+----------------------------+--------------------+-------------------------------------------------------------------+
| Local Variables            | lower_with_under   |                                                                   |
+----------------------------+--------------------+-------------------------------------------------------------------+
		
Main
----

Even a file meant to be used as a script should be importable and a mere import should not have the side effect of executing the script's main functionality. The main functionality should be in a main() function.

In Python, pychecker, pydoc, and unit tests require modules to be importable. Your code should always check if __name__ == '__main__' before executing your main program so that the main program is not executed when the module is imported.

::

    def main():
          ...

    if __name__ == '__main__':
        main()

All code at the top level will be executed when the module is imported. Be careful not to call functions, create objects, or perform other operations that should not be executed when the file is being pychecked or pydoced.

Parting Words
-------------

BE CONSISTENT.

If you're editing code, take a few minutes to look at the code around you and determine its style. If they use spaces around all their arithmetic operators, you should too. If their comments have little boxes of hash marks around them, make your comments have little boxes of hash marks around them too.

The point of having style guidelines is to have a common vocabulary of coding so people can concentrate on what you're saying rather than on how you're saying it. We present global style rules here so people know the vocabulary, but local style is also important. If code you add to a file looks drastically different from the existing code around it, it throws readers out of their rhythm when they go to read it. Avoid this.
