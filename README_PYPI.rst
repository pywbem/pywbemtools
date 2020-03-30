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


Installation
------------

Requirements:

1. Python 2.7, 3.4 and higher

2. Operating Systems: Linux, OS-X, native Windows, UNIX-like environments on
   Windows (e.g. Cygwin)

3. On Python 2, the following OS-level packages are needed:

   * On native Windows:

     - ``choco`` - Chocolatey package manager. The pywbemtools package installation
       uses Chocolatey to install OS-level software. See https://chocolatey.org/
       for the installation instructions for Chocolatey.

     - ``wget`` - Download tool. Can be installed with: ``choco install wget``.

   * On Linux, OS-X, UNIX-like environments on Windows (e.g. Cygwin):

     - ``wget`` - Download tool. Can be installed using the OS-level package
       manager for the platform.

Installation:

* On Python 2, install OS-level packages needed by the pywbem package:

  - On native Windows:

    .. code-block:: bash

        > wget -q https://raw.githubusercontent.com/pywbem/pywbem/master/pywbem_os_setup.bat
        > pywbem_os_setup.bat

  - On Linux, OS-X, UNIX-like environments on Windows (e.g. Cygwin):

    .. code-block:: bash

        $ wget -q https://raw.githubusercontent.com/pywbem/pywbem/master/pywbem_os_setup.sh
        $ chmod 755 pywbem_os_setup.sh
        $ ./pywbem_os_setup.sh

    The ``pywbem_os_setup.sh`` script uses sudo internally, so your userid
    needs to have sudo permission.

* Install the pywbemtools Python package:

  .. code-block:: bash

      $ pip install pywbemtools

For more details, including how to install the needed OS-level packages
manually, see `Installation`_.


Documentation and change history
--------------------------------

For the latest version of pywbemtools released on Pypi:

* `Documentation`_
* `Change history`_


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
