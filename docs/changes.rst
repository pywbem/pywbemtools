
.. _`Change log`:

Change log
==========


pywbemtools 0.6.0
-----------------

This version is currently in development and is shown as |version|.

This version contains all fixes up to pywbemtools 0.5.0.

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

**Enhancements:**

**Cleanup:**

* Test: Enabled Python warning suppression for PendingDeprecationWarning
  and ResourceWarning (py3 only), and fixed incorrect make variable for that.

* Test: Removed testfixtures from minimum constraints file, as it is not used.

* Test: Increased minimum version of pytest from 3.3.0 to 4.3.1 because
  it fixed an issue that surfaced with pywbem minimum package levels
  on Python 3.7.

* Code: refactor code to use only the .format formatter and remove all use
  of the % formatter.

**Known issues:**

* See `list of open issues`_.

.. _`list of open issues`: https://github.com/pywbem/pywbemtools/issues


pywbemtools 0.5.0
-----------------

Released: 2019-09-29

This is the initial release of pywbemtools.
