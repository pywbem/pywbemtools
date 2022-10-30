
Pywbemtools - WBEM command line tools
*************************************

This package contains the following Python based WBEM command line tools:

* :ref:`pywbemcli <Pywbemcli command>` - a WBEM client CLI for interacting with
  WBEM servers to execute both basic CIM/XML requests on the servers and also
  higher level requests such as showing namespaces, indication subscriptions,
  profiles, etc.
* :ref:`pywbemlistener <Pywbemlistener command>` - a WBEM CLI tool that runs
  and manages WBEM listeners to receive and display WBEM indications.

WBEM is a standardized approach for systems management defined by the
`DMTF <https://www.dmtf.org>`_ that is used in the industry for a wide variety
of systems management tasks. See
`WBEM Standards <https://www.dmtf.org/standards/wbem>`_ for more information.
An important use of this approach is the
`SMI-S <https://www.snia.org/tech_activities/standards/curr_standards/smi>`_
standard defined by `SNIA <https://www.snia.org>`_ for managing storage.

Pywbemtools is based on the :term:`pywbem` WBEM client infrastructure package.

The pywbemtools github page is: `https://github.com/pywbem/pywbemtools <https://github.com/pywbem/pywbemtools>`_.

.. toctree::
   :maxdepth: 2
   :numbered:
   :caption: Table of Contents:
   :name: mastertoc

   introduction.rst
   pywbemcli/index.rst
   pywbemlistener/index.rst
   development.rst
   appendix.rst
   changes.rst
   genindex.rst
.. The genindex.rst and a corresponding file required to include index
