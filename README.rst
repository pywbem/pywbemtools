pywbemtools: Python tools for communicating with WBEM servers
=============================================================

.. |os-setup-link| raw:: html

    <a href="https://pywbemtools.readthedocs.io/en/stable/_downloads/pywbem_os_setup.sh">pywbem_os_setup.sh</a>

.. image:: https://img.shields.io/pypi/v/pywbemtools.svg
    :target: https://pypi.python.org/pypi/pywbemtools/
    :alt: Version on Pypi

.. image:: https://travis-ci.org/pywbem/pywbemtools.svg?branch=master
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

.. image:: https://img.shields.io/pypi/pyversions/pywbemtools.svg?color=brightgreen
    :alt: PyPI - Python Version

.. # .. contents:: **Contents:**
.. #    :local:

Overview
--------

Pywbemtools is a collection of command line tools that communicate with WBEM
Servers. The tools are written in pure Python and support Python 2 and Python
3.

Pywbemtools provides a command line tool (pywbemcli) that uses the pywbem
Python WBEM client infrastructure to issue operations to a WBEM server using
the CIM/WBEM standards defined by the DMTF to perform system management tasks.

CIM/WBEM infrastructure is used for a wide variety of systems management tasks
in the industry including DMTF management standards and the SNIA Storage
Management Initiative Specification(SMI-S).

Pywbemcli provides the functionality to :

* Explore the CIM data of WBEM Servers. It can manage/inspect the CIM model
  components including CIM classes, CIM instances, and CIM qualifiers and execute
  CIM methods and queries on the WBEM server. It implements subcommands to
  execute the CIM-XML operations defined in the DMTF specification
  CIM Operations Over HTTP(DSP0200_).

* Inspect/manage WBEM server functionality such as CIM namespaces, WBEM
  registered profiles, and other server information.

* Capture detailed information on interactions with the WBEM server including
  time statistics.

.. _DSP0200: https://www.dmtf.org/sites/default/files/standards/documents/DSP0200_1.4.0.pdf

Installation Requirements
-------------------------

1. Python 2.7, 3.4 and higher

2. Operating Systems: Linux, MacOS, Windows(native) and Windows(Cygwin)

Installation
------------

The quick way:

.. code-block:: bash

    $ pip install pywbemtools

For more details, see the `Installation section`_ in the pywbemcools
documentation.

.. _Installation section: https://pywbemtools.readthedocs.io/en/stable/introduction.html#installation

Documentation
-------------

The latest pywbemtools documentation is available on ReadTheDocs:

* `Documentation for latest released version`_

.. _Documentation for latest released version: https://pywbemtools.readthedocs.io/en/stable/

* `Documentation for latest unreleased development version`_

.. _Documentation for latest unreleased development version: https://pywbemtools.readthedocs.io/en/latest/

The detailed change history for the latest released version in the
`Change log section`_.

.. _Change log section: https://pywbemtools.readthedocs.io/en/stable/changes.html


Quickstart
----------

pywbemcli
^^^^^^^^^

The following are examples of pywbemcli commands:

All commands within pywbemcli include help as the --help or -h option::

    pywbemcli --help

Executing the EnumerateClasses CIM-XML operation:

.. code-block:: text

    $ pywbemcli -s http://localhost class get CIM_ManagedElement

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

Executing the CIM-XML EnumerateInstance operation with ``-o`` option that
returns instance names:

.. code-block:: text

    $pywbemcli -s http://localhost instance enumerate PyWBEM_Person -o

    root/cimv2:PyWBEM_Person.Name="Alice",CreationClassName="PyWBEM_Person"
    root/cimv2:PyWBEM_Person.Name="Bob",CreationClassName="PyWBEM_Person"
    root/cimv2:PyWBEM_Person.Name="Charlie",CreationClassName="PyWBEM_Person"

Executing the CIM-XML GetInstance operation that requests a single instance
from the WBEM server with the instance name shown in the example:

.. code-block:: text

    $ pywbemcli -s https://localhost instance get PyWBEM_Person.CreationClassName=\"PyWBEM_Person\",Name=\"Alice\"

    instance of PyWBEM_Person {
       ...
       Secretary = NULL;
       Title = NULL;
       CreationClassName = "PyWBEM_Person";
       Name = "Alice";
    };

or using the pywbemcli interactive option (``-i`` or ``--interactive``) where
pywbemcli presents a list of instances on the wbem server from the class name:

.. code-block:: text

    $ pywbemcli -s https://localhost instance get PyWBEM_Person -i

    instance of PyWBEM_Person {
       ...
       Secretary = NULL;
       Title = NULL;
       CreationClassName = "PyWBEM_Person";
       Name = "Alice";
    };
                 <<< pywbemcli responds with:
    Pick Instance name to process
    0: //leonard/root/cimv2:PyWBEM_Person.Name="Alice",CreationClassName="PyWBEM_Person"
    1: //leonard/root/cimv2:PyWBEM_Person.Name="Bob",CreationClassName="PyWBEM_Person"
    2: //leonard/root/cimv2:PyWBEM_Person.Name="Charlie",CreationClassName="PyWBEM_Person"
    Input integer between 0 and 2 or Ctrl-C to exit selection:
                 <<< user responds with >> 0

    instance of PyWBEM_Person {
       ...
       Secretary = NULL;
       Title = NULL;
       CreationClassName = "PyWBEM_Person";
       Name = "Alice";
    };

