
Pywbemtools - WBEM command line tools
*************************************

This package contains the following Python based WBEM tools:

* :ref:`pywbemcli <Pywbemcli command>` - a WBEM client CLI tool for interacting
  with WBEM servers to execute both basic CIM/XML requests on the servers and
  higher level requests such as showing namespaces, indication subscriptions,
  profiles, etc.

* :ref:`pywbemlistener <Pywbemlistener command>` - a WBEM CLI tool that runs
  and manages WBEM listeners to receive and display WBEM indications.

CIM/WBEM standards are used for a wide variety of systems management tasks
in the industry including DMTF management standards and the `SNIA`_
Storage Management Initiative Specification (`SMI-S`_).

.. _pywbem package on Pypi: https://pypi.org/project/pywbem/
.. _DMTF: https://www.dmtf.org/
.. _CIM/WBEM standards: https://www.dmtf.org/standards/wbem/
.. _SNIA: https://www.snia.org/
.. _SMI-S: https://www.snia.org/forums/smi/tech_programs/smis_home

Pywbemtools uses the :term:`pywbem` WBEM client infrastructure package.

The pywbemtools github page is: `https://github.com/pywbem/pywbemtools <https://github.com/pywbem/pywbemtools>`_.

.. toctree::
   :maxdepth: 2
   :numbered:
   :caption: Table of Contents:
   :name: mastertoc

   introduction.rst
   pywbemcli/index.rst
   pywbemlistener/index.rst
   settingsandconfiguration.rst
   development.rst
   appendix.rst
   changes.rst
   genindex.rst
.. The genindex.rst and a corresponding file required to include index
