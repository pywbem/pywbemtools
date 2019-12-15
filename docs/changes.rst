
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

* Added PyYAML>=5.1 as a prerequisite package for pywbemtools for installation.
  So far, it was pulled in indirectly via pywbem.

* Fixed case sensitive matching of class names in instance modify by
  picking up the fix in pywbem 0.14.6. (See issue #429).

* Fixed issue where extra diagnostic information about click was being displayed
  when the general option --verbose was defined.

* Fixed issue with x509 parameter of WBEMConnection. (See issue #468)

**Enhancements:**

* Add capability to reorder commands in the help for each group.  The commands
  in all groups except for the top group (pywbemcli -h) are ordered in the
  help list by their order in their source file. The display of commands in
  the top level group is alphabetical except that connection, help, and repl
  are reordered to the bottom of the list. (See issue #466)

* Define alternatives for creating INSTANCENAME input parameter since the
  original form using, WBEMURI is error prone with quote marks.
  (see issue #390)

* Add prompt-toolkit auto-suggest.  This extends the command completion
  capability in the repl mode (interactive mode) to make suggestions on
  command line input based on the history file.  Usually auto-suggest completion
  will be shown as gray text behind the current input. Auto-suggest is not
  available in command line mode.

* Add ability to filter results of 'class enumerate', 'class find', and
  'instance count' commands for selected class qualifiers.  This ability
  is based on 3 new options for each of the above commands '--association',
  '--indication', and '--experimental' each of which has a corresponding
  'no-...'. The user can filter to find classes with combinations of these
  options returning only classes that meet the option criteria.  Thus,
  '--association' returns classes that are associations and '--no-association'
  returns only classes that are not associations.  See issue # 447

**Cleanup:**

* Test: Enabled Python warning suppression for PendingDeprecationWarning
  and ResourceWarning (py3 only), and fixed incorrect make variable for that.

* Test: Removed testfixtures from minimum constraints file, as it is not used.

* Test: Increased minimum version of pytest from 3.3.0 to 4.3.1 because
  it fixed an issue that surfaced with pywbem minimum package levels
  on Python 3.7.

* Code: refactor code to use only the .format formatter and remove all use
  of the % formatter.

* Test: Added missing indirectly referenced prerequisite packages to
  minimum-constraints.txt, for a defined package level when testing with
  PACKAGE_LEVEL=minimum.

* Clean up test mock files by merging mock_simple_model_ext.mof into
  mock_simple_model.mof

* Changed some tests to account for behavior difference with pywbem 0.15.0
  references and associations with invalid class, role.

* Changed minimun version of pywbem to 0.15.0 because of test differences
  that resulted from differences between pywbem 0.14.6 and 0.15.0. The
  differences are in pywbem_mock where the code was changed to return errors
  for invalid classnames and roles in association and reference operations
  where it previously return empty, ignoring the invalid classname.

**Known issues:**

* See `list of open issues`_.

.. _`list of open issues`: https://github.com/pywbem/pywbemtools/issues


pywbemtools 0.5.0
-----------------

Released: 2019-09-29

This is the initial release of pywbemtools.
