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

.. _`Pywbemtools Features`:

Pywbemtools features
--------------------

Pywbemtools is a collection of command line tools that communicate with WBEM
servers. The tools are written in pure Python and support Python 2 and Python
3.

At this point, pywbemtools includes a single command line tool named
``pywbemcli`` that uses the `pywbem package on Pypi`_ to issue operations to a
WBEM server using the `CIM/WBEM standards`_ defined by the `DMTF`_ to perform
system management tasks.

CIM/WBEM standards are used for a wide variety of systems management tasks
in the industry including DMTF management standards and the `SNIA`_
Storage Management Initiative Specification (`SMI-S`_).

.. _pywbem package on Pypi: https://pypi.org/project/pywbem/
.. _DMTF: https://www.dmtf.org/
.. _CIM/WBEM standards: https://www.dmtf.org/standards/wbem/
.. _SNIA: https://www.snia.org/
.. _SMI-S: https://www.snia.org/forums/smi/tech_programs/smis_home

The pywbemtools package includes the following tools:

1. :ref:`Pywbemcli command` - provides access to WBEM servers from the command line


.. _`Supported environments`:

Supported environments
----------------------

.. _pywbem WBEM servers documentation: https://pywbem.readthedocs.io/en/stable/intro.html#wbem-servers

The pywbemtools package is supported in these environments:

