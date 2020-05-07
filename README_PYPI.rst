.. # README file for Pypi

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

Pywbemcli provides access to WBEM servers from the command line.
It provides functionality to:

* Explore the CIM data of WBEM servers. It can manage/inspect the CIM model
  components including CIM classes, CIM instances, and CIM qualifiers and
  execute CIM methods and queries on the WBEM server.

* Execute specific CIM-XML operations on the WBEM server as defined in `DMTF`_
  standard `DSP0200 (CIM Operations over HTTP)`_.

* Inspect and manage WBEM server functionality including:

  * CIM namespaces
  * Advertised WBEM management profiles
  * WBEM server brand and version information

* Capture detailed information on CIM-XML interactions with the WBEM server
  including time statistics and details of data flow.

* Maintain a file with persisted WBEM connection definitions so that pywbemcli
  can access multiple WBEM servers by name.

* Provide both a command line mode and an interactive mode where multiple
  pywbemcli commands can be executed within the context of a WBEM server.

* Use an integrated mock WBEM server to try out commands. The mock server
  can be loaded with CIM objects defined in MOF files or via Python scripts.

Documentation
-------------

For the latest version of pywbemtools released on Pypi:

* `Documentation`_
* `Installation`_
* `Change history`_

Quickstart
----------

All commands within pywbemcli show help with the ``-help`` or ``-h`` options:

.. code-block:: text

    $ pywbemcli --help
    . . .
    $ pywbemcli connection --help
    . . .
    $ pywbemcli connection save --help
    . . .

The following examples build on each other and show a typical sequence of
exploration of a WBEM server. For simplicity, they all operate against the
default namespace of the server, and use a persistent connection definition for
the server:

* Add a persistent connection definition named ``conn1`` for the WBEM server to
  be used, so that the subsequent commands can refer to it:

  .. code-block:: text

      $ pywbemcli -s https://localhost --no-verify -u user -p password connection save conn1

* pywbemcli also supports mocked WBEM servers in memory, that are preloaded
  with CIM objects defined in MOF files. Add a persistent connection definition
  named ``assoc1`` to a mock server using one of the MOF files provided in
  the repo:

  .. code-block:: text

      $ pywbemcli -m tests/unit/simple_assoc_mock_model.mof connection save assoc1

