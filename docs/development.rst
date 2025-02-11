
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
       $ tox -e py38                      # Run tests on Python 3.8

.. _`Disabling the spinner when debugging`:

Disabling the spinner when debugging
------------------------------------

Subcommands normally display a spinner (a character-based spinning wheel)
while waiting for completion.

For debugging, it is useful to disable that spinner. This can be done by
setting the ``PYWBEM_SPINNER`` environment variable to 'false', '0', or the
empty string. For example::

    $ export PYWBEM_SPINNER=false


    Git workflow
    ------------

    * Long-lived branches:
      - `master` - for next functional version
      - `stable_M.N` - for fix stream of released version `M.N`.
    * We use topic branches for everything!
      - Based upon the intended long-lived branch, if no dependencies
      - Based upon an earlier topic branch, in case of dependencies
      - It is valid to rebase topic branches and force-push them.
    * We use pull requests to review the branches.
      - Use the correct long-lived branch (e.g. `master` or `stable_0.8`) as a
        merge target!
      - Review happens as comments on the pull requests.
      - At least two +1 are required for merging.
    * GitHub meanwhile offers different ways to merge pull requests. We merge pull
      requests by creating merge commits, so the single commits of a topic branch
      remain unchanged, and we see the title line of the pull request in the merge
      commit message, which is often the only place that tells the issue that was
      fixed.

    Releasing a version
    -------------------

    This section describes how to release a version of pywbemtools to PyPI.

    It covers all variants of versions that can be released:

    * Releasing a new major version (Mnew.0.0) based on the master branch
    * Releasing a new minor version (M.Nnew.0) based on the master branch
    * Releasing a new update version (M.N.Unew) based on the stable branch of its
      minor version

    The description assumes that the `pywbem/pywbemtools` repo is cloned locally in
    a directory named `pywbemtools`. Its upstream repo is assumed to have the
    remote name `origin`.

    Any commands in the following steps are executed in the main directory of your
    local clone of the `pywbem/pywbemtools` Git repo.

    1.  Set shell variables for the version that is being released and the branch
        it is based on:

        * ``MNU`` - Full version M.N.U that is being released
        * ``MN`` - Major and minor version M.N of that full version
        * ``BRANCH`` - Name of the branch the version that is being released is
          based on

        When releasing a new major version (e.g. ``1.0.0``) based on the master
        branch:

            MNU=1.0.0
            MN=1.0
            BRANCH=master

        When releasing a new minor version (e.g. ``0.9.0``) based on the master
        branch:

            MNU=0.9.0
            MN=0.9
            BRANCH=master

        When releasing a new update version (e.g. ``0.8.1``) based on the stable
        branch of its minor version:

            MNU=0.8.1
            MN=0.8
            BRANCH=stable_${MN}

    2.  Create a topic branch for the version that is being released:

            git checkout ${BRANCH}
            git pull
            git checkout -b release_${MNU}

    3.  Update the change log:

        First make a dry-run to print the change log as it would be:

            towncrier build --draft

        If you are satisfied with the change log, update the change log:

            towncrier build --yes

        This will update the change log file ``docs/changes.rst`` with the
        information from the change fragment files in the ``changes`` directory, and
        will delete these change fragment files.

    4.  Run the Safety tool:

        .. code-block:: sh

            RUN_TYPE=release make safety

        When releasing a version, the safety run for all dependencies will fail
        if there are any safety issues reported. In normal and scheduled runs,
        safety issues reported for all dependencies will be ignored.

        If the safety run fails, you need to fix the safety issues that are
        reported.

    5.  Commit your changes and push the topic branch to the remote repo:

            git commit -asm "Release ${MNU}"
            git push --set-upstream origin release_${MNU}

    6.  On GitHub, create a Pull Request for branch ``release_M.N.U``. This will
        trigger the CI runs.

        Important: When creating Pull Requests, GitHub by default targets the
        ``master`` branch. When releasing based on a stable branch, you need to
        change the target branch of the Pull Request to ``stable_M.N``.

        Set the milestone of that PR to version M.N.U.

        The PR creation will cause the "test" workflow to run. That workflow runs
        tests for all defined environments, since it discovers by the branch name
        that this is a PR for a release.

    7.  On GitHub, close milestone ``M.N.U``.

        Verify that the milestone has no open items anymore. If it does have open
        items, investigate why and fix.

    8.  On GitHub, once the checks for the Pull Request for branch ``start_M.N.U``
        have succeeded, merge the Pull Request (no review is needed). This
        automatically deletes the branch on GitHub.

        If the PR did not succeed, fix the issues.

    9.  Publish the package

            git checkout ${BRANCH}
            git pull
            git branch -D release_${MNU}
            git branch -D -r origin/release_${MNU}
            git tag -f ${MNU}
            git push -f --tags

        Pushing the new tag will cause the "publish" workflow to run. That workflow
        builds the package, publishes it on PyPI, creates a release for it on Github,
        and finally creates a new stable branch on Github if the master branch was
        released.

    10. Verify the publishing

        Wait for the "publish" workflow for the new release to have completed:
        https://github.com/pywbem/pywbemtools/actions/workflows/publish.yml

        Then, perform the following verifications:

        * Verify that the new version is available on PyPI at
          https://pypi.python.org/pypi/pywbemtools/

        * Verify that the new version has a release on Github at
          https://github.com/pywbem/pywbemtools/releases

        * Verify that the new version has documentation on ReadTheDocs at
          https://pywbemtools.readthedocs.io/en/stable/changes.html

          The new version M.N.U should be automatically active on ReadTheDocs,
          causing the documentation for the new version to be automatically built
          and published.

          If you cannot see the new version after some minutes, log in to
          https://readthedocs.org/projects/pywbemtools/versions/ and activate
          the new version.


    Starting a new version
    ----------------------

    This section shows the steps for starting development of a new version of
    pywbemtools.

    This section covers all variants of new versions:

    * Starting a new major version (Mnew.0.0) based on the master branch
    * Starting a new minor version (M.Nnew.0) based on the master branch
    * Starting a new update version (M.N.Unew) based on the stable branch of its
      minor version

    The description assumes that the `pywbem/pywbemtools` repo is cloned locally in
    a directory named `pywbemtools`. Its upstream repo is assumed to have the
    remote name `origin`.

    Any commands in the following steps are executed in the main directory of your
    local clone of the `pywbem/pywbemtools` Git repo.

    1.  Set shell variables for the version that is being started and the branch it
        is based on:

        * ``MNU`` - Full version M.N.U that is being started
        * ``MN`` - Major and minor version M.N of that full version
        * ``BRANCH`` -  Name of the branch the version that is being started is
          based on

        When starting a new major version (e.g. ``1.0.0``) based on the master
        branch:

            MNU=1.0.0
            MN=1.0
            BRANCH=master

        When starting a new minor version (e.g. ``0.9.0``) based on the master
        branch:

            MNU=0.9.0
            MN=0.9
            BRANCH=master

        When starting a new minor version (e.g. ``0.8.1``) based on the stable
        branch of its minor version:

            MNU=0.8.1
            MN=0.8
            BRANCH=stable_${MN}

    2.  Create a topic branch for the version that is being started:

            git checkout ${BRANCH}
            git pull
            git checkout -b start_${MNU}

    3.  Commit your changes and push them to the remote repo:

            git commit -asm "Start ${MNU}"
            git push --set-upstream origin start_${MNU}

    4.  On GitHub, create a Pull Request for branch ``start_M.N.U``.

        Important: When creating Pull Requests, GitHub by default targets the
        ``master`` branch. When starting a version based on a stable branch, you
        need to change the target branch of the Pull Request to ``stable_M.N``.

    5.  On GitHub, create a milestone for the new version ``M.N.U``.

        You can create a milestone in GitHub via Issues -> Milestones -> New
        Milestone.

    6.  On GitHub, go through all open issues and pull requests that still have
        milestones for previous releases set, and either set them to the new
        milestone, or to have no milestone.

    7.  On GitHub, once the checks for the Pull Request for branch ``start_M.N.U``
        have succeeded, merge the Pull Request (no review is needed). This
        automatically deletes the branch on GitHub.

    8.  Add release start tag and clean up the local repo:

        Note: An initial tag is necessary because the automatic version calculation
        done by setuptools-scm uses the most recent tag in the commit history and
        increases the least significant part of the version by one, without
        providing any controls to change that behavior.

        .. code-block:: sh

            git checkout ${BRANCH}
            git pull
            git branch -D start_${MNU}
            git branch -D -r origin/start_${MNU}
            git tag -f ${MNU}a0
            git push -f --tags


