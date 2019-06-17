.. # README file for Pypi

Pywbemtools is a collection of command line tools  is a WBEM client,
written in pure Python. It supports Python 2 and Python 3.

A WBEM client allows issuing WBEM operations to a WBEM server, using the
`CIM/WBEM standards`_ defined by the DMTF, for the purpose of performing
systems management tasks. A WBEM indication listener is used to wait for
and process notifications emitted by a WBEM server, also for the purpose
of systems management.

In addition to providing a command line interface for the client side DMTF defined
WBEM Operations, pywbem cli provides commands for a number of high level
operations that are useful to developers and users of WBEM Servers such
as the implementation of the SNIA SMI specification.

CIM/WBEM infrastructure is used for a wide variety of systems management
tasks in the industry.

For more information on pywbem, see the `pywbem readme`_, and the
`pywbem documentation`_.

.. _pywbem readme: https://github.com/pywbem/pywbemtools/blob/stable_0.14/README.rst
.. _pywbem documentation: https://pywbemtools.readthedocs.io/en/stable_0.6/
.. _CIM/WBEM standards: https://www.dmtf.org/standards/wbem/
