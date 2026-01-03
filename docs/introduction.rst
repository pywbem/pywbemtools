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

* :ref:`pywbemcli <Pywbemcli command>` - A command line tool using
  the :ref:`Pywbemcli command line interface` with a :ref:`Command mode` and
  and :ref:`Interactive mode` that provides command groups and commands for the
  pywbemcli client including:

  - Explore the CIM data of WBEM servers. It can manage/inspect the CIM model
    components including CIM classes(:ref:`Class command group`), CIM
    instances(:ref:`Instance command group`), and CIM qualifiers and execute
    CIM methods and queries on the WBEM server. Thus, for example, the command
    :ref:`class enumerate <Class enumerate command>` returns CIM classes from
    the  WBEM server defined by the current :term:`connection definition`.

  - Execute specific CIM-XML operations on the WBEM server as defined in `DMTF`_
    standard :term:`DSP0200` (CIM Operations over HTTP).

  - Display the responses in a variety of formats (:ref:`Output formats`)
    including viewing in the MOF, XML, pywbem Python formats and as
    tables and trees of hierarchical objects such as CIM classes.

    * Inspect and manage WBEM server functionality including:

      * :term:`CIM namespaces <CIM namespace>` (:ref:`Namespace command group`)
      * Advertised WBEM management profiles (:ref:`Profile command group`)
      * WBEM server brand and version information (:ref:`Server command group`)
      * WBEM server indication subscription data (:ref:`Subscription command group`)

  - Capture detailed information on CIM-XML interactions with the WBEM server
    including time statistics and details of data flow.

  - Maintain a file (:term:`connections file`) with persisted WBEM
    :term:`connection definitions <connection definition>` so that pywbemcli
    can access multiple WBEM servers by name. See :ref:`Connection command group`

  - Use an integrated :ref:`Mock WBEM Server` to try out commands or
    demonstrate server capabilities. The mock server can be loaded with CIM
    objects defined in MOF files or via Python scripts.

* :ref:`pywbemlistener <Pywbemlistener command>` - A command line utility that
  manages WBEM indication listeners running as background processes on the
  local system and displays/logs CIM indications received by these listeners.

CIM/WBEM standards are used for a wide variety of systems management tasks
in the industry including DMTF management standards and the `SNIA`_
Storage Management Initiative Specification (`SMI-S`_).

.. _pywbem package on Pypi: https://pypi.org/project/pywbem/
.. _DMTF: https://www.dmtf.org/
.. _CIM/WBEM standards: https://www.dmtf.org/standards/wbem/
.. _SNIA: https://www.snia.org/
.. _SMI-S: https://www.snia.org/forums/smi/tech_programs/smis_home


.. _`Supported environments`:

Supported environments
----------------------

.. _pywbem WBEM servers documentation: https://pywbem.readthedocs.io/en/stable/intro.html#wbem-servers

The pywbemtools package is supported in these environments:

* Operating systems: Linux, Windows (native and Unix-like environments
  (ex. Cygwin), OS-X
* Python versions: 3.9 and greater
* WBEM servers: Any WBEM server that conforms to the DMTF specifications listed
  in :ref:`Standards conformance`. WBEM servers supporting older versions of
  these standards are also supported, but may have limitations.
  See the `pywbem WBEM servers documentation`_ for more details.


.. _`Installation`:

Installation
------------

This section describes the installation for users of pywbemtools.

The setup for developers of pywbemtools is described in
:ref:`Pywbemtools development`.

Installation using pipx
~~~~~~~~~~~~~~~~~~~~~~~

.. _virtual Python environment: https://docs.python-guide.org/en/latest/dev/virtualenvs/

The recommended way to use the pywbemtools Python package is by installing it with
pipx.

Pipx creates a `virtual Python environment`_ under the covers and installs the
pywbemtools Python package into that environment and makes the ``pywbemcli``
and ``pywbemlistener`` commands available in a directory that is in the PATH.
These commands will be available that way, regardless of whether or not you
have a virtual Python environment active (that you may need for other purposes).

1.  Prerequisite: Install pipx as an OS-level package

    Follow the steps at https://pipx.pypa.io/stable/installation/ to install
    pipx as an OS-level package to your local system.

2.  Without having any virtual Python environment active, install pywbemtools using
    pipx

    To install the latest released version of pywbemtools:

    .. code-block:: bash

        $ pipx install pywbemtools

    To install a specific released version of pywbemtools, e.g. 1.2.0:

    .. code-block:: bash

        $ pipx install pywbemtools==1.2.0

    To install a specific development branch of pywbemtools, e.g. master:

    .. code-block:: bash

        $ pipx install git+https://github.com/pywbem/pywbemtools.git@master

    To install pywbemtools with a non-default Python version, e.g. 3.10:

    .. code-block:: bash

        $ pipx install pywbemtools --python python3.10

Installation into a virtual Python environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In some cases it may be useful to install pywbemtools into your own
`virtual Python environment`_. That avoids the dependency to pipx, but it
requires you to activate the virtual environment every time you want to use the
``pywbemcli`` or ``pywbemlistener`` commands.

There are a number of ways virtual Python environments can be created. This
documentation describes the use of "virtualenv":

1.  Prerequisite: Install virtualenv into system Python:

    .. code-block:: bash

        $ pip install virtualenv

2.  Create and activate a virtual Python environment:

    .. code-block:: bash

        $ virtualenv ~/.virtualenvs/pywbemtools
        $ source ~/.virtualenvs/pywbemtools/bin/activate

3.  Install pywbemtools into the virtual Python environment:

    To install the latest released version of pywbemtools so that it uses your
    default Python version:

    .. code-block:: bash

        (pywbemtools) $ pip install pywbemtools

    If you want to use `uv <https://docs.astral.sh/uv/>`_ for installing Python
    packages, this can be done with:

    .. code-block:: bash

        (pywbemtools) $ uv pip install pywbemtools

    In the remainder of this section, only the installation with "pip" is
    described, but "uv" can be used as well.

    To install a specific released version of pywbemtools, e.g. 1.2.0:

    .. code-block:: bash

        (pywbemtools) $ pip install pywbemtools==1.2.0

    To install a specific development branch of pywbemtools, e.g. master:

    .. code-block:: bash

        (pywbemtools) $ pip install git+https://github.com/pywbem/pywbemtools.git@master

Installation into a system Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Your system Python version(s) are installed using OS-level packages for all the
Python functionality.

Adding packages to your system Python using Python packages from Pypi may create
issues. This is why recent
versions of pip raise a warning when attempting to install into the system
Python. Even if you install a Python package from Pypi into your user's space,
this may create issues.

The main issue is that the more Python packages you install into the system
Python, the more likely there will be incompatible Python package dependencies.

Another issue is when you replace OS-level packages with Python packages.

In order to avoid these issues, you should install pywbemtools into the system
Python only in cases where the system has a well-defined scope and you have
full control over the set of OS-level and Python-level packages, for example
when building a Docker container.


.. _`Troubleshooting the installation`:

Troubleshooting the installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. index:: pair; troubleshooting: pywbem

Support for correcting a number of installation issues can be found in the
`pywbem troubleshooting documentation. <https://pywbem.readthedocs.io/en/latest/appendix.html#troubleshooting>`_


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