.. _`Git workflow`:

Git workflow
------------

* Long-lived branches:

  - ``master`` - for next functional version
  - ``stable_M.N`` - for fix stream of released version ``M.N``.

* We use topic branches for everything!

  - Based upon the intended long-lived branch, if no dependencies
  - Based upon an earlier topic branch, in case of dependencies
  - It is valid to rebase topic branches and force-push them.

* We use pull requests to review the branches.

  - Use the correct long-lived branch (e.g. ``master`` or ``stable_0.8``) as a
    merge target!
  - Review happens as comments on the pull requests.
  - At least two +1 are required for merging.

* GitHub meanwhile offers different ways to merge pull requests. We merge pull
  requests by creating merge commits, so the single commits of a topic branch
  remain unchanged, and we see the title line of the pull request in the merge
  commit message, which is often the only place that tells the issue that was
  fixed.


.. _`Releasing a version`:

Releasing a version
-------------------

This section describes how to release a version of pywbemtools to PyPI.

It covers all variants of versions that can be released:

* Releasing a new major version (Mnew.0.0) based on the master branch
* Releasing a new minor version (M.Nnew.0) based on the master branch
* Releasing a new update version (M.N.Unew) based on the stable branch of its
  minor version

The description assumes that the ``pywbem/pywbemtools`` repo is cloned locally in
a directory named ``pywbemtools``. Its upstream repo is assumed to have the
remote name ``origin``.

