
.. _`Change log`:

Change log
==========


pywbemtools 1.3.1
-----------------

Released: 2026-01-04

**Bug fixes:**

* Addressed safety issues up to 2025-10-27.

* Fixed new issues reported by Pylint 3.2 and 3.3.

* Test: Fixed the issue that coveralls was not found in the test workflow on MacOS
  with Python 3.9-3.11, by running it without login shell. Added Python 3.11 on
  MacOS to the normal tests.

* For Python 3.6 and 3.7, changed macos-latest back to macos-12 because
  macos-latest got upgraded from 12 to 14 and no longer supports Python 3.6
  and 3.7.

* Test: Changed macos-12 to macos-13 since macos-12 was removed in GitHub Actions.
  Changed ubuntu-latest for Python 3.7 to ubuntu-22.04 because GitHub Actions
  upgraded ubuntu-latest to be ubuntu-24.04.

* Development: Fix issue with minimum-constraints-develop.txt that causing
  failure of make check_reqs. Added two pkgs to minimum-constraints-develop.txt:
  package Levenshtein used by safety and Sphinx and roman-numerals-py used by
  Sphinx. See PR 1453 for details.

* Dev: Circumvented safety issue with import of typer module by pinning typer
  to <0.17.0.

* Fixed that the --nq, --no-qualifiers option was ignored for class operations,
  and qualifiers were always included.

* Test: Fixed new issues raised by pylint 4.0.0.


pywbemtools 1.3.0
-----------------

This version contains all fixes up to version 1.2.1.

Released: 2024-04-20

**Incompatible changes:**

