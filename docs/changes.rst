
.. _`Change log`:

Change log
==========

.. ifconfig:: version.endswith('dev0')

.. # Reenable the following lines when working on a development version:

This version of the documentation is development version |version| and
contains the `master` branch up to this commit:

.. git_changelog::
   :revisions: 1


pywbemcli v0.1.0.dev0
---------------------

Released: Not yet

Incompatible changes
^^^^^^^^^^^^^^^^^^^^

Enhancements
^^^^^^^^^^^^

This is the initial release of pywbemcli command line tool.

Bug fixes
^^^^^^^^^

* Fix issues with the create_instance function. It now processes scalar
  and array properties. Issue # 11
* fix issue with the help_over file format.  It was output as .md file and
  the resulting output could be viewed by only some tools (i.e. github
  messed it up). Changed to display as a .rst file output. (see issue #27)


Build, test, quality
^^^^^^^^^^^^^^^^^^^^

Documentation
^^^^^^^^^^^^^