Any commands in the following steps are executed in the main directory of your
local clone of the ``pywbem/pywbemtools`` Git repo.

1.  Set shell variables for the version that is being released and the branch
    it is based on:

    * ``MNU`` - Full version M.N.U that is being released
    * ``MN`` - Major and minor version M.N of that full version
    * ``BRANCH`` - Name of the branch the version that is being released is
      based on

    When releasing a new major version (e.g. ``1.0.0``) based on the master
    branch:

    .. code-block:: sh

        MNU=1.0.0
        MN=1.0
        BRANCH=master

    When releasing a new minor version (e.g. ``0.9.0``) based on the master
    branch:

    .. code-block:: sh

        MNU=0.9.0
        MN=0.9
        BRANCH=master

    When releasing a new update version (e.g. ``0.8.1``) based on the stable
    branch of its minor version:

    .. code-block:: sh

        MNU=0.8.1
        MN=0.8
        BRANCH=stable_${MN}

2.  Create a topic branch for the version that is being released:

    .. code-block:: sh

        git checkout ${BRANCH}
        git pull
        git checkout -b release_${MNU}

3.  Update the change log:

    First make a dry-run to print the change log as it would be:

    .. code-block:: sh

        towncrier build --draft

    If you are satisfied with the change log, update the change log:

    .. code-block:: sh

        towncrier build --yes

    This will update the change log file ``docs/changes.rst`` with the
    information from the change fragment files in the ``changes`` directory, and
    will delete these change fragment files.

4.  Run the Safety tool:

    .. code-block:: sh

        RUN_TYPE=release make safety

    When releasing a version, the safety run for all dependencies will fail
    if there are any safety issues reported. In normal and scheduled runs,
    safety issues reported for all dependencies will be ignored.

    If the safety run fails, you need to fix the safety issues that are
    reported.

5.  Commit your changes and push the topic branch to the remote repo:

    .. code-block:: sh

        git commit -asm "Release ${MNU}"
        git push --set-upstream origin release_${MNU}