* Dropped support for Python 3.5 (issue #1308)

* Installation of this package using "setup.py" is no longer supported.
  Use "pip" instead.

* Update to pywbemtools version 1.3.0 requires pywbem version >= 1.7.2
  which allows urllib3 version >= 2.0. This may result in issues with SSL because
  urllib3 may require support of TLS protocol version >= 1.2 possibly
  resulting in exceptions such as the following:

    SSLError(1, '[SSL: UNSUPPORTED_PROTOCOL] unsupported protocol . . .)  or
    NotOpenSSLWarning: urllib3 v2.0 only supports OpenSSL 1.1.1+

  See `pywbem troubleshooting documentation. <https://pywbem.readthedocs.io/en/latest/appendix.html#troubleshooting>`_
  for help resolving such issues.

**Bug fixes:**

* Increased pywbem to 1.7.2 to pick up fixes. (issue #1304)

* Addressed safety issues up to 2024-03-25.

* Fixed coveralls issues with KeyError and HTTP 422 Unprocessable Entity.

* Disallow the use of the click_repl version 3.0 because it cannot
  process general options and causes a significant number of CLI tests to
  fail. (issue #1312)

* Circumvented the removal of Python 2.7 from the Github Actions plugin
  setup-python, by using the Docker container python:2.7.18-buster instead.

* Fixed issue with PyYAML 5.4 installation on Python>=3.10 that fails since
  the recent release of Cython 3.

* Correct issue in tab completion for --name argument and option where
  invalid co:nnection file could cause exception.  Changes messages issued
  for error to warning. This eliminates most tests of pywbemlistener but
  only with Python 2.7 and that version of Python is deprecated
  (see issue #1316)

* Test: Circumvented a pip-check-reqs issue by excluding its version 2.5.0.

* Test: cicumvented a test failure with pywbemlistener and python 2.7 by
  disabling a significant number of pywbemlistener tests for python 2.7 and
  modifying the packages to use subprocess32 in place of subprocess with
  python 2.7 in case any tests fail.  (see issue #1327)

* Development: Fixed dependency issue with safety 3.0.0 by pinning it.

* Test: Upgraded GitHub Actions plugins to use node.js 20.

* Test: Fixed issues resulting from removal of support for pytest.warns(None)
  in pytest version 8.

* Test: Fixed invocation of pipdeptree in test workflow to use python -m.

* Fixed pywbemtools install tests to perform the import test in a directory
  where it does not import from the repo main directory. Removed the temporary
  disablement of the install tests that was put in place during development of
  pywbem 1.2.0.

**Enhancements:**

* Added support for Python 3.12.

* Extend tab completion to include connection show, connection delete,
  connection save. (see issue # 1315)

* Changed version of OpenPegasus-wbemserver container for end2end tests
  from version 0.1.2 to 0.1.3.  This version corrects OpenPegasus issues in
  requesting test indications from the wbem server and uses OpenPegasus
  2.14.4 or greater. This change will allow end2end indication testing.

* Fix issue where localhost was always assigned as the pywbemlistener bind
  address. This limited the listener to only receiving indications from the
  same system as the listener itself and only on the local network interface.
  This change was part of extending the options to allow the user to define
  the bind address as part of the start and run commands. (see issue #1296)

* Add pywbemlistener run/start command option --bind-addr to allow the user to
  define a bind address to a listener. This replaces the use of the fixed
  bind-address of localhost. This also changes the default bind address to
  allow receiving indications on any local system network interrface and
  not testing for the indication destination IP address. (see issue #1296)

* Add an option to pywbemlistener to allow testing with a listener on a
  different address/system than the system where pywbemlistener test is being
  executed. This will allow testing across multiple systems.

* Split safety run out of "check" make target ino a separate "safety" make target
  and moved its run to the end of the test workflow.

* Split safety runs into an 'install' and an 'all' run. The install run
  uses a new minimum-constraints-install.txt file that contains just the
  direct and indirect install dependencies and must succeed. The 'all' run
  uses the minimum-constraints.txt file which includes the
  minimum-constraints-install.txt file and that run may fail.
  This reduces the burden of fixing safety issues that affect only development
  packages.

* Dev: Improved release procedure by generalizing the stable branch name
  in the test workflow which allowed removing the step to update it.

* Added support for running 'ruff', a new lint tool.

* Indroduces a troubleshooting section to the pywbemtools documentation.

* Dev: Pinned coverage to <7.0 to speed up installation of development
  environment. coveralls 3.3 also pins coverage to <7.0, so that is not
  a unique restriction of pywbem.

**Cleanup:**

* Change to used safety-policy-file .safety-policy-yml to keep the safety issue
  ignore list in place of the list in the Makefile.

* Add several new safety ignore entries into .safety-policy.yml from the
  new issues that were added to list May 2023.

* Clean up several documentation syntax issues in the pywbemcli documentation.

* New safety issue(GitPython) Sept 2023, check-reqs issue  ruamel-yaml.

* Changed the format of the README and README_PYPI files from RST to Markdown,
  to address formatting issues with badges on the Github site (issue #1376).


pywbemtools 1.2.0
-----------------

This version contains all fixes up to version 1.1.1.

Released: 2023-03-20

**Bug fixes:**

* Fix issue where "instance get" was not properly ordering the columns
  of the table output for commands like "-o table instance get ... --pl p1,p2,p3".
  The table was not being output in the same order as the list of properties in
  the property list option. (see issue #1259)

* Changed the development status of the Python package from "4 - Beta" to
  "5 - Production/Stable". This actually applies since version 1.1.0.
  (issue #1237)
* Fix minor issue where if user input --pl "a, b, c" they would get strange
  error.  Now fails with error stating that space not allowed in property list.

* Fix issue in instance count where error reports CIMError code and not
  the code string. (see #1242)

* Fix issue with invalid --connections-file general option and interactive
  mode. Will abort entering interactive mode if the file does not
  exist. (See issue #1275)

**Enhancements:**

* Added a new make target 'check_reqs' that runs pip-missing-reqs on
  the pywbemtools package itself and on some development commands, and
  added that to the GitHub Actions test workflow. (issue #1255)

* Added displaying of the package dependency tree via pipdeptree to
  the GitHub Actions test workflow. (issue #1256)

* Test: Added new make target 'check_reqs' that uses pip-missing-reqs to check
  for missing dependencies in minimum-constraints.txt.

* Added support for Python 3.11. (issue #1243)

* Increased the minimum version of pywbem to 1.6.0. (issue #1244)

* Add a new command that will display help on subjects that have been defined
  for the command.  This allows defining help for subjects that are not
  specific to a particular command.  This is created specifically to
  provide help for the setup to activate shell tab completion. The initial
  subjects are repl and instancename.

* Add a new command to pywbemcli (docs) that calls the current system default
  web browser to view the pywbemtools public documentation that is in
  ReadTheDocs.

* Added documentation defining activation of tab-complation in shells.
  Tab-completion must be activated by the user before the <TAB> can be used
  in cmd mode to complete the terminal input of command and option names. (see
  issue #1158)

* Add specific tab-completion for the values of the general option --name and
  command arguments/names values that look up connection name to enable
  tab_completion for Click 8 and ignore it for Click 7. Modify general options
  --mock-server, --connection-file, --keyfile, --certfile that are for files to
  use the click.Path type which enables tab-completion. Modify --use-pull
  choice general option to allow the "" choice. so that tab-completion is
  automatically enabled. (See issue #487)

* Modify several pywbemlistener args and options to make enable
  tab-completion. This includes output-format, keyfile, certfile, keyfile,
  scheme, output_format, logdir. (see issue # 1278)

* Add docs command to pywbemlistener. This is the same as the docs command
  in pywbemcli and calls the system default browser to load the pywbemtools
  documentation in ReadTheDocs.

* Add help command to pywbemlistener. This is the same as the help command
  in which defines a set of general subjects for pywbemlistener about which
  help can be requested.  The subjects are generally about tab-completion
  and tab-completion activation.

**Cleanup:**

* Use Ubuntu 20.04 for os target for some github CI tests because python setup
  action does not include Python 3.5 and 3.6 for ubuntu 22.04 (i.e ubuntu-latest as
  of Nov 2022) which causes scheduled test failure.  See issue #1245

* Update to reflect new security issues that were added in Jan 2023. This
  involved GitPython, safety, setuptools certifi,  and future.

* Update for new tests in pylint including 1) use-dict-literal which warns about
  call to dict() when passing keyword arguments vs. using literal (This is a
  speed issue) 2) overlybroad exceptions. Modified definition of
  overlybroadexceptions to prefix names with builtins. 3. Fixed issue found
  by new usless-exception warning. (raise not part of statement)

* Improve the help description for repl.  It was not complete.

* Update Pegasus docker image version to 0.1.2


pywbemtools 1.1.0
-----------------

This version contains all fixes up to version 1.0.1.

Released: 2022-11-08

**Incompatible changes:**

* Dropped support for Python 3.4. (issue #1129)

* Removed deprecated commands (``server namespaces`` and ``server interop``.
  These commands are part of the namespace group ``namespace list`` and
  ``namespace interop``.)

**Bug fixes:**

* Resolved new issues reported by Pylint 2.13. (issue #1164)

* Fix issue where the instance shrub --fullpath option was not displaying the
  paths. (see issue #1180)

* Fixed new formatting issues raised by flake8 5.0.

* Fixed issue where the instance shrub command duplicated the results instances
  tree in cases where there was an inter-namespace association and displayed
  the complete ClassName of the association class rather than just the
  class name. (see issue #1191)

* Fix issue where we were not setting the flag to use the general option
  --max-pull-option when the was defined with an interactive command.  This
  meant that the option was ignored for the current command. (see issue #
  1193).

* Fixed a flake8 AttributeError when using importlib-metadata 5.0.0 on
  Python>=3.7, by pinning importlib-metadata to <5.0.0 on these Python versions.

**Enhancements:**

* Increased minimum version of Click to 8.0.1 on Python >= 3.6 to prepare for
  new features. Adjusted testcases accordingly.

* Extended class/instance enumerate/get/associators/references and qualifier
  enumerate to allow getting the objects from multiple namespaces with a single
  request.  This extends the command option --namespace to allow multiple
  namespaces for these commands using either comma-separated format (ex.
  --namespace root/cimv2,root/cimv3) or multiple definitions of the option (ex.
  --namespace root/cimv2 --namespace root/cimv3) The display of results have
  been extended to include the namespace name for the objects in all of the
  output formats if multiple namespaces are used. As before, the namespaces are
  not shown if only a single or the default namespace is requested.(see issues
  #1058 and #1059)

* Add a new option (--object-order) to class and instance
  enumerate/get/associators/references and qualifier enumerate/get to reorder
  the command results displays by the object name rather than the default of
  namespace name. This allows the user to more easily compare the objects
  themselves in different namespaces. (see issues #1058 and #1059)

* Extended documentation to better document the use and characteristics
  of the general options and the creation of the mock WBEM server
  script (see issue #1190)

**Cleanup:**

* Extend use of general options in interactive mode to allow setting the
  connections-file for an interactive command. (see issue #1037)

* Change DOCKER TEST_SERVER_IMAGE defined in Makefile to use one created from
  OpenPegasus toolset.  See github OpenPegasus/OpenPegasusDocker repository
  for pegasus, pegasus tools, and pegasus docker build tools.  This image
  should be faster and is smaller (lt 400 mb) although still too large. This
  docker file was created using the Docker definition and makefiles in the
  github project OpenPegasus and repository OpenPegasusDocker. It contains
  a build of OpenPegasus on Ubuntu 20.04 platform with the OpenPegasus
  test provider environment installed. The docker server image build was
  tested against the OpenPegasus testsuite.  However, the interop namespace
  was modified to use root/interop in the container. The image contains the
  OpenPegasus components to run the server against a repository based on
  the DMTF schema version 2.41.0.

* Remove deprecated commands ``server namespaces`` and ``server interop``.

* Fixed tests that fail because XML output of classes and qualifier declarations
  return attributes not ordered before python version 3.8. (see issue #1173).

* Modify tests/unit/pywbemcli/wbemserver_mock_class.py to remove the
  CIMInstanceName host lement used in creating a ProfileImplements instance.  That
  element of CIMInstanceName is not allowed on Create instance of association
  classes and as of pywbem 1.5.0 that limitation is enforces.  (see issue
  #1203)

* Modify instance shrub command to only display the classname of the
  association class (i.e. reference_class). Even with multi namespace
  environments the reference class must be in the target namespace.

* Extend the pywbemtools documentation to further explain the mock server
  support, and how to create mock environments using MOF and python scripts
  including many more references back to the pywbem documentation.

* Clarify the usage of the general options in the documentation.
  (see issue #1162)

* Clean up issues in the docs where items in bullet lists do not show the
  bullets Changes rtd-requirements to avoid suspect versions. (see issue #1218)

* Update to requirements files for new Nov 2022 security issues with wheel,
  safety, and py. (see PR # 1627)


pywbemtools 1.0.0
-----------------

This version contains all fixes up to version 0.9.1.

Released: 2022-02-01

**Incompatible changes:**

* The PYWBEMCLI_TERMWIDTH environment variable was renamed to
  PYWBEMTOOLS_TERMWIDTH since it is common to all pywbemtools commands.

* Changed option --default on command ``connection select`` to ``set-default``.
  to be compatible with other commands that touch the default connection
  definition.

* Removed the deprecated option ``--force`` from the ``class delete`` command.
  It had been marked deprecated in pywbemtools version 0.9.0 and was superseded
  by the ``--include-instances`` option which performs exactly the same function.
  (see issue # 1142)

**Bug fixes:**

* Test: Fixed that test_utils.py changed the PYWBEMCLI_TERMWIDTH env var
  for testing purposes without restoring it.

* Fixes issue where the command:
  ``class invokemethod <class> <method> -n <namespace>``
  ignores the command namespace option (-n) and usedsthe default
  namespace. (see issue #990)

* Fix issue where an exception occurs if the user tries to display
  cim instances as a table but the class for the instances returned are not in the
  default namespace and an alternate namespace is defined for the command.
  The function display_cim_objects(...) uses valuemapping_for_property() but
  specifies the default namespace as the target.  (See issue #995)

* Fixed issues raised by new Pylint versions 2.9 and 2.10.

* Fixed an error that resulted in exception traceback when instance commands
  used the instance wildcard (e.g. 'CIM_ManagedSystemElement.?') and the
  enumerate instances operation failed for some reason. (issue #963)

* Fix issue where the general help for '--log' was unclear. (see issue #1025)

* Fixed an error that resulted in exception traceback when instance commands
  used the instance wildcard (e.g. 'CIM_ManagedSystemElement.?') and the
  enumerate instances operation failed for some reason. (issue #963)

* Fix issue with --log general option where the log was left enabled when the
  option was used in interactive mode command; it did not revert to the log
  state before the interactive command. The change caused the log configuration
  to restore to either off if there was no --log option on the subsequent
  command line or to the value defined on the command line.(see issue #1023)

* Disabled new Pylint issue 'consider-using-f-string', since f-strings were
  introduced only in Python 3.6.

* Fixed install error of wrapt 1.13.0 on Python 2.7 on Windows due to lack of
  MS Visual C++ 9.0 on GitHub Actions, by pinning it to <1.13.

* Fix issue with message from _common.py (parse_version_value) that was
  passed to warning_msg but should have been subclass of python warning.
  Changed to use pywbemtools_warn(). (see issue #1041)

* Fixed issue with Sphinx and python 2.7 by changing the sphinx requirements
  in dev-requirements.txt and minimum-constraints.txt. (see issue #1070)

* Modify dev-requirements.txt to limit version of more-itertools to != 8.11.0
  for python < 3.6. (see issue #1077)

* Fixed new issues raised by pylint 2.12.2.

* Fixed issue with instance commands (ex. instance get, references, etc) that
  use the wildcard .? to request that pywbemcli present list of possible
  instances.  It was not handling the non-existence of class in the
  target namespace correctly and would crash because no instances were returned
  get_instanceNames() . Now generates an exception.
  (see issue #1105)

* Fixed issues in "instance count" including unitialized variable and
  correctly finishing scan when errors occur. Adds new option to this command
  to allow user to ignore classes defined with this option (--ignore-class).
  (see issues #1108 and #916 )

* Fixed issue where pywbemcli can get exception if used against server that
  does not support pull operations (see #1118)

**Enhancements:**

* Added a 'pywbemlistener' command for running and managing WBEM listeners.
  (issues #430, #479, #948)

* Implement server schema command that returns information about the schemas
  for each namespace including: 5. the DMTF schemas, 2. schema version, 3. whether
  any classes in the schema/namespace are experimental, and 4) the number of
  classes in this schema, and 5. the DMTF schemas (characters before the `_` in
  the namespace). (see issue #444)

* Remove restrictions on parameter modification of server parameters when the
  --name general option is specified.  Originally the --name server definition
  could not be modified with other general options (ex. --timeout). Those
  restrictions are removed. (see issue #1034)

* Generate exception when general options such as --user, --password, etc.
  that apply only to the server are used with the --mock-server general
  option. (see issue #1035)

* Extend the capability to set the default connection in a connections file to
  the connection save command and a specific command that will set or clear the
  default.  Since the ability to set the default connection was only an
  option in the connection select command it was difficult to find.  This makes
  the functionality more visible and more usable.

* Enhanced test matrix for push-driven runs on GitHub Actions to add
  Python 3.5 on macOS, and removing Python 3.5 minimum on Windows.

* Implement command group subscription that manages the creation, viewing and
  removal of indication subscription on WBEM servers. This creates a new command
  group 'subscription' and new commands for adding, removing, and displaying
  (list) indication destination, filter, and subscription instances on target
  WBEM servers. It includes the code for the new commands, a set of tests
  and the documentation for the new commands. (see issue #4)

* Add new MutuallyExclusiveOption class to pywbemtools/_click_extensions.py to
  allow defining command options as mutually exclusive.  See the class
  for documentation.  Modify pywbemcli.py mutually excluseive options --server,
  --name, and --mock-server to use this class.

* Increased minimum version of pywbem to 1.4.0. (issues #1020, #991, #1124)

* Support for Python 3.10: Added Python 3.10 in GitHub Actions tests, and in
  package metadata.

* Implement an end-end test for the subscription command group.

* Changed output format for table output of instance enumerate --no option to
  show each key as a column in the table so that keys are more readable.

* The '-v' option now displays better information about namespace creation
  and deletion, particularly in mock environments. (related to issue #991)

* Test: Added testcases for namespace creation and deletion. (related to
  issue #991)

* Extended the table view of CIM instances to improve formatting, allow
  hiding columns where all property values are Null (--show-null option)
  and allow the table to be wider than the terminal width if there is
  more information than could be shown in the terminal width.  (see issue
  #1131)

**Cleanup:**

* Prepared the development environment for having more than one pywbemtools
  command. As part of that, moved a number of utility functions from the
  'pywbemtools/pywbemcli' subdirectory to the common 'pywbemtools' directory.

* Moved the environment variable names from being class attributes on the
  PywbemServer class to become constants in the config module. (issue #658)

* Cleanup the test code used as pywbemcli scripts.  Named all of them
  with the last part of the name  _script.py and modified them to use the
  setup initialization with Python 3.6 and greater as well as the old
  script interface.

* Modify pywbemcli.py code that copies command line defined pywbem_server for
  reuse in interactive commands to use WBEMConnection.copy() rather than
  deepcopy(). This includes adding a copy()  method to PywbemServer. This also
  requires that the minimum version of pywbem be set to at least 1.3.0 where
  the copy() method was added to  pywbem (see issue #1030).  This fixes issue
  in python 2.7 with exception and avoids copying the FakedWBEMConnection
  CIM repository.

- Add list of security issues to be ignored by Makefile security test and enable
  failure of build if security test fails. This brings Pywbemtools into line
  with pywbem Makefile.Reordered some of the items in the minumum_constraints.txt file
  to better compare with the pywbem file and also commented out all minimum constraints
  for Jupyter and its dependencies since we have no notebooks in pywbemcli
  today. Modified minimum version of typed-ast, pylint and astrid to match pywbem
  and pass saftey tests.

* Remove the file minimum-constraints-base.txt and put contents into
  minimum-constraints.txt. (see issue #1076)

* Add instance count tests to end-end testing against OpenPegasus.

* Removed the deprecated option ``--force`` from the ``class delete`` command.
  It had been created in pywbemtools version 0.8.0 and was deprecated in
  version 0.90 in favor of the ``--include-instances`` option which performs
  exactly the same function. (see issue # 1142)


pywbemtools 0.9.0
-----------------

This version contains all fixes up to pywbemtools 0.8.1.

Released: 2021-05-03

**Incompatible changes:**

* Modified the --timestats general option from boolean to choice with 3
  choices for when statistics are displayed (after each command or via a
  command). See   issue #588)

**Deprecations:**

* Deprecated the 'server namespaces' and 'server interop' commands. Use the
  new commands 'namespace list' and 'namespace interop', respectively.
  (issue #877)

* The '--force' / '-f' option of the 'class delete' command has been deprecated
  because its name does not sufficiently make it clear that other inhibitors
  than existing instances of the class (such as existing subclasses, or
  referencing classes) will still cause rejection of the command.
  Use the new '--include-instances' option instead. (issue #885)

**Bug fixes:**

* Fixed a ValueError on Windows that was raised when the connections file was
  not on the home drive.

* Limit click package to < 8.0 because of a) incompatibility with python 2.7,
  b) incompatibility between click 8.0 and clicl-repl.
  (see issues #816 and #817)

* Limit mock package to lt 4.0.3 to avoid issue issue that causes test failure.
  (see #822)

* Fix issue caused by mock package version 4.0.3 by creating replacements for
  warnings.warn and warnings.warn_explicit functions  and removing the use of
  the patch decorator in pywbemcli.py before the definition of the cli
  function.  (see issue #822)

* Fixes issue where in pywbemcli the --timeout and --use-pull general
  options were not always correctly included in the new object context in
  interactive mode if they were specified on the interactive mode cmd line.

* Fixed issue in tests with use of stdin and inputting the instance path
  for instance get and instance delete. This was a test setup issue and not
  a code issue. (see issue # 387)

* Mitigated the coveralls HTTP status 422 by pinning coveralls-python to
  <3.0.0.

* Fix issue where documentation index disappeared when we changed the
  documentation theme (see issue #868)

* Test: Fixed behavior of 'pdb' test condition, which is supposed to stop
  in the pdb debugger before executing the command function, but did immediately
  leave the debugger again because of redirections of the standard streams.
  The debugger now properly comes up when 'pdb' is specified as a condition.

* Test: Fixed restoring of environment variables that are modified by testcases,
  and displaying of PYWBEMCLI environment variables during testing in verbose
  mode.

* Change MOFCompiler.add_mof/remove_mof() to only display exceptions received
  if not MOFCompileError since the MOF compiler logs all MOFCompileError
  exceptions. (see issue #395)

**Enhancements:**

* Increased the minimum pywbem version to 1.2.0.

* Add new option to class find command (--summary) to display a summary of
  the counts of classes found instead of the full list of the classes to make
  the command more useful for real servers that may return many classes for
  a class find. (see issue #810)

* Extend the class tree command to optionally provide extra information about
  each class in the tree including 1) the value of the Version qualifier
  if it exists and whether the class is Abstract, an Association, or an
  Indication class. (see. # 817)

* Migrated from Travis and Appveyor to GitHub Actions. This required several
  changes in package dependencies for development.

* The verbose option ('-v' / '--verbose') now also displays the objects that
  are compiled into a mock environment when setting it up.

* Added 'qualifier delete' command. (see #884)

* Enabled the tests for Python 3.4 on Windows again - this required
  some changes in the Makefile and constraints files.

* Added a 'namespace' command group that allows listing, creating and deleting
  CIM namespaces, and showing the Interop namespace. The 'server namespaces'
  and 'server interop' commands that provide a subset of that functionality
  have been deprecated. (issue #877)

* Added commands 'add-mof' and 'remove-mof' for compiling MOF to the 'server'
  command group. (issue #886)

* Test: Added end2end test capability using the OpenPegasus container image
  on Docker Hub.

* Added new command group ('statistics') that contols use of statistics. See
  issue #588)

* Implement command to get statistics from server and present as a table #895)

* Test: Added a unit test module for _utils.py.

* Added an '--include-instances' option to the 'class delete' command that
  replaces the deprecated '--force' / '-f' option. (issue #885)

* Added an '--include-objects' option to the 'namespace delete' command that
  causes the deletion of instances, classes and qualifier types in the targeted
  namespace before the namespace itself is deleted. The objects in the namespace
  are deleted in the correct order of dependencies so that no dangling
  dependencies exist at any point in the operation. (issue #885)

* Added a ''--dry-run' option to the 'class delete' and 'namespace delete'
  commands. If used, it displays the message about each deletion with a
  'Dry run:' prefix and does not perform the actual deletion. (issue #911)

**Cleanup:**

* Cleaned up the circumvention for Click issue #1231 by upgrading the minimum
  Click version to 7.1.1, where possible. The circumvention is still required
  on Python 2.7 and 3.4 on Windows.

* Clarified in the help text of general option '--pdb' that it will be ignored
  in interactive mode but can be specified on each interactive command.

* Test: Added a check that rejects the use of the 'pdb' test condition when the
  test specifies stdin for the test, because the 'pdb' test condition disables
  the stdin/stdout/stderr redirection.


pywbemtools 0.8.0
-----------------

This version contains all fixes up to pywbemtools 0.7.3.

Released: 2020-10-13

**Incompatible changes:**

* Moving the commands "server profiles" and "serve centralinsts" to the
  new group profiles with the commmand names "profile list" and
  "profile centralinsts" added a command group and removed 2 commands
  from the server command group. (See issue #612)

* The `--deprecation-warnings` / `--no-deprecation-warnings` general option
  has been remamed to `--warn` / `--no-warn`, and it now controls the
  display of all Python warnings.

**Bug fixes:**

* Order display of instance names when the .? is used to pick an instance
  name so the same order of instance names is displayed for all versions of
  Python. (See issue #458 and #459)

* Pinned prompt-toolkit to <3.0 on Python 3.8 on Windows to avoid WinError 995.
  (See issue #690)

* Fixed exception when command entered in interactive mode, on Python 2.
  (See issue #224)

* Test: Default connection file does not get restored in some cases during test.
  (See issue #680)

* AssociationShrub produces instancename slightly different table output in
  some cases for pywbem 1 vs previous versions(inclusion of "/:" prefix).
  (see issue #704)

* Test: Fixed attempt in test_class_cmds.py to invoke a non-static method on a
  class object. (see issue #707)

* Fix help message for "--deprecated" to be unicode so python 2.7 help does not
  fail. (see issue #725). This error was added with issue #678

* Upgraded nocasedict and nocaselist packages to pick up fixes.

* Error in test defintion for qualdecl Indication causes failure with pywbem
  i.1.0 where mocker validates qualifiers scopes. (see issue #766)

* Test: Preventive fix for potential issue with virtualenv raising
  AttributeError during installtest on Python 3.4. (see issue #775)

* Test: Added checking for no expected warning. (see issue #774)

* Fixed incorrect property order in instance table output, where key properties
  were not ordered before non-key properties but ordered along with them.
  (see issue #782)

* Docs/Test: Fixed failing install of Jinja2 on Python 3.4 by adding it
  to dev-requirements.txt and pinning it to <2.11 for Python 3.4.

* Test: Aligned qualifier definitions in test MOF with CIM Schema.
  (related to issue #788)

* Upgraded pywbem to 1.1.1 to pick up fixes and enhancements.
  (see issues #749, #183)

**Enhancements:**

* Introduced caching of the mock environment used by connection definitions in
  order to speed up the loading of the connection definition. The mock
  environments are stored in directory ~/.pywbemcli_mockcache and are
  automatically managed. The pywbemcli --verbose general option can be used
  to show messages about the cache management. (See issue #689)

* A new approach for the setup of mock scripts has been introduced: The mock
  script defines a `setup(conn, server, verbose)` function that is called when
  the mock environment is built. It is not called when the mock environment
  is reinstantiated from the cache.
  The old approach with setting global variables CONN, SERVER, VERBOSE is still
  supported, but the mock environment cannot be cached and will be built every
  time when mock scripts with that setup approach are used.
  On Python <3.5, mock scripts with the `setup()` function are rejected, because
  the functionality to import them is not available, and the compile+exec
  approach does not allow executing the setup() function. (See issue #689)

* Modify general help to display the full path of the default connections file.
  (See issue #660)

* Move the commands associated with WBEM management profiles from the server
  group to a new profile group. (See issue #612). See also Incompatible changes.

* Add --deprecated/-no-deprecated as a new qualifier filter for the class
  enumerate, class find, and instance count commands. Extend the behavior so
  that for each of the possible filters it looks for the qualifier on all
  of the elements (property, method, parameter) in addition to the class
  itself.  See issue #678)

* Test: Enabled coveralls to run on all Python versions in the Travis CI,
  resulting in a combined coverage for all Python versions.

* For instance display in table format, added the display of
  the units of properties to the table headers. If a property
  in the class has a PUnit or Units qualifier set, the unit
  is translated to a human readable SI unit using the pywbem.siunit_obj()
  function, and appended to the property name in square brackets.
  (See issue #727)

* Consolidated the warnings control, such that the deprecation messages were
  changed to be issued as Python warnings, and the `--warn` / `--no-warn`
  general options now control the display of all Python warnings. If `--warn`
  is used, all Python warnings are shown once. If `--no-warn` is used (default),
  the `PYTHONWARNINGS` environment variable determines which warnings are shown.
  If that variable is not set, no warnings are shown. (See issue #723)
  Added the 'mock' package and for Python 2.7, the 'funcsigs' package as new
  dependencies.

* Specifying a property list (--pl option) on instance commands with table
  output formats now uses the order of properties as specified in the property
  list in the output table, instead of sorting them. (See issue #702)

* Allow unsetting general options. Originally the general options could be
  either set specifically by defining them on the command line or the
  default would be enabled. However, in interactive mode the need may arise
  to set an option back to its default value (i.e. the equivalent of not
  including it on the command line). This fixes the options so that there is
  an alternative that will will set them to the default value. (see issue
  #350)

* Converted remaining unittest testcases to pytest. (See issue #91)

* Test: When testing with latest package levels, the package versions of
  indirect dependencies are now also upgraded to the latest compatible
  version from Pypi. (see issue #784)

**Cleanup**

* Remove unused NocaseList from __common.py

* Moved the general option --pull_max_cnt to become part of the persistent
  server definition rather than transient.  This means that this
  parameter is part of the data maintained in the server definitionfile and
  applies to just the server defined.  (See issue #694)

* Docs: Improved the description and help texts of the connections file and the
  --connections-file general option in various places, for consistency.
  (Related to issue #708)

* Move code associated with display_cimobjects() to a separate module. This
  is part of creating table representation of classes (See issue #249)

* Resolved remaining Pylint issues and enforced clean pylint checks.
  (See issue #668)

* Renamed the default connections file in the user's home directory from
  `pywbemcli_connection_definitions.yaml` to `.pywbemcli_connections.yaml`,
  because it is really an internal file not meant for being edited.
  An existing file with the old name is migrated automatically.
  (See issue #716)

* Refactor error handling for connections file handlingif there are problems
  with the YAML file or loading the file. Created new exceptions for the
  Connections File and created a unit test and function error test.
  (see issue #661)

* Separate code to execute test files (ex. setup up mock of prompt) from
  the process of executing files defined by the --mock-server general option.
  The new capability is controled by an environment variable
  "PYWBEMCLI_STARTUP_SCRIPT" that is considered intenal to pywbemcli testing.

* Refactor statistics display to present information consistent with the
  display in pywbem. (see issue # 724)

* Refactor connections show command and clean up its documentation.  (see
  issue #732)

* Remove use of pydicti dictionary package in favor of NocaseDict.

* set pylint disable on all uses of pdb.set_trace(). This is an issue between
  the add-on package pdbpp and lint, not pdb.  (see issue # 751)

* Docs: Changed Sphinx theme to sphinx_rtd_theme. (see issue #792)

* Modified the class WbemServerMock in tests/unit/testmock to define a
  WBEM server configuration that includes multiple namespaces, a user and
  an interop namespace to test cross-namespace mock. (see issue #183)


pywbemtools 0.7.0
-----------------

This version contains all fixes up to pywbemtools 0.6.1.

Released: 2020-07-12

**Incompatible changes:**

* The default location for the connections file (pywbemcli_connection_definitions.yaml)
  has been moved from the users current directory to the users home directory.
  A general option (``connections_file``) allows the user to set other directories
  and file names for this file. (See issue #596)

**Deprecations:**

* Deprecated support for Python 2.7 and 3.4, because these Python versions have
  reached their end of life. A future version of pywbemtools will remove support
  for Python 2.7 and 3.4. (see issue #630).

**Bug fixes:**

* Fixed incorrect connection list output in readme files (see issue #593).

* Fixed yaml.RepresenterError during 'connection save' command. This introduced
  a dependency on the yamlloader package. (see issue #603).

* Fixed possible issue where the `connection test` command would fail on a
  server that did not support class operations.  (See issue #606)

* Pinned version of colorama to <0.4.0 for Python <=3.4.

* Adjusted to changes in the pywbem mock support for method providers, in the
  sample method provider simple_mock_invokemethod_pywbem_V1.py. (See issue #646)

* Fix issue with MOF compile in pywbem_mock to account for changes to
  pywbem.FakedWBEMConnection in pywbem 1.0.0.  Because the pywbem
  mocker stopped displaying compile error messages, this change modifies the
  code to display the compile errors as exceptions for pywbem 1.0 and use the
  original display for pre 1.0 pywbem version.  With pywbem 1.0.0 it also
  outputs the compile error message and exception to stderr whereas before
  the compile error text was routed to stdout. (See issue #637)

* Fixed an issue where displaying instances in a table format missed properties
  if the list of instances had different sets of properties. (See issue #650)

* Change the table output for outputformat html to output the title parameter
  as an html caption entity instead of as a paragraph.  This allows html
  tables to be subtabled and also presents the table title better.
  (see issue #721)

**Enhancements:**

* Enabled installation using 'setup.py install' from unpacked source distribution
  archive, and added install tests for various installation methods including
  this one. (see issues #590, #591).

* Enhance output formats to allow an additional format group TEXT with
  a single format ``text``. This format outputs the command result as a
  text string to the console and is use for simple commands like
  ``server interop`` that only output one piece of data. (see issue #594)

* Extended the command `connection test` so that it will also test for existence
  of the DMTF pull operations.  It tests for all of the operations and
  reports success or failure on each operation.

* Added value-mapped strings to properties in instance table output.
  For integer-typed (scalar or array) properties that have a ValueMap qualifier,
  the output of instances in table format now includes the value of the Values
  qualifier in parenthesis, in addition to the integer value. (See issue #634)

* The order of properties when displaying instances in a table format is now
  predictable: First the sorted key properties, then the sorted non-key
  properties. (Part of fix for issue #650)

* Modify connections file location functionality so that the default file
  location is the users home directory. Any other directory and filename can
  be specified using the general option ``connections_file`` which has a
  corresponding environment variable.  (See issue #596)

**Cleanup**

* Adds command to test connection for existence of  the pull operations
  (connection test-pull)

* Refactored display_class_tree() and other functions in _displaytree.py  and
  _cmd_class.py cmd_class_tree function to eliminate boundary conditions, and
  clarify code.

* Extended parameter type testing in class PywbemServer so that all
  constructor parameters are value tested.  This specifically fixes issue
  where we were depending on WBEMConnection to test types of ca_certs
  and invalid data types could get into the connections file. (See issue
  #663).

* Added a function test test module test_misc_errors.py that tests for some
  common exceptions that apply to many commands (ex. connection error).


pywbemtools 0.6.0
-----------------

This version contains all fixes up to pywbemtools 0.5.1.

Released: 2020-04-10

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

* Fixed issue with class find command not returning connection error when
  cannot connect to server.

* Added documentation for the --version general option.

* Increased pywbem minimum version to 0.16.0 to accomodate install issues
  on Python 3.4, and to pick up other fixes.

* Test: Accomodated new formatting of error messages in Click 7.1.1, and
  excluded Click 7.1 due to bug.

* Test: Fixed dependency to Python development packages on CygWin platform
  in Appveyor CI.

* Pygments 2.4.0 and readme-renderer 25.0 have removed support for Python 3.4
  and have therefore been pinned to below these versions on Python 3.4.

* Fix bug where order of commands listed in help output was different for
  different versions of Python. (See issue #510)

* Increased minimum version of pluggy package from 0.12.0 to 0.13.0
  because it failed during loading of pytest plugins on Python 3.8.
  (See issue #494)

* Test: Changed testcases that check the CIM-XML generated with output format
  'xml' to tolerate the different order of XML attributes that happens on
  Python 3.8 (See issue #494)

* Fixed several badges on the README page.

* Remove use of pywbem internal functions from pywbemcli. This removes use of
  NocaseDict, _to_unicode, _ensure_unicode, _format from pywbemcli. (See
  issue #489)

* Corrected issue with use-pull general option that causes issues with using
  the 'either' option with servers that do not have pull. (See issue #530)

* Pinned dparse to <0.5.0 on Python 2.7 due to an issue.

* Test: Fixed incorrect coverage reported at the end of the pytest run,
  by increasing the minimum version of the coverage package to 4.5.2.
  (See issue #547)

* Test: Fixed bug with detection of invalid test validation values, and fixed
  testcases in turn (See issue #553).

* Fixed issues in README and README_PYPI file (See issue #555)

* Improvements and bug fixes in the way the INSTANCENAME parameter of pywbemcli
  commands is processed. (See issue #528)

* Increased minimum versions of some packages used for development to address
  security issues reported by the pyup.io safety tool: twine, bleach, urllib3.

**Enhancements:**

* Promoted development status of pywbemtools from Alpha to Beta.
  (See issue #476)

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
  returns only classes that are not associations.  See issue #447

* Added support for disabling the spinner that is displayed by default during
  any ongoing activities, by setting the env var PYWBEM_SPINNER to 'false',
  '0', or the empty string. This is useful when debugging.  See issue #465.

* Modified the response handling on commands that may return nothing with
  successful response to display a message if the general option --verbose
  is defined and display nothing if --verbose not set.  This includes
  class/instance delete, instance modify and the commands that display
  cim objects. (See issue #123)

* Changed the `--ca-certs` general option to support the changes as of
  pywbem version 1.0.0 (new values 'system' and 'certifi', and default changed
  from a fixed set of directories to 'certifi'). The pywbem version is
  determined at run time and pywbem versions before 1.0.0 are still supported.

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

* Removed usage of the "pbr" package. It was used for automatic versioning
  of the pywbemtools package, but it had too many drawbacks for that small
  benefit (See issue #178):

  - Getting the minor version increased in a development version (instead of
    the patch version) by means of markers in the commit message never worked.
  - The package needed to be tagged twice during the release process.
  - If the last tag was too far in the past of the commit history, the
    shallow git checkout used by Travis failed and its depth needed to be
    adjusted. At some point this defeats the purpose of a shallow checkout.

* Test: Added support for testing on Python 3.8 in Travis, Appveyor and Tox.
  (See issue #494)

* Added support for adjusting the width of any help output to the terminal
  width. The width can be set using the PYWBEMCLI_TERMWIDTH env var.
  (See issues #518 and #542)

* Docs: Increased the width of the help text to 120 (See issue #548).

* Modified the help usage to better reflect the required and optional
  components of the command line. This includes showing the location
  in the cmd line for general options where before it was called
  [COMMAND-OPTIONS] and showing the positioning of both arguments and
  command arguments. (See issue #446)

* Increased minimum version of pywbem to 0.17.0 (See issue #571)

* Add option `--full` to `connection list` to create both a brief table
  output that only has 3 columns (name, server, mock-server) as default but
  when the option is set all of the columns currently in the report. We did
  this because it appears that the most frequent use of this command is to just
  get the name of the various servers defined within an 80 column display.
  This also now shows empty columns where the original report hid any columns
  that were empty. (See issue #556)

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

* Added tests of all command groups and commands for server connection error.

* Removed a circumvention for a pywbem bug related to colons in WBEM URIs
  that was fixed in pywbem 0.13.0. (See issue #131)

* Added the general option `--use-pull` to the the PywbemServer() class so that
  it is persisted in the connection file and to the display of connection
  information (`connection show` and `connection list`). This means that
  `--use-pull` can now be set for a particular server permanently.(See issues
  #529 and #534).

* Added table formatted output for connection show and removed original
  free-form output format. (See issue #572)

* Added documentation on incremental search option to search the command
  history file in interactive mode. (See issue #595)

* Added documentation index entries for commands, command groups, etc. (see
  issue #598)



pywbemtools 0.5.0
-----------------

Released: 2019-09-29

This is the initial release of pywbemtools.
