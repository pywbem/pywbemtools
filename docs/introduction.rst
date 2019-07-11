.. Copyright  2017 IBM Corp. and Inova Development Inc.
..
.. Licensed under the Apache License, Version 2.0 (the "License");
.. you may not use this file except in compliance with the License.
.. You may obtain a copy of the License at
..
..    http://www.apache.org/licenses/LICENSE-2.0
..
.. Unless required by applicable law or agreed to in writing, software
.. distributed under the License is distributed on an "AS IS" BASIS,
.. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
.. See the License for the specific language governing permissions and
.. limitations under the License.
..


.. _`Introduction`:

Introduction
============

.. _`pywbemtools Features`:

pywbemtools Features
--------------------

The pywbemtools package (part of the pywbem github project) is a pure python package
that is a container for multiple client tools and applications that use the
pywbem APIs defined by the pywbem package in the github pywbem project to
interact with WBEM Servers.

The goal of this package is to provide a simple, complete and extensible
tools to allow inspection and management of the data in WBEM
servers that are compatible with the DMTF specifications.

Today the only tool in this package is pywbemcli:

Pywbemcli Command Line Browser
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

pywbemcli, an extensible command line browser for WBEM Servers.  This tool
provides access to a WBEM server directly from the command line.
It provides commands to:

1. Inspect and manage the primitive CIM Objects CIMClasses, CIMInstances,
and CIM QualifierDeclaractions defined by the server using the
requests APIs of the pywbem package.

2. Inspect and manage higher level components of the WBEM Server including

    - Namespaces
    - Profiles
    - Indication Subscriptions


.. _`Installation`:

Installation
------------

The easiest way to install the pywbemtools package is by using Pip:

::

    $ pip install pywbemtools

This will download and install the latest released version of pywbemcli and
its dependent packages into your current Python environment (e.g. into your
system Python or into a virtual Python environment).

It is often beneficial to set up a `virtual Python environment`_, because that
leaves your system Python installation unchanged.

.. _virtual Python environment: http://docs.python-guide.org/en/latest/dev/virtualenvs/

As an alternative, if you want to install the latest development level of the
pywbemcli package for some reason, install directly from the ``master`` branch
of the Git repository of the package:

::

    $ pip install git+https://github.com/pywbem/pywbemtools.git@master

You can verify that the pywbemtools package and its dependent packages are
installed correctly by importing the package into Python:

::

    $ python -c "import pywbemtools; print('ok')"
    ok

.. _`Setting up pywbemtools`:

Setting up pywbemtools
----------------------

Currently there is no setup ones the package is installed.

Simply calling pywbemcli starts the cli tool

.. _`Deprecation policy`:

Deprecation policy
------------------

Pywbemtools attempts to be as backwards compatible as possible.

Occasionally functionality needs to be retired, because it is flawed and
a better but incompatible replacement has emerged.

In pywbemtools, such changes are done by deprecating existing functionality, without
removing it. The deprecated functionality is still supported throughout new
minor releases. Eventually, a new major release will break compatibility and
will remove the deprecated functionality.

In order to prepare users of pywbemtools for that, deprecation of functionality is
stated in the API documentation, and is made visible at runtime by issuing
Python warnings of type ``DeprecationWarning`` (see the Python
:mod:`py:warnings` module).

Since Python 2.7, ``DeprecationWarning`` messages are suppressed by default.
They can be shown for example in any of these ways:

* By specifying the Python command line option: ``-W default``
* By invoking Python with the environment variable: ``PYTHONWARNINGS=default``

It is recommended that users of the pywbemtools package run their test code with
``DeprecationWarning`` messages being shown, so they become aware of any use of
deprecated functionality.

Here is a summary of the deprecation and compatibility policy used by pywbem,
by release type:

* New update release (M.N.U -> M.N.U+1): No new deprecations; fully backwards
  compatible.
* New minor release (M.N.U -> M.N+1.0): New deprecations may be added; as
  backwards compatible as possible.
* New major release (M.N.U -> M+1.0.0): Deprecated functionality may get
  removed; backwards compatibility may be broken.

Compatibility is always seen from the perspective of the user of pywbemtools, so a
backwards compatible new pywbem release means that the user can safely upgrade
to that new release without encountering compatibility issues.

Versioning
----------

This documentation applies to version |release| of the pywbemtools package. You
can also see that version in the top left corner of this page.

The pywbemtools package uses the rules of `Semantic Versioning 2.0.0`_ for its
version.

.. _Semantic Versioning 2.0.0: http://semver.org/spec/v2.0.0.html

The package version can be accessed by programs using the
``pywbemtools.__version__`` variable [#]_:

.. autodata:: pywbemtools.pywbemcli.__version__

This documentation may have been built from a development level of the
package. You can recognize a development version of this package by the
presence of a ".devD" suffix in the version string. Development versions are
pre-versions of the next assumed version that is not yet released. For example,
version 0.5.1.dev2 is development pre-version #2 of the next version to be
released after 0.5.0. Version 1.5.1 is an `assumed` next version, because the
`actually released` next version might be 0.2.0 or even 1.0.0.

.. [#] For tooling reasons, that variable is shown as
   ``pywbemtools.pywbemcli.__version__`` in this documentation, but it should be
   accessed as ``pywbemtools.pywbemcli.__version__``.


.. _`Compatibility`:

Compatibility
-------------

In this package, compatibility is always seen from the perspective of the user
of the package. Thus, a backwards compatible new version of this package means
that the user can safely upgrade to that new version without encountering
compatibility issues.

This package uses the rules of `Semantic Versioning 2.0.0`_ for compatibility
between package versions, and for :ref:`deprecations <Deprecations>`.

The public API of this package that is subject to the semantic versioning
rules (and specificically to its compatibility rules) is the API described in
this documentation.

Violations of these compatibility rules are described in section
:ref:`Change log`.


.. _`Deprecations`:

Deprecations
------------

Deprecated functionality is marked accordingly in this documentation and in the
:ref:`Change log`, and is made visible at runtime by issuing Python warnings of
type :exc:`~py:exceptions.DeprecationWarning` (see :mod:`py:warnings` for
details).

Since Python 2.7, :exc:`~py:exceptions.DeprecationWarning` warnings are
suppressed by default. They can be shown for example in any of these ways:

* by specifying the Python command line option:

  ``-W default``

* by invoking Python with the environment variable:

  ``PYTHONWARNINGS=default``

* by issuing in your program:

  ::

      warnings.filterwarnings(action='default', category=DeprecationWarning)

It is recommended that users of this package run their test code with
:exc:`~py:exceptions.DeprecationWarning` warnings being shown, so they become
aware of any use of deprecated functionality.

It is even possible to raise an exception instead of issuing a warning message
upon the use of deprecated functionality, by setting the action to ``'error'``
instead of ``'default'``.


.. _`Reporting issues`:

Reporting issues
----------------

If you encounter any problem with this package, or if you have questions of any
kind related to this package (even when they are not about a problem), please
open an issue in the `pywbemtools issue tracker`_.

.. _pywbemtools issue tracker: https://github.com/pywbem/pywbemtools/issues


.. _`License`:

License
-------

This package is licensed under the `Apache 2.0 License`_.

.. _Apache 2.0 License: https://raw.githubusercontent.com/pywbem/pywbemtools/master/LICENSE