6.  On GitHub, create a Pull Request for branch ``release_M.N.U``. This will
    trigger the CI runs.

    Important: When creating Pull Requests, GitHub by default targets the
    ``master`` branch. When releasing based on a stable branch, you need to
    change the target branch of the Pull Request to ``stable_M.N``.

    Set the milestone of that PR to version M.N.U.

    The PR creation will cause the "test" workflow to run. That workflow runs
    tests for all defined environments, since it discovers by the branch name
    that this is a PR for a release.

7.  On GitHub, close milestone ``M.N.U``.

    Verify that the milestone has no open items anymore. If it does have open
    items, investigate why and fix.

8.  On GitHub, once the checks for the Pull Request for branch ``start_M.N.U``
    have succeeded, merge the Pull Request (no review is needed). This
    automatically deletes the branch on GitHub.

    If the PR did not succeed, fix the issues.

9.  Publish the package

    .. code-block:: sh

        git checkout ${BRANCH}
        git pull
        git branch -D release_${MNU}
        git branch -D -r origin/release_${MNU}
        git tag -f ${MNU}
        git push -f --tags

    Pushing the new tag will cause the "publish" workflow to run. That workflow
    builds the package, publishes it on PyPI, creates a release for it on Github,
    and finally creates a new stable branch on Github if the master branch was
    released.

10. Verify the publishing

    Wait for the "publish" workflow for the new release to have completed:
    https://github.com/pywbem/pywbemtools/actions/workflows/publish.yml

    Then, perform the following verifications:

    * Verify that the new version is available on PyPI at
      https://pypi.python.org/pypi/pywbemtools/

    * Verify that the new version has a release on Github at
      https://github.com/pywbem/pywbemtools/releases

    * Verify that the new version has documentation on ReadTheDocs at
      https://pywbemtools.readthedocs.io/en/stable/changes.html

      The new version M.N.U should be automatically active on ReadTheDocs,
      causing the documentation for the new version to be automatically built
      and published.

      If you cannot see the new version after some minutes, log in to
      https://readthedocs.org/projects/pywbemtools/versions/ and activate
      the new version.


.. _`Starting a new version`:

Starting a new version
----------------------

This section shows the steps for starting development of a new version of
pywbemtools.

This section covers all variants of new versions:

* Starting a new major version (Mnew.0.0) based on the master branch
* Starting a new minor version (M.Nnew.0) based on the master branch
* Starting a new update version (M.N.Unew) based on the stable branch of its
  minor version

The description assumes that the ``pywbem/pywbemtools`` repo is cloned locally in
a directory named ``pywbemtools``. Its upstream repo is assumed to have the
remote name ``origin``.

Any commands in the following steps are executed in the main directory of your
local clone of the ``pywbem/pywbemtools`` Git repo.

1.  Set shell variables for the version that is being started and the branch it
    is based on:

    * ``MNU`` - Full version M.N.U that is being started
    * ``MN`` - Major and minor version M.N of that full version
    * ``BRANCH`` -  Name of the branch the version that is being started is
      based on

    When starting a new major version (e.g. ``1.0.0``) based on the master
    branch:

    .. code-block:: sh

        MNU=1.0.0
        MN=1.0
        BRANCH=master

    When starting a new minor version (e.g. ``0.9.0``) based on the master
    branch:

    .. code-block:: sh

        MNU=0.9.0
        MN=0.9
        BRANCH=master

    When starting a new minor version (e.g. ``0.8.1``) based on the stable
    branch of its minor version:

    .. code-block:: sh

        MNU=0.8.1
        MN=0.8
        BRANCH=stable_${MN}

2.  Create a topic branch for the version that is being started:

    .. code-block:: sh

        git checkout ${BRANCH}
        git pull
        git checkout -b start_${MNU}

3.  Commit your changes and push them to the remote repo:

    .. code-block:: sh

        git commit -asm "Start ${MNU}"
        git push --set-upstream origin start_${MNU}

4.  On GitHub, create a Pull Request for branch ``start_M.N.U``.

    Important: When creating Pull Requests, GitHub by default targets the
    ``master`` branch. When starting a version based on a stable branch, you
    need to change the target branch of the Pull Request to ``stable_M.N``.

5.  On GitHub, create a milestone for the new version ``M.N.U``.

    You can create a milestone in GitHub via Issues -> Milestones -> New
    Milestone.

