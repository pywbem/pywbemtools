Releasing PyWBEMTOOLS
=====================

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

3.  Edit the version file:

        vi pywbemtools/_version.py

    and set the ``__version__`` variable to the version that is being released:

        __version__ = 'M.N.U'

4.  Edit the change log:

        vi docs/changes.rst

    and make the following changes in the section of the version that is being
    released:

    * Finalize the version.
    * Change the release date to today's date.
    * Make sure that all changes are described.
    * Make sure the items shown in the change log are relevant for and
      understandable by users.
    * In the "Known issues" list item, remove the link to the issue tracker and
      add text for any known issues you want users to know about.
    * Remove all empty list items.

5.  When releasing based on the master branch, edit the GitHub workflow file
    ``test.yml``:

        vi .github/workflows/test.yml

    and in the ``on`` section, increase the version of the ``stable_*`` branch
    to the new stable branch ``stable_M.N`` created earlier:


        on:
          schedule:
            . . .
          push:
            branches: [ master, stable_M.N ]
          pull_request:
            branches: [ master, stable_M.N ]

6.  Commit your changes and push the topic branch to the remote repo:

        git commit -asm "Release ${MNU}"
        git push --set-upstream origin release_${MNU}

7.  On GitHub, create a Pull Request for branch ``release_M.N.U``. This will
    trigger the CI runs.

    Important: When creating Pull Requests, GitHub by default targets the
    ``master`` branch. When releasing based on a stable branch, you need to
    change the target branch of the Pull Request to ``stable_M.N``.

8.  On GitHub, close milestone ``M.N.U``.

9.  On GitHub, once the checks for the Pull Request for branch ``start_M.N.U``
    have succeeded, merge the Pull Request (no review is needed). This
    automatically deletes the branch on GitHub.

10. Add a new tag for the version that is being released and push it to
    the remote repo. Clean up the local repo:

        git checkout ${BRANCH}
        git pull
        git tag -f ${MNU}
        git push -f --tags
        git branch -D release_${MNU}

11. When releasing based on the master branch, create and push a new stable
    branch for the same minor version:

        git checkout -b stable_${MN}
        git push --set-upstream origin stable_${MN}
        git checkout ${BRANCH}

    Note that no GitHub Pull Request is created for any ``stable_*`` branch.

12. When releasing based on the master branch, activate the new stable branch
    ``stable_M.N`` on ReadTheDocs:

    * Go to https://readthedocs.org/projects/pywbemtools/versions/
      and log in.

    * Activate the new version ``stable_M.N``.

      This triggers a build of that version. Verify that the build succeeds
      and that new version is shown in the version selection popup at
      https://pywbemtools.readthedocs.io/

13. On GitHub, edit the new tag ``M.N.U``, and create a release description on
    it. This will cause it to appear in the Release tab.

    You can see the tags in GitHub via Code -> Releases -> Tags.

14. Upload the package to PyPI:

        make upload

    This will show the package version and will ask for confirmation.

    **Attention!** This only works once for each version. You cannot release
    the same version twice to PyPI.

    Verify that the released version arrived on PyPI at
    https://pypi.python.org/pypi/pywbemtools/


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

3.  Edit the version file:

        vi pywbemtools/_version.py

    and update the version to a draft version of the version that is being
    started:

        __version__ = 'M.N.U.dev1'

4.  Edit the change log:

        vi docs/changes.rst

    and insert the following section before the top-most section:

        pywbemtools M.N.U.dev1
        ----------------------

        This version contains all fixes up to version M.N-1.x.

        Released: not yet

        **Incompatible changes:**

        **Deprecations:**

        **Bug fixes:**

        **Enhancements:**

        **Cleanup:**

        **Known issues:**

        * See `list of open issues`_.

        .. _`list of open issues`: https://github.com/pywbem/pywbemtools/issues

5.  Commit your changes and push them to the remote repo:

        git commit -asm "Start ${MNU}"
        git push --set-upstream origin start_${MNU}

6.  On GitHub, create a Pull Request for branch ``start_M.N.U``.

    Important: When creating Pull Requests, GitHub by default targets the
    ``master`` branch. When starting a version based on a stable branch, you
    need to change the target branch of the Pull Request to ``stable_M.N``.

7.  On GitHub, create a milestone for the new version ``M.N.U``.

    You can create a milestone in GitHub via Issues -> Milestones -> New
    Milestone.

8.  On GitHub, go through all open issues and pull requests that still have
    milestones for previous releases set, and either set them to the new
    milestone, or to have no milestone.

9.  On GitHub, once the checks for the Pull Request for branch ``start_M.N.U``
    have succeeded, merge the Pull Request (no review is needed). This
    automatically deletes the branch on GitHub.

10. Update and clean up the local repo:

        git checkout ${BRANCH}
        git pull
        git branch -D start_${MNU}
