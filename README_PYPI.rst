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

Pywbemcli provides the functionality to :

* Explore the CIM data of WBEM Servers.  It can manage/inspect the CIM
  model components including CIM classes, CIM instances, and CIM
  qualifiers and execute CIM methods and queries on the WBEM server. It
  implements subcommands to execute the CIM-XML operations defined in the
  DMTF specification `CIM Operations Over HTTP(DSP0200)`_

* Inspect/manage WBEM server functionality such as CIM namespaces, WBEM
  registered profiles, and other server information.

* Capture detailed information on interactions with the WBEM server
  including time statistics.

For more information on pywbemtools see the `pywbemtools readme`_ and the
`pywbemtools documentation`_

.. _pywbemtools readme: https://github.com/pywbem/pywbemtools/blob/master/README.rst
.. _pywbemtools documentation: https://pywbemtools.readthedocs.io/en/stable/

For more information on pywbem, see the `pywbem readme`_, and the
`pywbem documentation`_.

.. _pywbem: https://github.com/pywbem/pywbem
.. _pywbem readme: https://github.com/pywbem/pywbem/blob/master/README.rst
.. _pywbem documentation: https://pywbem.readthedocs.io/en/stable/

.. _CIM/WBEM standards: https://www.dmtf.org/standards/wbem/
.. _DMTF: https://www.dmtf.org/
.. _SNIA: https://www.snia.org/
.. _SMI-S: https://www.snia.org/forums/smi/tech_programs/smis_home
.. _WBEM: https://www.dmtf.org/standards/wbem

.. _CIM Operations Over HTTP(DSP0200): https://www.dmtf.org/sites/default/files/standards/documents/DSP0200_1.4.0.pdf