There are alternate output formats for those subcommands that output CIM objects. Thus,
``instance enumerate <classname>`` can produce a table output where the columns are
the properties by setting the general option ``-o table``. The following is an
example (The instances of CIM_Foo only have two properties):

.. code-block:: text

    $ pywbemcli -N mocsvrassoc -o table -m tests/unit/simple_mock_model.mof instance enumerate CIM_Foo
    Instances: CIM_Foo
    +--------------+---------------+
    | InstanceID   | IntegerProp   |
    |--------------+---------------|
    | "CIM_Foo1"   | 1             |
    | "CIM_Foo2"   | 2             |
    | "CIM_Foo3"   |               |
    +--------------+---------------+

Instance associators the (CIM-XML Associators operation) can be accessed as follows:

.. code-block:: text

    $ pywbemcli> instance associators TST_Person -i
    Pick Instance name to process
    0: root/cimv2:TST_Person.name="Mike"
    1: root/cimv2:TST_Person.name="Saara"
    2: root/cimv2:TST_Person.name="Sofi"
    3: root/cimv2:TST_Person.name="Gabi"
    ...
    Input integer between 0 and 7 or Ctrl-C to exit selection: 0   << user responds 0

    instance of TST_Person {
       name = "Sofi";
    };

    instance of TST_Person {
       name = "Gabi";
    };

    instance of TST_FamilyCollection {
       name = "Family2";
    };

Other operations against WBEM servers include getting information on namespaces,
the interop namespace, and WBEM server brand informaton:

.. code-block:: text

    $ pywbemcli -s https://localhost server interop

    Server Interop Namespace:
    Namespace Name
    ----------------
    root/PG_InterOp

Or to view registered profiles:

.. code-block:: text

    $ pywbemcli -s http://localhost -u kschopmeyer -p test8play server profiles --organization DMTF
      Advertised management profiles:
    +----------------+----------------------+-----------+
    | Organization   | Registered Name      | Version   |
    |----------------+----------------------+-----------|
    | DMTF           | CPU                  | 1.0.0     |
    | DMTF           | Computer System      | 1.0.0     |
    | DMTF           | Ethernet Port        | 1.0.0     |
    | DMTF           | Fan                  | 1.0.0     |
    | DMTF           | Indications          | 1.1.0     |
    | DMTF           | Profile Registration | 1.0.0     |
    +----------------+----------------------+-----------+


Pywbemcli can also be executed in the interactive (REPL) mode by executing it
without entering a command or by using the command ``repl``. In this mode
the command line prompt is ``pywbemcli>``, the WBEM server connection is
maintained between commands and the general options apply to all commands
executed:

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

There are several commands in different command groups to help locating information on the WBEM
server including `class find`, `instance count`, and `class tree`.

For example `class find` finds classes that start with `CIM_` across
multiple namespaces.

.. code-block:: text

    $ pywbemcli -m tests/unit/simple_mock_model.mof class find CIM_

      root/cimv2:CIM_Foo
      root/cimv2:CIM_Foo_sub
      root/cimv2:CIM_Foo_sub2
      root/cimv2:CIM_Foo_sub_sub

The command `class tree` produces an ASCII tree output of the hiearchy of
classes:

.. code-block:: text

    $ pywbemcli -m tests/unit/simple_mock_model.mof class tree
    root
     +-- CIM_Foo
         +-- CIM_Foo_sub2
         +-- CIM_Foo_sub
             +-- CIM_Foo_sub_sub

Pywbemcli can maintain a persistent file of connections that can be accessed by
name. The following example shows creation of a new named server definition. The
first command creates a new connection in the connectionfile. The second
command lists the connections in the connection file, and thethird executes
`class enumerate -o` on the named server:

.. code-block:: text

    $ pywbemcli -m tests/unit/simple_mock_model.mof -N mocksvr1 connection save
    $ pywbemcli connection list
    WBEMServer Connections:
    +----------+--------------+-------------+--------+------------+-----------+------------+------------+-----------+-------+
    | name     | server uri   | namespace   | user   | password   |   timeout | noverify   | certfile   | keyfile   | log   |
    |----------+--------------+-------------+--------+------------+-----------+------------+------------+-----------+-------|
    | mocksvr1 |              | root/cimv2  |        |            |        30 | False      |            |           |       |
    +----------+--------------+-------------+--------+------------+-----------+------------+------------+-----------+-------+
    $ pywbemcli -N mocksvr1 class enumerate -o

    CIM_Foo


Project Planning
----------------

For each upcoming release, the bugs and feature requests that are planned to
be addressed in that release are listed in the
`issue tracker <https://github.com/pywbem/pywbemtools/issues>`_
with an according milestone set that identifies the target release.
The due date on the milestone definition is the planned release date.
There is usually also an issue that sets out the major goals for an upcoming
release.


Contributing
------------

For information on how to contribute to this project, see
`Development documentation`_.

.. _Development documentation: https://github.com/pywbem/pywbemtools/blob/master/DEVELOP.md


License
-------

The pywbemtools package is licensed under the `Apache 2.0 License`_.

.. _Apache 2.0 License: https://github.com/pywbem/pywbemtools/tree/master/LICENSE.txt
