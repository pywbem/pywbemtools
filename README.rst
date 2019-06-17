pywbemtools: Python Tools using pywbem API
==========================================

Overview
========

The pywbemtools repository contains user tools that utilize the pywbem client api
to allow a user to inspect and manage WBEM servers.

The current release consists of a single tool, a command line browser
``pywbemcli`` that is capable of inspecting and managing the classes,
instances, and qualifier declarations defined in a WBEMServer and in
addtion, inspecting the WBEMServer characteristics such as namespaces,
profiles, and indication subscriptions.

Installation Requirements
=========================

1. Python 2.7, 3.4 or 3.6.

2. Linux - Including linux tools like make, etc.

Installation
============

The quick way:

.. code-block:: bash

    $ pip install pywbemtools

For more details, see the `Installation section`_ in the documentation.

.. _Installation section: http://pywbemtools.readthedocs.io/en/stable/intro.html#installation

Documentation
=============

The pywbemtools documentation is on the ReadTheDocs(RTD) website.

Preliminary documentation is available at:

* `Documentation for master branch in Git repo`_

.. blah* `Documentation for latest version on Pypi`_

.. _Documentation for master branch in Git repo: http://pywbemtools.readthedocs.io/en/latest/
.. _Documentation for latest version on Pypi: http://pywbemtools.readthedocs.io/en/stable/

Release documentation will be made available when the first release is
completed.

Quickstart
===========

Pywbemcli
^^^^^^^^^


TODO - Add simple examples of pywbemcli

Contributing
============

For information on how to contribute to this project, see the
`Development section`_ in the documentation.

.. _Development section: http://python-zhmcclient.readthedocs.io/en/stable/development.html

License
=======

The pywbemtools package is licensed under the `Apache 2.0 License`_.

.. _Apache 2.0 License: https://github.com/pywbem/pywbemtools/tree/master/LICENSE.txt