* Operating systems: Linux, Windows (native and Unix-like environments
  (ex. Cygwin), OS-X
* Python versions: 2.7, 3.4, and greater
* WBEM servers: Any WBEM server that conforms to the DMTF specifications listed
  in :ref:`Standards conformance`. WBEM servers supporting older versions of
  these standards are also supported, but may have limitations.
  See the `pywbem WBEM servers documentation`_ for more details.


.. _`Installation`:

Installation
------------

.. _virtual Python environment: http://docs.python-guide.org/en/latest/dev/virtualenvs/
.. _PyPI: http://pypi.python.org/

This section describes the complete installation of pywbemtools with all steps
including prerequisite operating system packages.

The easiest way to install the pywbemtools package is using pip. Pip ensures
that any dependent Python packages also get installed.

Pip will install the packages into your currently active Python environment
(your system Python or your predefined `virtual Python environment`_).

It is beneficial to set up a `virtual Python environment`_ for your project,
because that leaves your system Python installation unchanged, it does not
require ``sudo`` rights, and gives you better control about the installed
packages and their versions.

If you want to contribute to the pywbem project, you need to set up a
development and test environment for pywbem. That has a larger set of OS-level
prerequisites and its setup is described in the :ref:`Pywbemtools development` chapter.


.. _`Installation prerequisites`:

Installation prerequisites
^^^^^^^^^^^^^^^^^^^^^^^^^^

The Python environment into which you want to install must have the following
Python packages installed:

- setuptools - http://pypi.python.org/pypi/setuptools
- wheel
- pip - generally installed with Python 3.x but may be a separate install
  with Python 2.7 and with Cygwin Python releases.

Pywbemtools installs the pywbem package.

When using pywbem versions before 1.0.0 on Python 2, pywbem requires a number
of OS-level packages, and your system must have the following commands
installed:

* On native Windows:

  - ``choco`` - Chocolatey package manager. The pywbemtools package installation
    uses Chocolatey to install OS-level software. See https://chocolatey.org/
    for the installation instructions for Chocolatey.

  - ``wget`` - Download tool. Can be installed with: ``choco install wget``.

* On Linux, OS-X, UNIX-like environments on Windows (e.g. Cygwin):

  - ``wget`` - Download tool. Can be installed using the OS-level package
    manager for the platform.

.. _`Installation with pip`:

Installation with pip
^^^^^^^^^^^^^^^^^^^^^

When using pywbem versions before 1.0.0 on Python 2, install the OS-level
packages needed by the pywbem package as follows:

* On native Windows:

  .. code-block:: bash

      > wget -q https://raw.githubusercontent.com/pywbem/pywbem/master/pywbem_os_setup.bat
      > pywbem_os_setup.bat

* On Linux, OS-X, UNIX-like environments on Windows (e.g. Cygwin):

  .. code-block:: bash

      $ wget -q https://raw.githubusercontent.com/pywbem/pywbem/master/pywbem_os_setup.sh
      $ chmod 755 pywbem_os_setup.sh
      $ ./pywbem_os_setup.sh

  The ``pywbem_os_setup.sh`` script uses sudo internally, so your userid
  needs to have sudo permission.

If you want to install the needed OS-level packages manually, see
`pywbem prerequisite OS packages <https://pywbem.readthedocs.io/en/latest/intro.html#prerequisite-operating-system-packages-for-install>`_.

The following command downloads and installs the latest released version of the
pywbemtools package from `PyPI`_ into the currently active Python environment:

.. code-block:: text

    $ pip install pywbemtools

As an alternative, if you want to install the latest development level of the
pywbemtools package for some reason, install directly from the ``master``
branch of the Git repository of the package:

.. code-block:: text

    $ pip install git+https://github.com/pywbem/pywbemtools.git@master#egg=pywbemtools


.. _`Verification of the installation`:

Verification of the installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can verify that the pywbemtools package and its dependent packages are
installed correctly by invoking pywbemcli. Invoking with the ``--version``
option displays the installed version of both pywbem and pywbemtools as
shown in the following example:

.. code-block:: bash

    $ pywbemcli --version
    pywbemcli, version 0.5.0
    pywbem, version 0.14.4


.. _`Standards conformance`:

Standards conformance
---------------------

.. _pywbem standards conformance documentation: https://pywbem.readthedocs.io/en/stable/intro.html#standards-conformance

Pywbemtools attempts to comply to the maximum possible with the relevant standards.

Pywbemtools uses pywbem for communication with the WBEM server. Therefore
pywbemtools conformance to the relevant standards is defined in the `pywbem
standards conformance documentation`_.

Therefore, the level of conformance and limitations for pywbemtools is the same
as pywbem except for any specific notations in this document.


.. _`Deprecation policy`:

Deprecation policy
------------------

Pywbemtools attempts to be as backwards compatible as possible.

Occasionally functionality needs to be retired, because it is flawed and
a better but incompatible replacement has emerged.

In pywbemtools, such changes are done by deprecating existing functionality,
without removing it. The deprecated functionality is still supported throughout
new minor releases. Eventually, a new major release will break compatibility
and will remove the deprecated functionality.

In order to prepare users of pywbemtools for that, deprecation of functionality
is stated in the CLI documentation, and is made visible at runtime by issuing
Python warnings of type ``DeprecationWarning`` (see the Python
:mod:`py:warnings` module).

Since Python 2.7, ``DeprecationWarning`` messages are suppressed by default.
They can be shown for example by invoking pywbemcli with the environment
variable: ``PYTHONWARNINGS=default``, or by using the
ref:`--warn general option`.

It is recommended that users of the pywbemtools package run their test code with
``DeprecationWarning`` messages being shown, so they become aware of any use of
deprecated functionality.

Here is a summary of the deprecation and compatibility policy used by
pywbemtools, by release type:

* New update release (M.N.U -> M.N.U+1): No new deprecations; fully backwards
  compatible.
* New minor release (M.N.U -> M.N+1.0): New deprecations may be added; as
  backwards compatible as possible.
* New major release (M.N.U -> M+1.0.0): Deprecated functionality may get
  removed; backwards compatibility may be broken.

Compatibility is always seen from the perspective of the user of pywbemtools,
so a backwards compatible new pywbemtools release means that the user can
safely upgrade to that new release without encountering compatibility issues.

Versioning
----------

This documentation applies to version |release| of the pywbemtools package. You
can also see that version in the top left corner of this page.

The pywbemtools package uses the rules of `Semantic Versioning 2.0.0`_ for its
version.

.. _Semantic Versioning 2.0.0: http://semver.org/spec/v2.0.0.html


This documentation may have been built from a development level of the
package. You can recognize a development version of this package by the
presence of a ".devD" suffix in the version string. Development versions are
pre-versions of the next assumed version that is not yet released. For example,
version 0.5.1.dev2 is development pre-version #2 of the next version to be
released after 0.5.0. Version 1.5.1 is an `assumed` next version, because the
`actually released` next version might be 0.7.0 or even 1.0.0.


.. _`Compatibility`:

Compatibility
-------------

In this package, compatibility is always seen from the perspective of the user
of the package. Thus, a backwards compatible new version of this package means
that the user can safely upgrade to that new version without encountering
compatibility issues.

This package uses the rules of `Semantic Versioning 2.0.0`_ for compatibility
between package versions, and for deprecations.

The public command line interface of this package that is subject to the
semantic versioning rules (and specifically to its compatibility rules) is
the CLI syntax described in this documentation.

The output formats are currently not the subject of compatibility assurances.

Violations of these compatibility rules are described in section
:ref:`Change log`.


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