* List the persistent connection definitions:

  .. code-block:: text

      $ pywbemcli connection list
      WBEM server connections(brief): (#: default, *: current)
      name    server             mock-server
      ------  -----------------  --------------------------------------
      assoc1                     tests/unit/simple_assoc_mock_model.mof
      conn1   https://localhost

* List the persistent connection definitions with full information:

  .. code-block:: text

      $ pywbemcli connection list --full
      WBEM server connections(full): (#: default, *: current)
      name    server             namespace    user      timeout  use_pull    verify    certfile    keyfile    mock-server
      ------  -----------------  -----------  ------  ---------  ----------  --------  ----------  ---------  --------------------------------------
      assoc1                     root/cimv2                  30              True                             tests/unit/simple_assoc_mock_model.mof
      conn1   https://localhost  root/cimv2   user           30  True        False

* Show the class tree, using the previously added connection definition ``assoc1``:

  .. code-block:: text

      $ pywbemcli -n assoc1 class tree
      root
       +-- TST_FamilyCollection
       +-- TST_Lineage
       +-- TST_MemberOfFamilyCollection
       +-- TST_Person
           +-- TST_Personsub

* Retrieve a single class from that class tree:

  .. code-block:: text

      $ pywbemcli -n assoc1 class get TST_Person
      class TST_Person {

            [Key ( true ),
             Description ( "This is key prop" )]
         string name;

         string extraProperty = "defaultvalue";

      };

* Enumerate the instances of that class, returning only their instance names
  by use of the ``--no`` option:

  .. code-block:: text

      $ pywbemcli -n assoc1 instance enumerate TST_Person --no
      root/cimv2:TST_Person.name="Gabi"
      root/cimv2:TST_Person.name="Mike"
      root/cimv2:TST_Person.name="Saara"
      root/cimv2:TST_Person.name="Sofi"
      root/cimv2:TST_PersonSub.name="Gabisub"
      root/cimv2:TST_PersonSub.name="Mikesub"
      root/cimv2:TST_PersonSub.name="Saarasub"
      root/cimv2:TST_PersonSub.name="Sofisub"

* Retrieve a single instance using one of these instance names:

  .. code-block:: text

      $ pywbemcli -n assoc1 instance get 'root/cimv2:TST_Person.name="Sofi"'
      instance of TST_Person {
         name = "Sofi";
      };

* The instance to be retrieved can also be selected interactively by use of
  the wildcard instance key ("CLASSNAME.?"):

  .. code-block:: text

      $ pywbemcli -n assoc1 instance get TST_Person.?
      Pick Instance name to process
      0: root/cimv2:TST_Person.name="Saara"
      1: root/cimv2:TST_Person.name="Mike"
      2: root/cimv2:TST_Person.name="Sofi"
      3: root/cimv2:TST_Person.name="Gabi"
      4: root/cimv2:TST_PersonSub.name="Gabisub"
      5: root/cimv2:TST_PersonSub.name="Sofisub"
      6: root/cimv2:TST_PersonSub.name="Mikesub"
      7: root/cimv2:TST_PersonSub.name="Saarasub"
      Input integer between 0 and 7 or Ctrl-C to exit selection: 3
      instance of TST_Person {
         name = "Gabi";
      };

* There are multiple output formats supported. The enumerated instances can for
  example be formatted as a table of properties by use of the ``-o table``
  general option (these instances have only one property 'name'):

  .. code-block:: text

      $ pywbemcli -n assoc1 -o table instance enumerate TST_Person
      Instances: TST_Person
      +------------+
      | name       |
      |------------|
      | "Gabi"     |
      | "Mike"     |
      | "Saara"    |
      | "Sofi"     |
      | "Gabisub"  |
      | "Mikesub"  |
      | "Saarasub" |
      | "Sofisub"  |
      +------------+

* Traverse all associations starting from a specific instance that is selected
  interactively:

  .. code-block:: text

      $ pywbemcli -n assoc1 -o table instance associators TST_Person.?
      Pick Instance name to process
      0: root/cimv2:TST_Person.name="Saara"
      1: root/cimv2:TST_Person.name="Mike"
      2: root/cimv2:TST_Person.name="Sofi"
      3: root/cimv2:TST_Person.name="Gabi"
      4: root/cimv2:TST_PersonSub.name="Gabisub"
      5: root/cimv2:TST_PersonSub.name="Sofisub"
      6: root/cimv2:TST_PersonSub.name="Mikesub"
      7: root/cimv2:TST_PersonSub.name="Saarasub"
      Input integer between 0 and 7 or Ctrl-C to exit selection: 1
      Instances: TST_FamilyCollection
      +-----------+
      | name      |
      |-----------|
      | "Family2" |
      | "Gabi"    |
      | "Sofi"    |
      +-----------+

Other operations against WBEM servers include getting information on namespaces,
the Interop namespace, WBEM server brand information, or the advertised
management profiles:

* Show the Interop namespace of the server:

  .. code-block:: text

      $ pywbemcli -n conn1 server interop
      Server Interop Namespace:
      Namespace Name
      ----------------
      root/PG_InterOp

* List the advertised management profiles:

  .. code-block:: text

      $ pywbemcli -n conn1 server profiles --organization DMTF
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

    $ pywbemcli -n conn1
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


.. _Documentation: https://pywbemtools.readthedocs.io/en/stable/
.. _Installation: https://pywbemtools.readthedocs.io/en/stable/introduction.html#installation
.. _Contributing: https://pywbemtools.readthedocs.io/en/stable/development.html#contributing
.. _Change history: https://pywbemtools.readthedocs.io/en/stable/changes.html
.. _pywbemtools issue tracker: https://github.com/pywbem/pywbemtools/issues
.. _pywbem package on Pypi: https://pypi.org/project/pywbem/
.. _DMTF: https://www.dmtf.org/
.. _CIM/WBEM standards: https://www.dmtf.org/standards/wbem/
.. _DSP0200 (CIM Operations over HTTP): https://www.dmtf.org/sites/default/files/standards/documents/DSP0200_1.4.0.pdf
.. _SNIA: https://www.snia.org/
.. _SMI-S: https://www.snia.org/forums/smi/tech_programs/smis_home
.. _Apache 2.0 License: https://github.com/pywbem/pywbemtools/tree/master/LICENSE.txt
