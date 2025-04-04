# pywbemtools: Python tools for communicating with WBEM servers

[![Version on Pypi](https://img.shields.io/pypi/v/pywbemtools.svg)](https://pypi.python.org/pypi/pywbemtools/)
[![Test status (master)](https://github.com/pywbem/pywbemtools/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/pywbem/pywbemtools/actions/workflows/test.yml?query=branch%3Amaster)
[![Docs status (master)](https://readthedocs.org/projects/pywbemtools/badge/?version=latest)](https://readthedocs.org/projects/pywbemtools/builds/)
[![Test coverage (master)](https://coveralls.io/repos/github/pywbem/pywbemtools/badge.svg?branch=master)](https://coveralls.io/github/pywbem/pywbemtools?branch=master)
[![Supported Python](https://img.shields.io/pypi/pyversions/pywbemtools.svg?color=brightgreen)](https://pypi.python.org/pypi/pywbemtools/)

# Overview

Pywbemtools is a collection of command line tools that communicate with
WBEM servers. The tools are written in pure Python and support Python 3.

Pywbemtools includes the following tools:

- `pywbemcli` - A command line utility that uses the
  [pywbem package on Pypi](https://pypi.org/project/pywbem/) to issue operations
  to a WBEM server using the
  [CIM/WBEM standards](https://www.dmtf.org/standards/wbem/) defined by the
  [DMTF](https://www.dmtf.org/) to perform system management tasks.
- `pywbemlistener` - A command line utility that manages WBEM
  indication listeners running as background processes on the local
  system. These listeners use the
  [pywbem package on Pypi](https://pypi.org/project/pywbem/) to receive
  indications sent by a WBEM server using the
  [CIM/WBEM standards](https://www.dmtf.org/standards/wbem/) defined by the
  [DMTF](https://www.dmtf.org/).

CIM/WBEM standards are used for a wide variety of systems management
tasks in the industry including DMTF management standards and the
[SNIA](https://www.snia.org/) Storage Management Initiative
Specification
([SMI-S](https://www.snia.org/forums/smi/tech_programs/smis_home)).

Pywbemcli provides access to WBEM servers from the command line. It
provides functionality to:

- Explore the CIM data of WBEM servers. It can manage/inspect the CIM
  model components including CIM classes, CIM instances, and CIM
  qualifiers and execute CIM methods and queries on the WBEM server.
- Execute specific CIM-XML operations on the WBEM server as defined in
  [DMTF](https://www.dmtf.org/) standard
  [DSP0200 (CIM Operations over HTTP)](https://www.dmtf.org/sites/default/files/standards/documents/DSP0200_1.4.0.pdf).
- Inspect and manage WBEM server functionality including:
  - CIM namespaces
  - Advertised WBEM management profiles
  - WBEM server brand and version information
- Capture detailed information on CIM-XML interactions with the WBEM
  server including time statistics and details of data flow.
- Maintain a file with persisted WBEM connection definitions so that
  pywbemcli can access multiple WBEM servers by name.
- Provide both a command line mode and an interactive mode where
  multiple pywbemcli commands can be executed within the context of a
  WBEM server.
- Use an integrated mock WBEM server to try out commands. The mock
  server can be loaded with CIM objects defined in MOF files or via
  Python scripts.

Pywbemlistener manages WBEM indication listeners that run on the local
system as background processes. It provides functionality to:

-   Start and stop listeners.
-   List and show details of listeners.
-   Send test indications to listeners.

# Installation

Requirements:

1.  Python 3.8 and higher
2.  Operating Systems: Linux, OS-X, native Windows, UNIX-like
    environments on Windows (e.g. Cygwin)

Installation:

- If not yet available, install the "pipx" command as described in
  https://pipx.pypa.io/stable/installation/.

- Without having any virtual Python environment active, install the CLI
  as follows:

  ``` bash
  $ pipx install pywbemtools
  ```

  That makes the `pywbemcli` and `pywbemlistener` commands available in the PATH,
  without having to activate any virtual Python environment.

For more details, see
[Installation](https://pywbemtools.readthedocs.io/en/stable/introduction.html#installation).

# Documentation and change history

For the latest version of pywbemtools released on Pypi:

- [Documentation](https://pywbemtools.readthedocs.io/en/stable/)
- [Change
  history](https://pywbemtools.readthedocs.io/en/stable/changes.html)

# Quickstart

All commands within any of the pywbemtools commands show help with the
`-help` or `-h` options. For example, for the pywbemcli command:

``` text
$ pywbemcli --help
. . .
$ pywbemcli connection --help
. . .
$ pywbemcli connection save --help
. . .
```

The following examples build on each other and show a typical sequence
of exploration of a WBEM server. For simplicity, they all operate
against the default namespace of the server, and use a persistent
connection definition for the server:

- Add a persistent connection definition named `conn1` for the WBEM
  server to be used, so that the subsequent commands can refer to it:

  ``` text
  $ pywbemcli -s https://localhost --no-verify -u user -p password connection save conn1
  ```

- pywbemcli also supports mocked WBEM servers in memory, that are
  preloaded with CIM objects defined in MOF files. Add a persistent
  connection definition named `assoc1` to a mock server using one of
  the MOF files provided in the repo:

  ``` text
  $ pywbemcli -m tests/unit/simple_assoc_mock_model.mof connection save assoc1
  ```

- List the persistent connection definitions:

  ``` text
  $ pywbemcli connection list
  WBEM server connections(brief): (#: default, *: current)
  name    server             mock-server
  ------  -----------------  --------------------------------------
  assoc1                     tests/unit/simple_assoc_mock_model.mof
  conn1   https://localhost
  ```

- List the persistent connection definitions with full information:

  ``` text
  $ pywbemcli connection list --full
  WBEM server connections(full): (#: default, *: current)
  name    server             namespace    user      timeout  use_pull    verify    certfile    keyfile    mock-server
  ------  -----------------  -----------  ------  ---------  ----------  --------  ----------  ---------  --------------------------------------
  assoc1                     root/cimv2                  30              True                             tests/unit/simple_assoc_mock_model.mof
  conn1   https://localhost  root/cimv2   user           30  True        False
  ```

- Show the class tree, using the previously added connection
  definition `assoc1`:

  ``` text
  $ pywbemcli -n assoc1 class tree
  root
   +-- TST_FamilyCollection
   +-- TST_Lineage
   +-- TST_MemberOfFamilyCollection
   +-- TST_Person
       +-- TST_Personsub
  ```

- Retrieve a single class from that class tree:

  ``` text
  $ pywbemcli -n assoc1 class get TST_Person
  class TST_Person {

        [Key ( true ),
         Description ( "This is key prop" )]
     string name;

     string extraProperty = "defaultvalue";

  };
  ```

- Enumerate the instances of that class, returning only their instance
  names by use of the `--no` option:

  ``` text
  $ pywbemcli -n assoc1 instance enumerate TST_Person --no
  root/cimv2:TST_Person.name="Gabi"
  root/cimv2:TST_Person.name="Mike"
  root/cimv2:TST_Person.name="Saara"
  root/cimv2:TST_Person.name="Sofi"
  root/cimv2:TST_PersonSub.name="Gabisub"
  root/cimv2:TST_PersonSub.name="Mikesub"
  root/cimv2:TST_PersonSub.name="Saarasub"
  root/cimv2:TST_PersonSub.name="Sofisub"
  ```

- Retrieve a single instance using one of these instance names:

  ``` text
  $ pywbemcli -n assoc1 instance get 'root/cimv2:TST_Person.name="Sofi"'
  instance of TST_Person {
     name = "Sofi";
  };
  ```

- The instance to be retrieved can also be selected interactively by
  use of the wildcard instance key (\"CLASSNAME.?\"):

  ``` text
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
  ```

- There are multiple output formats supported. The enumerated
  instances can for example be formatted as a table of properties by
  use of the `-o table` general option (these instances have only one
  property \'name\'):

  ``` text
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
  ```

- Traverse all associations starting from a specific instance that is
  selected interactively:

  ``` text
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
  ```

Other operations against WBEM servers include getting information on
namespaces, the Interop namespace, WBEM server brand information, or the
advertised management profiles:

- Show the Interop namespace of the server:

  ``` text
  $ pywbemcli -n conn1 server interop
  Server Interop Namespace:
  Namespace Name
  ----------------
  root/PG_InterOp
  ```

- List the advertised management profiles:

  ``` text
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
  ```

Pywbemcli can also be executed in the interactive (REPL) mode by
executing it without entering a command or by using the command `repl`.
In this mode the command line prompt is `pywbemcli>`, the WBEM server
connection is maintained between commands and the general options apply
to all commands executed:

``` text
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
```

The pywbemlistener command allows setting up WBEM indication listeners
on the local system. The following example starts a listener for HTTP on
port 25000 and uses pywbemcli to set that server up for sending
indications to the listener:

``` text
# Start OpenPegasus as a Docker container
$ docker create keyporttech/smi-server:0.1.2 --name pegasus
$ docker start pegasus

# Define a pywbemcli named connection for that OpenPegasus
$ pywbemcli -s https://localhost:5989 --no-verify connection save pegasus

# Start a pywbem listener that appends any received indications to a file
$ pywbemlistener start lis1 -s http -p 25000 --indi-file lis1.out
$ pywbemlistener list
+--------+--------+----------+-------+---------------------+
| Name   |   Port | Scheme   |   PID | Created             |
|--------+--------+----------+-------+---------------------|
| lis1   |  25000 | http     |  6662 | 2022-01-02 13:28:04 |
+--------+--------+----------+-------+---------------------+

# Add our pywbem listener as a listener destination to the OpenPegasus server
$ pywbemcli -n pegasus subscription add-destination lis1 -l http://localhost:25000
Added owned destination: Name=pywbemdestination:defaultpywbemcliSubMgr:lis1

$ pywbemcli -n pegasus subscription list-destinations
Indication Destinations: submgr-id=defaultpywbemcliSubMgr, svr-id=https://localhost:5989, type=all
+-------------+------------+--------------------------------+------------------------+---------------+------------+----------------+
| Ownership   | Identity   | Name                           | Destination            |   Persistence |   Protocol |   Subscription |
|             |            | Property                       |                        |          Type |            |          Count |
|-------------+------------+--------------------------------+------------------------+---------------+------------+----------------|
| owned       | lis1       | pywbemdestination:defaultpywbe | http://localhost:25000 |             3 |          2 |              0 |
|             |            | mcliSubMgr:lis1                |                        |               |            |                |
+-------------+------------+--------------------------------+------------------------+---------------+------------+----------------+

# Use pywbemlistener to send a test indication
# Note: This does not utilize the OpenPegasus server but sends it directly to the listener
$ pywbemlistener test lis1
Sending the following test indication:
instance of CIM_AlertIndication {
   IndicationIdentifier = NULL;
   AlertingElementFormat = 2;
   AlertingManagedElement = NULL;
   AlertType = 2;
   Message = "Test message";
   OwningEntity = "TEST";
   PerceivedSeverity = 2;
   ProbableCause = 0;
   SystemName = NULL;
   MessageArguments = { };
   IndicationTime = "20220102134842.761734+000";
   MessageID = "TESTnnnn";
};

Sent test indication #1 to listener lis1 at http://localhost:25000

$ cat lis1.out
2022-01-02 13:48:43.010994+01:00 127.0.0.1 instance of CIM_AlertIndication {    IndicationIdentifier = NULL;    AlertingElementFormat = 2;
  AlertingManagedElement = NULL;    AlertType = 2;    Message = "Test message";    OwningEntity = "TEST";    PerceivedSeverity = 2;
  ProbableCause = 0;    SystemName = NULL;    MessageArguments = { };    IndicationTime = "20220102134842.761734+000";
  MessageID = "TEST0001"; };
```

# Project Planning

For each upcoming release, the bugs and feature requests that are
planned to be addressed in that release are listed in the
[pywbemtools issue tracker](https://github.com/pywbem/pywbemtools/issues) with
an according milestone set that identifies the target release. The due date
on the milestone definition is the planned release date. There is
usually also an issue that sets out the major goals for an upcoming
release.

# Contributing

For information on how to contribute to this project, see
[Contributing](https://pywbemtools.readthedocs.io/en/stable/development.html#contributing).

# License

The pywbemtools package is licensed under the [Apache 2.0
License](https://github.com/pywbem/pywbemtools/tree/master/LICENSE.txt).
