
.. _`Change log`:

Change log
==========


pywbemtools 0.5.2
-----------------

Released: 2020-06-11

**Bug fixes:**

* Pinned pywbem to <1.0.0 due to the incompatibilities it will introduce.
  Support for working with pywbem 1.0.0 will be added in pywbemtools 0.7.0, and
  will not be rolled back into earlier versions of pywbemtools (see issue #616).


pywbemtools 0.5.1
-----------------

Released: 2020-03-31

**Bug fixes:**

* Fix issue with mixed old and new formats on click.echo statement.
  (See issue #419)

* Fixed missing Python 3.7 in supported environments shown on Pypi.
  (See issue #416)

* Fixed that the 'class find' command showed the --namespace option twice
  (see issue #417)

* Added PyYAML>=5.1 as a prerequisite package for pywbemtools for installation.
  So far, it was pulled in indirectly via pywbem.

* Fixed case sensitive matching of class names in instance modify by
  picking up the fix in pywbem 0.14.6. (See issue #429).

* Increased pywbem minimum version to 0.16.0 to accomodate install issues
  on Python 3.4, and to pick up other fixes.

* Test: Accomodated new formatting of error messages in Click 7.1.1, and
  excluded Click 7.1 due to bug.

* Fixed issue with x509 parameter of WBEMConnection. (See issue #468)

* Test: Fixed dependency to Python development packages on CygWin platform
  in Appveyor CI.

* Pygments 2.4.0 and readme-renderer 25.0 have removed support for Python 3.4
  and have therefore been pinned to below these versions on Python 3.4.

* Corrected issue with use-pull general option that causes issues with using
  the 'either' option with servers that do not have pull. (See issue #530)

* Pinned dparse to <0.5.0 on Python 2.7 due to an issue.

* Fixed issues in README and README_PYPI file (See issue #555)

**Enhancements:**

* Test: Improved assertion messages in tests.

* Output of "pywbemcli server profiles" command is now reliably sorted by
  version in addition to org and name. (See issue #500)

* Added support for a new `--pdb` general option and corresponding
  `PYWBEMCLI_PDB` environment variable that causes the pywbemcli command
  to come up with the pdb debugger before invoking the specified command.
  This is a debug feature that is expected to be used mainly by the
  developers of pywbemcli. (See issue #505)

* Test: Added support for entering the pdb debugger from specific unit testcases
  by setting the condition parameter of the testcase to the string 'pdb'.
  This causes pywbemcli to be invoked with the new --pdb option for that
  testcase. (See issue #505)

* Added Python 3.8 as a supported version.

**Cleanup:**

* Test: Enabled Python warning suppression for PendingDeprecationWarning
  and ResourceWarning (py3 only), and fixed incorrect make variable for that.

* Test: Removed testfixtures from minimum constraints file, as it is not used.

* Test: Increased minimum version of pytest from 3.3.0 to 4.3.1 because
  it fixed an issue that surfaced with pywbem minimum package levels
  on Python 3.7.

* Test: Added missing indirectly referenced prerequisite packages to
  minimum-constraints.txt, for a defined package level when testing with
  PACKAGE_LEVEL=minimum.


pywbemtools 0.5.0
-----------------

Released: 2019-09-29

This is the initial release of pywbemtools.
