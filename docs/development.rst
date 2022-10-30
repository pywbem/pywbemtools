
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

.. _chocolatey: https://https://chocolatey.org/
.. _winget: https://learn.microsoft.com/en-us/windows/package-manager/winget/

It is recommended to use Linux as the development environment for pywbemtools.
OS-X should work as well; Windows requires additional manual setup steps.

The pywbemtools development environment is based on a Makefile and therefore
requires the GNUmake utility to execute most of the build steps. For Linux and
the Mac environments, the GNU make utility normally exists but that is not the
case for Windows. GNU make can be installed on native windows from tools such
as `chocolatey`_  or `winget`_ for native windows or window environments such
as cygwin or WSL(Windows Subsystem for Linux) enabled to provide a suitable
GNUmake utility.

1. Clone the Git repo of this project and switch to its working directory:

   .. code-block:: bash

        $ git clone git@github.com:pywbem/pywbemtools.git
        $ cd pywbemtools

2. It is recommended that you set up a Python virtual environment. See section
   :ref:`Using Python virtual environments`.
   Have the virtual Python environment active for all remaining steps.

3. Install pywbemtools and its prerequisites for installing and running it
   as described in :ref:`Installation`.
   This will install Python packages into the active Python environment,
   and OS-level packages.

4. Unix-like environments on Windows (such as CygWin, MinGW, Babun, Gow, or
   WSL(Windows subsystem for Linux)) may bring their own Python, so double
   check that the active Python environment is the one you want to use.

5. Install the prerequisites for pywbemtools development.
   This will install Python packages into the active Python environment,
   and OS-level packages:

   .. code-block:: bash

        $ make develop

6. This project uses make to do things in the currently active Python
   environment. The command:

   .. code-block:: bash

        $ make

   displays a list of valid Make targets for pywbemtools installation and test
   and a short description of what each target does.


.. _`Using Python virtual environments`:

Using Python virtual environments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _virtual Python environment: http://docs.python-guide.org/en/latest/dev/virtualenvs/
.. _virtual Python environment tutorial: https://realpython.com/python-virtual-environments-a-primer/
.. _Python venv: https://docs.python.org/3/library/venv.html

It is beneficial to set up a virtual Python environment for your project,
because that leaves your system Python installation unchanged, it does not
require ``sudo`` rights, and gives you better control about the installed
packages and their versions.  In effect it isolates the environment for your
pywbemtools installation from the rest of the OS environment.

There are a number of different virtual environment tools available for python
depending on your OS and Python including venv, virtualenv, etc.  More information
on virtual environments can be found at sites like `virtual Python environment`_,
`virtual Python environment tutorial`_ or `Python venv`_

The pywbem development team extensively uses virtualenv and virtualenvwrapper in
multiple OS and python version environments.


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
   ``tests\unit\pywbemcli\test_class_subcmd.py``.

   Tests are run by executing:

   ::

       $ make test

   Test execution can be modified by a number of environment variables, as
   documented in the make help (execute ``make help``).

2. Individual test files

   Individual test files in the tests/unit/ environment can be executed by
   executing pytest <test_file_path>. Note that the tests require some
   dependencies to locate the pywbemtools code and to set the terminal width
   for the tests to 120 characters (many command outputs depend on the terminal
   width to format output). Thus the following would execute the tests on the
   class command group contained in ``tests\unit\pywbemcli\test_class_cmds.py``.

   ::

       $ PYTHONPATH=. PYWBEMTOOLS_TERMWIDTH=120 pytest tests/unit/pywbemcli/test_class_cmds.py

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
