.. # README file for Pypi

Pywbemtools is a collection of command line tools that communicate with WBEM
Servers. The tools are written in pure Python and support Python 2 and Python
3.

Pywbemtools provides a command line tool (pywbemcli) that uses the `pywbem`_
Python WBEM client infrastructure to issue operations to a WBEM server using
the `CIM/WBEM standards`_ defined by the `DMTF`_ to perform system management
tasks.

CIM/WBEM infrastructure is used for a wide variety of systems management tasks
in the industry including DMTF management standards and  the `SNIA`_
Storage Management Initiative Specification `SMI-S`_.

Pywbemcli provides a multilevel command line syntax to communicate with a WBEM
server to:

      * Explore the CIM data of WBEM Server.  It can manage/inspect the CIM
        model components including CIM_Classes, CIM_instances, and CIM
        qualifiers and execute CIM methods and queries on the WBEM server. It
        implements subcommands to execute almost all of the defined DMTF
        CIM/XML operations.

      * Inspect WBEM Server components such as namespaces, registered
        profiles, and other server information.

      * Capture detailed information on the interactions with the WBEM server
        including time statistics.

For more information on pywbemtools see the `pywbemtools readme`_ and the
`pywbemtools documentation`_

.. _pywbemtools readme: https://github.com/pywbem/pywbemtools/blob/stable_0.6/README.rst
.. _pywbemtools documentation: https://pywbemtools.readthedocs.io/en/stable_0.6/

For more information on pywbem, see the `pywbem readme`_, and the
`pywbem documentation`_.

.. _pywbem: https://github.com/pywbem/pywbem/blob/stable_0.14/README.rst
.. _pywbem readme: https://github.com/pywbem/pywbem/blob/stable_0.14/README.rst
.. _pywbem documentation: https://pywbem.readthedocs.io/en/stable_0.14/

.. _CIM/WBEM standards: https://www.dmtf.org/standards/wbem/
.. _DMTF: https://www.dmtf.org/
.. _SNIA: https://www.snia.org/
.. _SMI-S: https://www.snia.org/forums/smi/tech_programs/smis_home
.. _WBEM: https://www.dmtf.org/standards/wbem
