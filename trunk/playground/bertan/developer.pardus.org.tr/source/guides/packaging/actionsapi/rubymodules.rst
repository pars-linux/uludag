.. _rubymodules:

Rubymodules
===========

:Author: Semen Cirit
:Date: |today|
:Version: 0.1


get_config
-----------

::

    get_config(config)



Get the value of given configure parameter.

Examples::

    get_config('ruby_version')
    get_config('rubylibdir')
    get_config('ruby_install_name')

get_ruby_version
----------------

::

    get_ruby_version()

Returns the version of the ruby

get_rubylibdir
--------------

::

    get_rubylibdir()

Returns the ruby library directory.

get_sitedir
-----------

::

    get_sitedir()

Returns site_ruby directory

get_ruby_install_name
---------------------

::

    get_ruby_install_name()

Returns the ruby installation name.

get_gemhome
-----------

::

    get_gemhome()

Returns the Ruby gems directory.

get_sitelibdir
--------------

::

    get_sitelibdir()

Returns site_ruby library directory


auto_dodoc
----------

::

    auto_dodoc()

Copies AUTHORS, CHANGELOG, CONTRIBUTORS, Change*, KNOWN_BUGS, MAINTAINERS, NEWS, README*, History.txt files into /usr/share/doc/PACKAGE if they are exist.

install
-------

::

    install(parameters)

Install the ruby package with given parameters.

rake_install
------------

::

    rake_install(parameters)

Executes rake script with given parameters for installation.

run
---

::

    run(parameters)

Executes given parameters with ruby binary.