6.  On GitHub, go through all open issues and pull requests that still have
    milestones for previous releases set, and either set them to the new
    milestone, or to have no milestone.

7.  On GitHub, once the checks for the Pull Request for branch ``start_M.N.U``
    have succeeded, merge the Pull Request (no review is needed). This
    automatically deletes the branch on GitHub.

8.  Add release start tag and clean up the local repo:

    Note: An initial tag is necessary because the automatic version calculation
    done by setuptools-scm uses the most recent tag in the commit history and
    increases the least significant part of the version by one, without
    providing any controls to change that behavior.

    .. code-block:: sh

        git checkout ${BRANCH}
        git pull
        git branch -D start_${MNU}
        git branch -D -r origin/start_${MNU}
        git tag -f ${MNU}a0
        git push -f --tags


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


.. _`Creating and submitting a change to pywbemtools`:

Creating and submitting a change to pywbemtools
-----------------------------------------------

All changes to pywbemtools are made through Github with PRs created on topic
branches and merged with the current master after successful group review.

To make a change, create a topic branch. You can assume that you are the only
one using that branch, so force-pushes to that branch and rebasing that branch
is fine.

When you are ready to push your change, describe the change for users of the
package in a change fragment file. That is a small file in RST format with just
a single change. For more background, read the
[towncrier concept](https://towncrier.readthedocs.io/en/stable/markdown.html)
(which uses Markdown format in that description and calls these files
'news fragment files').

To create a change fragment file, execute:

For changes that have a corresponding issue:

.. code-block:: sh

    towncrier create <issue>.<type>.rst --edit

For changes that have no corresponding issue:

.. code-block:: sh

    towncrier create noissue.<number>.<type>.rst --edit

For changes where you do not want to create a change log entry:

.. code-block:: sh

    towncrier create noissue.<number>.notshown.rst --edit
    # The file content will be ignored - it can also be empty

where:

* ``<issue>`` - The issue number of the issue that is addressed by the change.
  If the change addresses more than one issue, copy the new change fragment file
  after its content has been edited, using the other issue number in the file
  name. It is important that the file content is exactly the same, so that
  towncrier can create a single change log entry from the two (or more) files.

  If the change has no related issue, use the ``noissue.<number>.<type>.rst``
  file name format, where ``<number>`` is any number that results in a file name
  that does not yet exist in the ``changes`` directory.

* ``<type>`` - The type of the change, using one of the following values:

  - ``incompatible`` - An incompatible change. This will show up in the
    "Incompatible Changes" section of the change log. The text should include
    a description of the incompatibility from a user perspective and if
    possible, how to mitigate the change or what replacement functionality
    can be used instead.

  - ``deprecation`` - An externally visible functionality is being deprecated
    in this release.
    This will show up in the "Deprecations" section of the change log.
    The deprecated functionality still works in this release, but may go away
    in a future release. If there is a replacement functionality, the text
    should mention it.

  - ``fix`` - A bug fix in the code, documentation or development environment.
    This will show up in the "Bug fixes" section of the change log.

  - ``feature`` - A feature or enhancement in the code, documentation or
    development environment.
    This will show up in the "Enhancements" section of the change log.

  - ``cleanup`` - A cleanup in the code, documentation or development
    environment, that does not fix a bug and is not an enhanced functionality.
    This will show up in the "Cleanup" section of the change log.

  - ``notshown`` - The change will not be shown in the change log.

This command will create a new change fragment file in the ``changes``
directory and will bring up your editor (usually vim).

If your change does multiple things of different types listed above, create
a separate change fragment file for each type.

If you need to modify an existing change log entry as part of your change,
edit the existing corresponding change fragment file.

Add the new or changed change fragment file(s) to your commit. The test
workflow running on your Pull Request will check whether your change adds or
modifies change fragment files.

You can review how your changes will show up in the final change log for
the upcoming release by running:

.. code-block:: sh

    towncrier build --draft

Always make sure that your pushed branch has either just one commit, or if you
do multiple things, one commit for each logical change. What is not OK is to
submit for review a PR with the multiple commits it took you to get to the final
result for the change.


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
