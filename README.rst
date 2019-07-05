pywbemtools: Python Tools using pywbem API
==========================================

.. # begin of customization for the current version
.. |pywbemtools-version| replace:: 0.5.0
.. |pywbemtools-next-version| replace:: 0.6.0
.. |pywbemtools-next-issue| replace:: 193
.. # end of customization for the current version

.. |pywbemtools-next-issue-link-1| raw:: html

    <a href="https://github.com/pywbem/pywbemtools/issues/

.. |pywbemtools-next-issue-link-2| raw:: html

    ">issue

.. |pywbemtools-next-issue-link-3| raw:: html

    </a>

.. |pywbemtools-next-issue-link| replace:: |pywbemtools-next-issue-link-1|\ |pywbemtools-next-issue|\ |pywbemtools-next-issue-link-2| |pywbemtools-next-issue|\ |pywbemtools-next-issue-link-3|


.. |os-setup-link| raw:: html

    <a href="https://pywbemtools.readthedocs.io/en/stable/_downloads/pywbem_os_setup.sh">pywbem_os_setup.sh</a>

.. image:: https://img.shields.io/pypi/v/pywbemtools.svg
    :target: https://pypi.python.org/pypi/pywbemtools/
    :alt: Version on Pypi

.. # .. image:: https://img.shields.io/pypi/dm/pywbemtools.svg
.. #     :target: https://pypi.python.org/pypi/pywbemtools/
.. #     :alt: Pypi downloads

.. image:: https://travis-ci.org/pywbem/pywbem.svg?branch=master
    :target: https://travis-ci.org/pywbem/pywbemtools
    :alt: Travis test status (master)

.. image:: https://ci.appveyor.com/api/projects/status/i022iaeu3dao8j5x/branch/master?svg=true
    :target: https://ci.appveyor.com/project/andy-maier/pywbemtools
    :alt: Appveyor test status (master)

.. image:: https://readthedocs.org/projects/pywbem/badge/?version=latest
    :target: https://pywbemtools.readthedocs.io/en/latest/
    :alt: Docs build status (master)

.. image:: https://img.shields.io/coveralls/pywbem/pywbem.svg
    :target: https://coveralls.io/r/pywbem/pywbemtools
    :alt: Test coverage (master)

.. image:: https://img.shields.io/badge/License-Apache License 2.0-green.svg

.. image:: https://img.shields.io/pypi/pyversions/pywbemtools.svg?color=brightgreen
    :alt: PyPI - Python Version

.. # .. contents:: **Contents:**
.. #    :local:

Overview
--------

The pywbemtools repository contains user tools that utilize the pywbem client api
to allow a user to inspect and manage WBEM servers.

The current release consists of a single tool, a command line browser
``pywbemcli`` that is capable of inspecting and managing the classes,
instances, and qualifier declarations defined in a WBEMServer and in
addtion, inspecting the WBEMServer characteristics such as namespaces,
profiles, and indication subscriptions.

Installation Requirements
-------------------------

1. Python 2.7, 3.4 - 3.7

2. Operating Systems: Linux, Windows(native and with UNIX-like environments)

Installation
------------

The quick way:

.. code-block:: bash

    $ pip install pywbemtools

For more details, see the `Installation section`_ in the documentation.

.. _Installation section: http://pywbemtools.readthedocs.io/en/stable/intro.html#installation

Documentation
-------------

The latest pywbemtools documentation is available on ReadTheDocs:

* `Documentation for latest released version`_

.. _Documentation for latest released version: https://pywbemtools.readthedocs.io/en/stable/

* `Documentation for latest unreleased development version`_

.. _Documentation for latest unreleased development version: https://pywbemtools.readthedocs.io/en/latest/

The documentation includes an overview, user documentation including the syntax of commands and subcommands,
examples of usage, and developer documentation.

.. _Presentations: https://pywbem.github.io/pywbem/documentation.html

The detailed change history for the latest released version in the
`Change log section`_.

.. _Change log section: https://pywbem.readthedocs.io/en/stable/changes.html


Quickstart
----------

pywbemcli
^^^^^^^^^

The following are examples of pywbemcli commands:

All commands within pywbemcli include help as the --help or -h option::

    pywbemcli --help

The WBEM CIM/XML operations may be executed individually.


Executing the CIM/XML EnumerateClasses operation


.. code-block:: text

    pywbemcli -s https://localhost -n xxx -p yyy class get CIM_ManagedElement

       [Abstract ( true ),
        Version ( "2.19.0" ),
        UMLPackagePath ( "CIM::Core::CoreElements" ),
        Description (
           "ManagedElement is an abstract class that provides a common superclass "
           "(or top of the inheritance tree) for the non-association classes in "
           "the CIM Schema." )]
    class CIM_ManagedElement {

          [Description (
              "InstanceID is an optional property that may be used to opaquely and "
    . . .
   string ElementName;

    };

Executing the CIM/XML EnumerateInstances operation:

.. code-block:: text

    pywbemcli -s https://localhost instance get PyWBEM_Person.CreationClassName=\"PyWBEM_Person\",Name=\"Alice\"

    instance of PyWBEM_Person {
       ...
       Secretary = NULL;
       Title = NULL;
       CreationClassName = "PyWBEM_Person";
       Name = "Alice";
    };

Other operations against WBEM servers include getting information on namespaces,
registered profiles, and WBEM server brand informaton:

.. code-block:: text

    pywbemcli -s https://localhost server interop

    Server Interop Namespace:
    Namespace Name
    ----------------
    root/PG_InterOp

Pywbemcli can also be executed in an interactive mode:

.. code-block:: text

    $ pywbemcli -s http://localhost -u kschopmeyer -p test8play
    Enter 'help' for help, <CTRL-D> or ':q' to exit pywbemcli.
    pywbemcli> server brand

    Server Brand:
    WBEM Server Brand
    -------------------
    OpenPegasus
    pywbemcli> server interop

    Server Interop Namespace:
    Namespace Name
    ----------------
    root/PG_InterOp
    pywbemcli> :q
    $


Project Planning
----------------

For each upcoming release, the bugs and feature requests that are planned to
be addressed in that release are listed in the
`issue tracker <https://github.com/pywbem/pywbemtools/issues>`_
with an according milestone set that identifies the target release.
The due date on the milestone definition is the planned release date.
There is usually also an issue that sets out the major goals for an upcoming
release.

Planned Next Release
--------------------

Pywbemtools |pywbemtools-next-version| is in development.

Pywbemtools |pywbemtools-next-issue-link| defines the basic direction for version
|pywbemtools-next-version|.

Contributing
------------

For information on how to contribute to this project, see the
`Development section`_ in the documentation.

.. _Development section: http://pywbemtools.readthedocs.io/en/stable/development.html

License
-------

The pywbemtools package is licensed under the `Apache 2.0 License`_.

.. _Apache 2.0 License: https://github.com/pywbem/pywbemtools/tree/master/LICENSE.txt
