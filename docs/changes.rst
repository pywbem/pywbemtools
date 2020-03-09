
.. _`Change log`:

Change log
==========


pywbemtools 0.5.1
-----------------

This version is currently in development and is shown as |version|.

Released: not yet

**Incompatible changes:**

**Deprecations:**

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

**Enhancements:**

* Test: Improved assertion messages in tests.

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

**Known issues:**

* See `list of open issues`_.

.. _`list of open issues`: https://github.com/pywbem/pywbemtools/issues


pywbemtools 0.5.0
-----------------

Released: 2019-09-29

This is the initial release of pywbemtools.
