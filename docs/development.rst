
.. _`Pywbemtools Development`:

Pywbemtools development
=======================

This section only needs to be read by developers of the pywbemtools package.
People that want to make a fix or develop some extension, and people that
want to test the project are also considered developers for the purpose of
this section.

Generally development users will install pywbemtools by cloning the pywbemtools
GitHub package and using the Make utility to handle the installation
of pywbemtools and its prerequisites. This provides the user with all of the
source of pywbemtools and in addition, the test environment and the documentation
files.


.. _`Repository`:

Repository
----------

The repository for pywbemtools is on GitHub:

https://github.com/pywbem/pywbemtools


.. _`Setting up the development environment`:

Setting up the development environment
--------------------------------------

It is recommended to use Linux as the development environment for pywbemtools.
OS-X should work as well, but Windows requires a number of manual setup steps.

1. Clone the Git repo of this project and switch to its working directory:

   .. code-block:: bash

        $ git clone git@github.com:pywbem/pywbemtools.git
        $ cd pywbemtools

2. It is recommended that you set up a `virtual Python environment`_.
   Have the virtual Python environment active for all remaining steps.

3. Install pywbemtools and its prerequisites for installing and running it
   as described in :ref:`Installation`.
   This will install Python packages into the active Python environment,
   and OS-level packages.

4. Unix-like environments on Windows (such as CygWin, MinGW, Babun, or Gow)
   bring their own Python, so double check that the active Python environment
   is the one you want to use.

5. Install the prerequisites for pywbemtools development.
   This will install Python packages into the active Python environment,
   and OS-level packages:

   .. code-block:: bash

        $ make develop

6. This project uses Make to do things in the currently active Python
   environment. The command:

   .. code-block:: bash

        $ make

   displays a list of valid Make targets and a short description of what each
   target does.

.. _virtual Python environment: https://docs.python-guide.org/en/latest/dev/virtualenvs/


.. _`Building the documentation`:

Building the documentation
--------------------------

The ReadTheDocs (RTD) site is used to publish the documentation for the
pywbemtools package at https://pywbemtools.readthedocs.io/

This page is automatically updated whenever the Git repo for this package
changes the branch from which this documentation is built.

In order to build the documentation locally from the Git work directory,
execute:

::

    $ make builddoc

The top-level document to open with a web browser will be
``build_doc/html/docs/index.html``.


.. _`Testing`:

.. # Keep the tests/README file in sync with this 'Testing' section.

Testing
-------

All of the following `make` commands run the tests in the currently active
Python environment. Depending on how the `pywbemtools` package is installed in
that Python environment, either the `pywbemtools` directory in the main
repository directory is used, or the installed `pywbemtools` package.
The test case files and any utility functions they use are always used from
the `tests` directory in the main repository directory.

The `tests` directory has the following subdirectory structure:

::

    tests
     +-- unit                Unit tests
     |    +-- utils               Utility functions used by unit tests
     +-- manual              Manual tests
     +-- schema              The CIM schema MOF files used by some tests

There are multiple types of tests in pywbemtools:

1. Unit tests and function tests

   Today, the unit tests and function tests are contained in the single
   directory `unit`.

   The distinction between unit tests and function tests as used in pywbemtools is
   that function tests exercise the entire pywbemcli client component or entire
   scripts using the pywbem_mock module and mock CIM model definitions
   to emulate a WBEM server, while unit tests exercise single modules without
   using access to a WBEM server.

   Generally, the function tests are organized by the command group so that
   for example the function tests for the class command group are in the file
   ``test_class_subcmd.py``.

   Tests are run by executing:

   ::

       $ make test

   Test execution can be modified by a number of environment variables, as
   documented in the make help (execute ``make help``).

3. Manual tests

   There are several Python scripts and shell scripts that can be run manually.
   The results need to be validated manually.

   These scripts are in the directory:

   ::

       tests/manual/

   and are executed by simply invoking them from within the main directory
   of the repository, e.g.:

   ::

       tests/manual/test_pegasus.py

   Some of the scripts support a ``--help`` option that informs about their
   usage.

   Some tests depend on the existence of a DMTF Schema defining the classes and
   qualifier declarations in a particular release

4. Running Tox

   To run the unit and function tests in all supported Python environments, the
   Tox tool can be used. It creates the necessary virtual Python environments and
   executes ``make test`` (i.e. the unit and function tests) in each of them.

   For running Tox, it does not matter which Python environment is currently
   active, as long as the Python tox package is installed in it:

   ::

       $ tox                              # Run tests on all supported Python versions
       $ tox -e py27                      # Run tests on Python 2.7


.. _`Disabling the spinner when debugging`:

Disabling the spinner when debugging
------------------------------------

Subcommands normally display a spinner (a character-based spinning wheel)
while waiting for completion.

For debugging, it is useful to disable that spinner. This can be done by
setting the ``PYWBEM_SPINNER`` environment variable to 'false', '0', or the
empty string. For example::

    $ export PYWBEM_SPINNER=false


.. _`Contributing`:

Contributing
------------

Third party contributions to this project are welcome!

In order to contribute, create a `Git pull request`_, considering this:

.. _Git pull request: https://help.github.com/articles/using-pull-requests/

* Test is required.
* Each commit should only contain one "logical" change.
* A "logical" change should be put into one commit, and not split over multiple
  commits.
* Large new features should be split into stages.
* The commit message should not only summarize what you have done, but explain
  why the change is useful.
* The commit message must follow the format explained below.

What comprises a "logical" change is subject to sound judgement. Sometimes, it
makes sense to produce a set of commits for a feature (even if not large).
For example, a first commit may introduce a (presumably) compatible API change
without exploitation of that feature. With only this commit applied, it should
be demonstrable that everything is still working as before. The next commit may
be the exploitation of the feature in other components.

For further discussion of good and bad practices regarding commits, see:

* `OpenStack Git Commit Good Practice`_
* `How to Get Your Change Into the Linux Kernel`_

.. _OpenStack Git Commit Good Practice: https://wiki.openstack.org/wiki/GitCommitMessages
.. _How to Get Your Change Into the Linux Kernel: https://www.kernel.org/doc/Documentation/SubmittingPatches


.. _`Core Development Team`:

Core Development Team
---------------------

Anyone can contribute to pywbemtools via pull requests as described in the previous
section.

The pywbemtools project has a core development team that holds regular web conferences
and that is using Slack for offline communication, on the Slack workspace:
https://pywbem.slack.com.

The web conference and the Slack workspace are by invitation, and if you want
to participate in the core team, please
`open a pywbem issue <https://github.com/pywbem/pywbem/issues>`_ to let us know.
