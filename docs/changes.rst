
.. _`Change log`:

Change log
==========

.. ifconfig:: version.endswith('dev0')

.. # Reenable the following lines when working on a development version:

This version of the documentation is development version |version| and
contains the `master` branch up to this commit:

.. git_changelog::
   :revisions: 1


pywbemcli v0.5.0.dev0
---------------------

Released: Not yet

This is the initial release of pywbemcli command line tool.

Incompatible changes
^^^^^^^^^^^^^^^^^^^^

Enhancements
^^^^^^^^^^^^

* Add input argument to _common.format_table to define sort of the
  rows of the table as a function of the formatting.

Bug fixes
^^^^^^^^^

* Fix issues with the create_instance function. It now processes scalar
  and array properties. Issue # 11
* fix issue with the help_over file format.  It was output as .md file and
  the resulting output could be viewed by only some tools (i.e. github
  messed it up). Changed to display as a .rst file output. (see issue #27gi)

* Fix issues around password so that we get the password from a prompt rather
  than just from the command line. This also adds a form of persistence to
  save info on connections by using the connection group.  It adds several
  subcommands to the connection group to show, list, create, delete, etc.
  connections so the user can maintain a list of WBEM servers that can be easily
  referenced rather than having to type them in.(issue # 6))

* Fix issues with `class find`. Failed when namespace specified with -n,
  did not turn off spinner, double sorted output.

* Fix issue where cmd line log option was not passed to named connections or
  when connection select used.

Build, test, quality
^^^^^^^^^^^^^^^^^^^^

Documentation
^^^^^^^^^^^^^
