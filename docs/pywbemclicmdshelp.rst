
.. _`pywbemcli Help Command Details`:

pywbemcli Help Command Details
==============================


This section defines the help output for each pywbemcli command group and subcommand.



The following defines the help output for the `pywbemcli  --help` subcommand


::

    Usage: pywbemcli [GENERAL-OPTIONS] COMMAND [ARGS]...

      Command line browser for WBEM Servers. This cli tool implements the
      CIM/XML client APIs as defined in pywbem to make requests to a WBEM
      server. This browser uses subcommands to:

          * Explore the characteristics of WBEM Servers based on using the
            pywbem client APIs.  It can manage/inspect CIM_Classes and
            CIM_instanceson the server.

          * In addition it can inspect namespaces and other server information
            and inspect and manage WBEM indication subscriptions.

      The options shown above that can also be specified on any of the
      (sub-)commands as well as the command line.

    Options:
      -s, --server TEXT               Hostname or IP address with scheme of the
                                      WBEMServer in  format
                                      [{scheme}://]{host}[:{port}]. Scheme must be
                                      "https" or "http" (Default: "https"). Host
                                      defines a  short or fully qualified DNS
                                      hostname, a literal  IPV4 address (dotted)
                                      or a literal IPV6 address Port (optional)
                                      defines a  WBEM server protocol to be used
                                      (Defaults 5988(HTTP) and  5989 (HTTPS).
                                      (EnvVar: PYWBEMCLI_SERVER).
      -N, --name TEXT                 Optional name for the connection.  If the
                                      name option is not set, the name "default"
                                      is used. If the name option exists and the
                                      server option does not exist pywbemcli
                                      attempts to retrieve the connection
                                      information from persistent storage. If the
                                      server option exists that is used as the
                                      connection
      -d, --default_namespace TEXT    Default Namespace to use in the target
                                      WBEMServer if no namespace is defined in the
                                      subcommand(EnvVar:
                                      PYWBEMCLI_DEFAULT_NAMESPACE). (Default:
                                      root/cimv2).
      -u, --user TEXT                 User name for the WBEM Server connection.
                                      (EnvVar: PYWBEMCLI_USER).
      -p, --password TEXT             Password for the WBEM Server. Will be
                                      requested as part  of initialization if user
                                      name exists and it is not  provided by this
                                      option.(EnvVar: PYWBEMCLI_PASSWORD ).
      -t, --timeout INTEGER RANGE     Operation timeout for the WBEM Server in
                                      seconds. (EnvVar: PYWBEMCLI_TIMEOUT).
                                      Default: 30
      -n, --noverify                  If set, client does not verify server
                                      certificate.
      -c, --certfile TEXT             Server certfile. Ignored if noverify flag
                                      set. (EnvVar: PYWBEMCLI_CERTFILE).
      -k, --keyfile TEXT              Client private key file. (EnvVar:
                                      PYWBEMCLI_KEYFILE).
      --ca_certs TEXT                 File or directory containing certificates
                                      that will be matched against a certificate
                                      received from the WBEM server. Set the --no-
                                      verify-cert option to bypass client
                                      verification of the WBEM server certificate.
                                      (EnvVar: PYWBEMCLI_CA_CERTS).Default:
                                      Searches for matching certificates in the
                                      following system directories: /etc/pki/ca-
                                      trust/extracted/openssl/ca-bundle.trust.crt
                                      /etc/ssl/certs
                                      /etc/ssl/certificates
      -o, --output-format [table|plain|simple|grid|rst|mof|xml|txt|tree]
                                      Output format (Default: simple). pywbemcli
                                      may override the format choice depending on
                                      the operation since not all formats apply to
                                      all output data types. For CIMstructured
                                      objects (ex. CIMInstance), the default
                                      output format is mof
      --use-pull_ops [yes|no|either]  Determines whether the pull operations are
                                      used forthe EnumerateInstances,
                                      associatorinstances,referenceinstances, and
                                      ExecQuery operations. yes means that pull
                                      will be used and if the server does not
                                      support pull, the operation will fail. No
                                      choice forces pywbemcli to try only the
                                      traditional non-pull operations. either
                                      allows pywbem to try both pull and then
                                      traditional operations. This choice is
                                      acomplished by using the Iter... operations
                                      as the underlying pywbem api call.  The
                                      default is either.
      --pull-max-cnt INTEGER          MaxObjectCount of objects to be returned if
                                      pull operations are used. This must be  a
                                      positive non-zero integer. Default is 1000.
      -T, --timestats                 Show time statistics of WBEM server
                                      operations after  each command execution.
      -v, --verbose                   Display extra information about the
                                      processing.
      -m, --mock-server FILENAME      If this option is defined, a mock WBEM
                                      server is constructed as the target WBEM
                                      server and the option value defines a MOF or
                                      Python file to be used to populate the mock
                                      repository. This option may be used multiple
                                      times where each use defines a single file
                                      or file_path.See the pywbemcli documentation
                                      for more information.
      --version                       Show the version of this command and exit.
      -h, --help                      Show this message and exit.

    Commands:
      class       Command group to manage CIM classes.
      connection  Command group to manage WBEM connections.
      help        Show help message for interactive mode.
      instance    Command group to manage CIM instances.
      qualifier   Commands to view QualifierDeclarations.
      repl        Enter interactive (REPL) mode (default).
      server      Command Group for WBEM server operations.


.. _`pywbemcli class --help`:

pywbemcli class --help
----------------------



The following defines the help output for the `pywbemcli class --help` subcommand


::

    Usage: pywbemcli class [COMMAND-OPTIONS] COMMAND [ARGS]...

      Command group to manage CIM classes.

      In addition to the command-specific options shown in this help text, the
      general options (see 'pywbemcli --help') can also be specified before the
      command. These are NOT retained after the command is executed.

    Options:
      -h, --help  Show this message and exit.

    Commands:
      associators   Get the associated classes for CLASSNAME.
      delete        Delete a single class.
      enumerate     Enumerate classes from the WBEM Server.
      find          Find all classes that match CLASSNAME-REGEX.
      get           Get and display a single CIM class.
      invokemethod  Invoke the class method named methodname.
      references    Get the reference classes for CLASSNAME.
      tree          Display CIM class inheritance hierarchy tree.


.. _`pywbemcli class associators --help`:

pywbemcli class associators --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class associators --help` subcommand


::

    Usage: pywbemcli class associators [COMMAND-OPTIONS] CLASSNAME

      Get the associated classes for CLASSNAME.

      Get the classes(or classnames) that are associated with the CLASSNAME
      argument filtered by the --assocclass, --resultclass, --role and
      --resultrole options.

      Results are displayed as defined by the output format global option.

    Options:
      -a, --assocclass <class name>   Filter by the associated class name
                                      provided.
      -c, --resultclass <class name>  Filter by the result class name provided.
      -r, --role <role name>          Filter by the role name provided.
      -R, --resultrole <role name>    Filter by the role name provided.
      --no-qualifiers                 If set, request server to not include
                                      qualifiers in the returned class(s). The
                                      default behavior is to request include
                                      qualifiers in the returned class(s).
      -c, --includeclassorigin        Include classorigin in the result.
      -p, --propertylist <property name>
                                      Define a propertylist for the request. If
                                      not included a Null property list is defined
                                      and the server returns all properties. If
                                      defined as empty string the server returns
                                      no properties. ex: -p propertyname1 -p
                                      propertyname2 or -p
                                      propertyname1,propertyname2
      -o, --names_only                Show only local properties of the class.
      -s, --sort                      Sort into alphabetical order by classname.
      -n, --namespace <name>          Namespace to use for this operation. If
                                      defined that namespace overrides the general
                                      options namespace
      -S, --summary                   Return only summary of objects (count).
      -h, --help                      Show this message and exit.


.. _`pywbemcli class delete --help`:

pywbemcli class delete --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class delete --help` subcommand


::

    Usage: pywbemcli class delete [COMMAND-OPTIONS] CLASSNAME

      Delete a single class.

      Deletes the class defined by CLASSNAME from the WBEM Server.

      If the class has instances, the command is refused unless the --force
      option is used. If --force is used, instances are also deleted.

      WARNING: Removing classes from a WBEM Server can cause damage to the
      server. Use this with caution.  It can impact instance providers and other
      components in the server.

      Some servers may refuse the operation.

    Options:
      -f, --force             Force the delete request to be issued even if there
                              are instances in the server or subclasses to this
                              class. The WBEM Server may still refuse the request.
      -n, --namespace <name>  Namespace to use for this operation. If defined that
                              namespace overrides the general options namespace
      -h, --help              Show this message and exit.


.. _`pywbemcli class enumerate --help`:

pywbemcli class enumerate --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class enumerate --help` subcommand


::

    Usage: pywbemcli class enumerate [COMMAND-OPTIONS] CLASSNAME

      Enumerate classes from the WBEM Server.

      Enumerates the classes (or classnames) from the WBEMServer starting either
      at the top of the class hierarchy or from  the position in the class
      hierarchy defined by `CLASSNAME` argument if provided.

      The output format is defined by the output-format global option.

      The includeclassqualifiers, includeclassorigin options define optional
      information to be included in the output.

      The deepinheritance option defines whether the complete hiearchy is
      retrieved or just the next level in the hiearchy.

    Options:
      -d, --deepinheritance     Return complete subclass hierarchy for this class
                                if set. Otherwise retrieve only the next hierarchy
                                level.
      -l, --localonly           Show only local properties of the class.
      --no-qualifiers           If set, request server to not include qualifiers
                                in the returned class(s). The default behavior is
                                to request include qualifiers in the returned
                                class(s).
      -c, --includeclassorigin  Include classorigin in the result.
      -o, --names_only          Show only local properties of the class.
      -s, --sort                Sort into alphabetical order by classname.
      -n, --namespace <name>    Namespace to use for this operation. If defined
                                that namespace overrides the general options
                                namespace
      -S, --summary             Return only summary of objects (count).
      -h, --help                Show this message and exit.


.. _`pywbemcli class find --help`:

pywbemcli class find --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class find --help` subcommand


::

    Usage: pywbemcli class find [COMMAND-OPTIONS] CLASSNAME-REGEX

      Find all classes that match CLASSNAME-REGEX.

      Find all classes in the namespace(s) of the target WBEMServer that match
      the CLASSNAME-REGEX regular expression argument. The CLASSNAME-REGEX
      argument is required.

      The CLASSNAME-REGEX argument may be either a complete classname or a
      regular expression that can be matched to one or more classnames. To limit
      the filter to a single classname, terminate the classname with $.

      The regular expression is anchored to the beginning of the classname and
      is case insensitive. Thus, `pywbem_` returns all classes that begin with
      `PyWBEM_`, `pywbem_`, etc.

      The namespace option limits the search to the defined namespace. Otherwise
      all namespaces in the target server are searched.

      Output is in table format if table output specified. Otherwise it is in
      the form <namespace>:<classname>

    Options:
      -s, --sort              Sort into alphabetical order by classname.
      -n, --namespace <name>  Namespace to use for this operation. If defined that
                              namespace overrides the general options namespace
      -h, --help              Show this message and exit.


.. _`pywbemcli class get --help`:

pywbemcli class get --help
^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class get --help` subcommand


::

    Usage: pywbemcli class get [COMMAND-OPTIONS] CLASSNAME

      Get and display a single CIM class.

      Get a single CIM class defined by the CLASSNAME argument from the WBEM
      server and display it. Normally it is retrieved from the default namespace
      in the server.

      If the class is not found in the WBEM Server, the server returns an
      exception.

      The --includeclassorigin, --includeclassqualifiers, and --propertylist
      options determine what parts of the class definition are tetrieved.

      The --output option determines the output format for the display.

    Options:
      -l, --localonly                 Show only local properties of the class.
      --no-qualifiers                 If set, request server to not include
                                      qualifiers in the returned class(s). The
                                      default behavior is to request include
                                      qualifiers in the returned class(s).
      -c, --includeclassorigin        Include classorigin in the result.
      -p, --propertylist <property name>
                                      Define a propertylist for the request. If
                                      not included a Null property list is defined
                                      and the server returns all properties. If
                                      defined as empty string the server returns
                                      no properties. ex: -p propertyname1 -p
                                      propertyname2 or -p
                                      propertyname1,propertyname2
      -n, --namespace <name>          Namespace to use for this operation. If
                                      defined that namespace overrides the general
                                      options namespace
      -h, --help                      Show this message and exit.


.. _`pywbemcli class invokemethod --help`:

pywbemcli class invokemethod --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class invokemethod --help` subcommand


::

    Usage: pywbemcli class invokemethod [COMMAND-OPTIONS] CLASSNAME METHODNAME

      Invoke the class method named methodname.

      This invokes the method named METHODNAME on the class named CLASSNAME.

      This is the class level invokemethod and uses only the class name on the
      invoke.The subcommand `instance invokemethod` invokes methods based on
      instance name.

    Options:
      -p, --parameter parameter  Optional multiple method parameters of form
                                 name=value
      -n, --namespace <name>     Namespace to use for this operation. If defined
                                 that namespace overrides the general options
                                 namespace
      -h, --help                 Show this message and exit.


.. _`pywbemcli class references --help`:

pywbemcli class references --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class references --help` subcommand


::

    Usage: pywbemcli class references [COMMAND-OPTIONS] CLASSNAME

      Get the reference classes for CLASSNAME.

      Get the reference classes (or their classnames) for the CLASSNAME argument
      filtered by the role and result class options and modified  by the other
      options.

    Options:
      -R, --resultclass <class name>  Filter by the classname provided.
      -r, --role <role name>          Filter by the role name provided.
      --no-qualifiers                 If set, request server to not include
                                      qualifiers in the returned class(s). The
                                      default behavior is to request include
                                      qualifiers in the returned class(s).
      -c, --includeclassorigin        Include classorigin in the result.
      -p, --propertylist <property name>
                                      Define a propertylist for the request. If
                                      not included a Null property list is defined
                                      and the server returns all properties. If
                                      defined as empty string the server returns
                                      no properties. ex: -p propertyname1 -p
                                      propertyname2 or -p
                                      propertyname1,propertyname2
      -o, --names_only                Show only local properties of the class.
      -s, --sort                      Sort into alphabetical order by classname.
      -n, --namespace <name>          Namespace to use for this operation. If
                                      defined that namespace overrides the general
                                      options namespace
      -S, --summary                   Return only summary of objects (count).
      -h, --help                      Show this message and exit.


.. _`pywbemcli class tree --help`:

pywbemcli class tree --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class tree --help` subcommand


::

    Usage: pywbemcli class tree [COMMAND-OPTIONS] CLASSNAME

      Display CIM class inheritance hierarchy tree.

      Displays a tree of the class hiearchy to show superclasses and subclasses.

      CLASSNAMe is an optional argument that defines the starting point for the
      hiearchy display

      If the --superclasses option not specified the hiearchy starting either at
      the top most classes of the class hiearchy or at the class defined by
      CLASSNAME is displayed.

      if the --superclasses options is specified and a CLASSNAME is defined the
      class hiearchy of superclasses leading to CLASSNAME is displayed.

      This is a separate subcommand because t is tied specifically to displaying
      in a tree format.so that the --output-format global option is ignored.

    Options:
      -s, --superclasses      Display the superclasses to CLASSNAME as a tree.
                              When this option is set, the CLASSNAME argument is
                              required
      -n, --namespace <name>  Namespace to use for this operation. If defined that
                              namespace overrides the general options namespace
      -h, --help              Show this message and exit.


.. _`pywbemcli connection --help`:

pywbemcli connection --help
---------------------------



The following defines the help output for the `pywbemcli connection --help` subcommand


::

    Usage: pywbemcli connection [COMMAND-OPTIONS] COMMAND [ARGS]...

      Command group to manage WBEM connections.

      These command allow viewing and setting connection information.

      In addition to the command-specific options shown in this help text, the
      general options (see 'pywbemcli --help') can also be specified before the
      command. These are NOT retained after the command is executed.

    Options:
      -h, --help  Show this message and exit.

    Commands:
      delete  Delete connection information.
      export  Export the current connection information.
      list    Execute a predefined wbem request.
      new     Create a new named WBEM connection.
      save    Save current connection into repository.
      select  Select a connection from defined connections.
      show    Show current or NAME connection information.
      test    Execute a predefined wbem request.


.. _`pywbemcli connection delete --help`:

pywbemcli connection delete --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection delete --help` subcommand


::

    Usage: pywbemcli connection delete [COMMAND-OPTIONS] NAME

      Delete connection information.

      Delete connection information from the persistent store for the connection
      defined by NAME.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli connection export --help`:

pywbemcli connection export --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection export --help` subcommand


::

    Usage: pywbemcli connection export [COMMAND-OPTIONS]

      Export  the current connection information.

      Creates an export statement for each connection variable and outputs the
      statement to the conole.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli connection list --help`:

pywbemcli connection list --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection list --help` subcommand


::

    Usage: pywbemcli connection list [COMMAND-OPTIONS]

      Execute a predefined wbem request.

      This provides a simple test to determine if the defined connection exists
      and is working.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli connection new --help`:

pywbemcli connection new --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection new --help` subcommand


::

    Usage: pywbemcli connection new [COMMAND-OPTIONS] NAME uri

      Create a new named WBEM connection.

      This subcommand creates and saves a new named connection from the input
      arguments (NAME and URI) and options

      The new connection that can be referenced by the name argument in the
      future.  This connection object is capable of managing all of the
      properties defined for WBEMConnections.

      The NAME and URI arguments MUST exist. They define the server uri and the
      unique name under which this server connection information will be stored.
      All other properties are optional.

      It does NOT automatically set the pywbemcli to use that connection. Use
      `connection select` to set a particular stored connection definition as
      the current connection.

      This is the alternative means of defining a new WBEM server to be
      accessed. A server can also be defined by supplying the parameters on the
      command line and using the `connection set` command to put it into the
      connection repository.

    Options:
      -d, --default_namespace TEXT  Default Namespace to use in the target
                                    WBEMServer if no namespace is defined in the
                                    subcommand (Default: root/cimv2).
      -u, --user TEXT               User name for the WBEM Server connection.
      -p, --password TEXT           Password for the WBEM Server. Will be
                                    requested as part  of initialization if user
                                    name exists and it is not  provided by this
                                    option.
      -t, --timeout INTEGER RANGE   Operation timeout for the WBEM Server in
                                    seconds. Default: 30
      -n, --noverify                If set, client does not verify server
                                    certificate.
      -c, --certfile TEXT           Server certfile. Ignored if noverify flag set.
      -k, --keyfile TEXT            Client private key file.
      -m, --mock-server FILENAME    If this option is defined, a mock WBEM server
                                    is constructed as the target WBEM server and
                                    the option value defines a MOF or Python file
                                    to be used to populate the mock repository.
                                    This option may be used multiple times where
                                    each use defines a single file or
                                    file_path.See the pywbemcli documentation for
                                    more information.
      --ca_certs TEXT               File or directory containing certificates that
                                    will be matched against a certificate received
                                    from the WBEM server. Set the --no-verify-cert
                                    option to bypass client verification of the
                                    WBEM server certificate. Default: Searches for
                                    matching certificates in the following system
                                    directories: /etc/pki/ca-
                                    trust/extracted/openssl/ca-bundle.trust.crt
                                    /etc/ssl/certs
                                    /etc/ssl/certificates
      -h, --help                    Show this message and exit.


.. _`pywbemcli connection save --help`:

pywbemcli connection save --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection save --help` subcommand


::

    Usage: pywbemcli connection save [COMMAND-OPTIONS] NAME

      Save current connection into repository.

      Saves the current wbem connection information into the repository of
      connections. If the name does not already exist in the connection
      information, the provided name is used.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli connection select --help`:

pywbemcli connection select --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection select --help` subcommand


::

    Usage: pywbemcli connection select [COMMAND-OPTIONS] NAME

      Select a connection from defined connections.

      Selects a connection from the persistently stored set of named connections
      if NAME exists in the store.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli connection show --help`:

pywbemcli connection show --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection show --help` subcommand


::

    Usage: pywbemcli connection show [COMMAND-OPTIONS] NAME

      Show current or NAME connection information.

      This subcommand displays  all the variables that make up the current WBEM
      connection if the optional NAME argument is NOT provided

      If the optional NAME argument is provided, the information on the
      connection with that name is displayed if that name is in the persistent
      repository.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli connection test --help`:

pywbemcli connection test --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection test --help` subcommand


::

    Usage: pywbemcli connection test [COMMAND-OPTIONS]

      Execute a predefined wbem request.

      This executes a predefined request against the  currently defined WBEM
      server to tconfirm that the connection exists and is working.

      It executes getclass on CIM_ManagedElement as the standard test.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli help --help`:

pywbemcli help --help
---------------------



The following defines the help output for the `pywbemcli help --help` subcommand


::

    Usage: pywbemcli help [OPTIONS]

      Show help message for interactive mode.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli instance --help`:

pywbemcli instance --help
-------------------------



The following defines the help output for the `pywbemcli instance --help` subcommand


::

    Usage: pywbemcli instance [COMMAND-OPTIONS] COMMAND [ARGS]...

      Command group to manage CIM instances.

      This incudes functions to get, enumerate, create, modify, and delete
      instances in a namspace and additional functions to get more general
      information on instances (ex. counts) within the namespace

      In addition to the command-specific options shown in this help text, the
      general options (see 'pywbemcli --help') can also be specified before the
      command. These are NOT retained after the command is executed.

    Options:
      -h, --help  Show this message and exit.

    Commands:
      associators   Get associated instances or names.
      count         Get instance count for classes.
      create        Create an instance of classname.
      delete        Delete a single CIM instance.
      enumerate     Enumerate instances or names of CLASSNAME.
      get           Get a single CIMInstance.
      invokemethod  Invoke a CIM method.
      query         Execute an execquery request.
      references    Get the reference instances or names.


.. _`pywbemcli instance associators --help`:

pywbemcli instance associators --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance associators --help` subcommand


::

    Usage: pywbemcli instance associators [COMMAND-OPTIONS] INSTANCENAME

      Get associated instances or names.

      Returns the associated instances or names (--names-only option) for the
      INSTANCENAME argument filtered by the --assocclass, --resultclass, --role
      and --resultrole options.

      This may be executed interactively by providing only a classname and the
      interactive option. Pywbemcli presents a list of instances in the class
      from which one can be chosen as the target.

    Options:
      -a, --assocclass <class name>   Filter by the associated instancename
                                      provided.
      -c, --resultclass <class name>  Filter by the result class name provided.
      -R, --role <role name>          Filter by the role name provided.
      -R, --resultrole <class name>   Filter by the result role name provided.
      -q, --includequalifiers         If set, requests server to include
                                      qualifiers in the returned instance(s).
      -c, --includeclassorigin        Include classorigin in the result.
      -p, --propertylist <property name>
                                      Define a propertylist for the request. If
                                      not included a Null property list is defined
                                      and the server returns all properties. If
                                      defined as empty string the server returns
                                      no properties. ex: -p propertyname1 -p
                                      propertyname2 or -p
                                      propertyname1,propertyname2
      -o, --names_only                Show only local properties of the class.
      -n, --namespace <name>          Namespace to use for this operation. If
                                      defined that namespace overrides the general
                                      options namespace
      -s, --sort                      Sort into alphabetical order by classname.
      -i, --interactive               If set, INSTANCENAME argument must be a
                                      class rather than an instance and user is
                                      presented with a list of instances of the
                                      class from which the instance to process is
                                      selected.
      -S, --summary                   Return only summary of objects (count).
      -h, --help                      Show this message and exit.


.. _`pywbemcli instance count --help`:

pywbemcli instance count --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance count --help` subcommand


::

    Usage: pywbemcli instance count [COMMAND-OPTIONS] CLASSNAME-REGEX

      Get instance count for classes.

      Displays the count of instances for the classes defined by the `CLASSNAME-
      REGEX` argument in one or more namespaces.

      The size of the response may be limited by CLASSNAME-REGEX argument which
      defines a regular expression based on the desired class names so that only
      classes that match the regex are counted. The CLASSNAME-regex argument is
      optional.

      The CLASSNAME-regex argument may be either a complete classname or a
      regular expression that can be matched to one or more classnames. To limit
      the filter to a single classname, terminate the classname with $.

      The CLASSNAME-REGEX regular expression is anchored to the beginning of the
      classname and is case insensitive. Thus `pywbem_` returns all classes that
      begin with `PyWBEM_`, `pywbem_`, etc.

      This operation can take a long time to execute.

    Options:
      -s, --sort              Sort by instance count. Otherwise sorted by
                              classname
      -n, --namespace <name>  Namespace to use for this operation. If defined that
                              namespace overrides the general options namespace
      -h, --help              Show this message and exit.


.. _`pywbemcli instance create --help`:

pywbemcli instance create --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance create --help` subcommand


::

    Usage: pywbemcli instance create [COMMAND-OPTIONS] CLASSNAME

      Create an instance of classname.

      Creates an instance of the class `CLASSNAME` with the properties defined
      in the property option.

      The propertylist option limits the created instance to the properties in
      the list. This parameter is NOT passed to the server

    Options:
      -P, --property property         Optional property definitions of form
                                      name=value.Multiple definitions allowed, one
                                      for each property to be included in the new
                                      instance.
      -p, --propertylist <property name>
                                      Define a propertylist for the request. If
                                      not included a Null property list is defined
                                      and the server returns all properties. If
                                      defined as empty string the server returns
                                      no properties. ex: -p propertyname1 -p
                                      propertyname2 or -p
                                      propertyname1,propertyname2
      -n, --namespace <name>          Namespace to use for this operation. If
                                      defined that namespace overrides the general
                                      options namespace
      -h, --help                      Show this message and exit.


.. _`pywbemcli instance delete --help`:

pywbemcli instance delete --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance delete --help` subcommand


::

    Usage: pywbemcli instance delete [COMMAND-OPTIONS] INSTANCENAME

      Delete a single CIM instance.

      Delete the instanced defined by INSTANCENAME from the WBEM server.

      This may be executed interactively by providing only a class name and the
      interactive option.

    Options:
      -i, --interactive       If set, INSTANCENAME argument must be a class rather
                              than an instance and user is presented with a list
                              of instances of the class from which the instance to
                              process is selected.
      -n, --namespace <name>  Namespace to use for this operation. If defined that
                              namespace overrides the general options namespace
      -h, --help              Show this message and exit.


.. _`pywbemcli instance enumerate --help`:

pywbemcli instance enumerate --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance enumerate --help` subcommand


::

    Usage: pywbemcli instance enumerate [COMMAND-OPTIONS] CLASSNAME

      Enumerate instances or names of CLASSNAME.

      Enumerate instances or instance names (the --name_only option) from the
      WBEMServer starting either at the top  of the hierarchy (if no CLASSNAME
      provided) or from the CLASSNAME argument if provided.

      Displays the returned instances (mof, xml, or table formats) or names

    Options:
      -l, --localonly                 Show only local properties of the class.
      -d, --deepinheritance           If set, requests server to return properties
                                      in subclasses of the target instances class.
                                      If option not specified only properties from
                                      target class are returned
      -q, --includequalifiers         If set, requests server to include
                                      qualifiers in the returned instance(s).
      -c, --includeclassorigin        Include ClassOrigin in the result.
      -p, --propertylist <property name>
                                      Define a propertylist for the request. If
                                      not included a Null property list is defined
                                      and the server returns all properties. If
                                      defined as empty string the server returns
                                      no properties. ex: -p propertyname1 -p
                                      propertyname2 or -p
                                      propertyname1,propertyname2
      -n, --namespace <name>          Namespace to use for this operation. If
                                      defined that namespace overrides the general
                                      options namespace
      -o, --names_only                Show only local properties of the class.
      -s, --sort                      Sort into alphabetical order by classname.
      -S, --summary                   Return only summary of objects (count).
      -h, --help                      Show this message and exit.


.. _`pywbemcli instance get --help`:

pywbemcli instance get --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance get --help` subcommand


::

    Usage: pywbemcli instance get [COMMAND-OPTIONS] INSTANCENAME

      Get a single CIMInstance.

      Gets the instance defined by INSTANCENAME.

      This may be executed interactively by providing only a classname and the
      interactive option (-i).

    Options:
      -l, --localonly                 Show only local properties of the returned
                                      instance.
      -q, --includequalifiers         If set, requests server to include
                                      qualifiers in the returned instance(s).
      -c, --includeclassorigin        Include class origin attribute in returned
                                      instance(s).
      -p, --propertylist <property name>
                                      Define a propertylist for the request. If
                                      not included a Null property list is defined
                                      and the server returns all properties. If
                                      defined as empty string the server returns
                                      no properties. ex: -p propertyname1 -p
                                      propertyname2 or -p
                                      propertyname1,propertyname2
      -n, --namespace <name>          Namespace to use for this operation. If
                                      defined that namespace overrides the general
                                      options namespace
      -i, --interactive               If set, INSTANCENAME argument must be a
                                      class rather than an instance and user is
                                      presented with a list of instances of the
                                      class from which the instance to process is
                                      selected.
      -h, --help                      Show this message and exit.


.. _`pywbemcli instance invokemethod --help`:

pywbemcli instance invokemethod --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance invokemethod --help` subcommand


::

    Usage: pywbemcli instance invokemethod [COMMAND-OPTIONS] INSTANCENAME
                                           METHODNAME

      Invoke a CIM method.

      Invoke the method defined by INSTANCENAME and METHODNAME arguments with
      parameters defined by the --parameter options.

      This issues an instance level invokemethod request and displays the
      results.

      A class level invoke method is available as `pywbemcli class
      invokemethod`.

    Options:
      -p, --parameter parameter  Optional multiple method parameters of form
                                 name=value
      -i, --interactive          If set, INSTANCENAME argument must be a class
                                 rather than an instance and user is presented
                                 with a list of instances of the class from which
                                 the instance to process is selected.
      -n, --namespace <name>     Namespace to use for this operation. If defined
                                 that namespace overrides the general options
                                 namespace
      -h, --help                 Show this message and exit.


.. _`pywbemcli instance query --help`:

pywbemcli instance query --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance query --help` subcommand


::

    Usage: pywbemcli instance query [COMMAND-OPTIONS] QUERY_STRING

      Execute an execquery request.

      Executes a query request on the target WBEM Server with the QUERY_STRING
      argument and query language options.

      The results of the query are displayed as mof or xml.

    Options:
      -l, --querylanguage QUERY LANGUAGE
                                      Use the query language defined. (Default:
                                      DMTF:CQL.
      -n, --namespace <name>          Namespace to use for this operation. If
                                      defined that namespace overrides the general
                                      options namespace
      -s, --sort                      Sort into alphabetical order by classname.
      -S, --summary                   Return only summary of objects (count).
      -h, --help                      Show this message and exit.


.. _`pywbemcli instance references --help`:

pywbemcli instance references --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance references --help` subcommand


::

    Usage: pywbemcli instance references [COMMAND-OPTIONS] INSTANCENAME

       Get the reference instances or names.

       Gets the reference instances or instance names(--names-only option) for a
       target `INSTANCENAME` in the target WBEM server filtered by the  `role`
       and `resultclass` options.

      This may be executed interactively by providing only a class name for
      `INSTANCENAME` and the `interactive` option(-i). Pywbemcli presents a list
      of instances names in the class from which one can be chosen as the
      target.

    Options:
      -R, --resultclass <class name>  Filter by the result class name provided.
      -r, --role <role name>          Filter by the role name provided.
      -q, --includequalifiers         If set, requests server to include
                                      qualifiers in the returned instance(s).
      -c, --includeclassorigin        Include classorigin in the result.
      -p, --propertylist <property name>
                                      Define a propertylist for the request. If
                                      not included a Null property list is defined
                                      and the server returns all properties. If
                                      defined as empty string the server returns
                                      no properties. ex: -p propertyname1 -p
                                      propertyname2 or -p
                                      propertyname1,propertyname2
      -o, --names_only                Show only local properties of the class.
      -n, --namespace <name>          Namespace to use for this operation. If
                                      defined that namespace overrides the general
                                      options namespace
      -s, --sort                      Sort into alphabetical order by classname.
      -i, --interactive               If set, INSTANCENAME argument must be a
                                      class rather than an instance and user is
                                      presented with a list of instances of the
                                      class from which the instance to process is
                                      selected.
      -S, --summary                   Return only summary of objects (count).
      -h, --help                      Show this message and exit.


.. _`pywbemcli qualifier --help`:

pywbemcli qualifier --help
--------------------------



The following defines the help output for the `pywbemcli qualifier --help` subcommand


::

    Usage: pywbemcli qualifier [COMMAND-OPTIONS] COMMAND [ARGS]...

      Commands to view QualifierDeclarations.

      Includes the capability to get and enumerate CIM qualifier declarations
      defined in the WBEM Server.

      pywbemcli does not provide the capability to create or delete CIM
      QualifierDeclarations

      In addition to the command-specific options shown in this help text, the
      general options (see 'pywbemcli --help') can also be specified before the
      command. These are NOT retained after the command is executed.

    Options:
      -h, --help  Show this message and exit.

    Commands:
      enumerate  Enumerate CIMQualifierDeclaractions.
      get        Display CIMQualifierDeclaration.


.. _`pywbemcli qualifier enumerate --help`:

pywbemcli qualifier enumerate --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli qualifier enumerate --help` subcommand


::

    Usage: pywbemcli qualifier enumerate [COMMAND-OPTIONS]

      Enumerate CIMQualifierDeclaractions.

      Displays all of the CIMQualifierDeclaration objects in the defined
      namespace in the current WBEM Server

    Options:
      -n, --namespace <name>  Namespace to use for this operation. If defined that
                              namespace overrides the general options namespace
      -S, --summary           Return only summary of objects (count).
      -h, --help              Show this message and exit.


.. _`pywbemcli qualifier get --help`:

pywbemcli qualifier get --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli qualifier get --help` subcommand


::

    Usage: pywbemcli qualifier get [COMMAND-OPTIONS] QUALIFIERNAME

      Display CIMQualifierDeclaration.

      Displays CIMQualifierDeclaration QUALIFIERNAME for the defined namespace
      in the current WBEMServer

    Options:
      -n, --namespace <name>  Namespace to use for this operation. If defined that
                              namespace overrides the general options namespace
      -h, --help              Show this message and exit.


.. _`pywbemcli repl --help`:

pywbemcli repl --help
---------------------



The following defines the help output for the `pywbemcli repl --help` subcommand


::

    Usage: pywbemcli repl [OPTIONS]

      Enter interactive (REPL) mode (default).

      Enters the interactive mode where subcommands can be entered interactively
      and load the command history file.

      If no options are specified on the command line,  the interactive mode is
      entered. The prompt is changed to `pywbemcli>' in the interactive mode.

      Pywbemcli may be terminated form this mode by entering <CTRL-D>, :q,
      :quit, :exit

      Parameters:

        ctx (:class:`click.Context`): The click context object. Created by the
        ``@click.pass_context`` decorator.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli server --help`:

pywbemcli server --help
-----------------------



The following defines the help output for the `pywbemcli server --help` subcommand


::

    Usage: pywbemcli server [COMMAND-OPTIONS] COMMAND [ARGS]...

      Command Group for WBEM server operations.

      In addition to the command-specific options shown in this help text, the
      general options (see 'pywbemcli --help') can also be specified before the
      command. These are NOT retained after the command is executed.

    Options:
      -h, --help  Show this message and exit.

    Commands:
      brand       Display information on the server.
      connection  Display connection info used by this server.
      info        Display general information on the Server.
      interop     Display the interop namespace name.
      namespaces  Display the namespaces in the WBEM server
      profiles    Display profiles in the WBEM Server.
      test_pull   Test existence of pull opeations.


.. _`pywbemcli server brand --help`:

pywbemcli server brand --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server brand --help` subcommand


::

    Usage: pywbemcli server brand [COMMAND-OPTIONS]

      Display information on the server.

      Display brand information on the current server if it is available. This
      is typically the definition of the server implementor.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli server connection --help`:

pywbemcli server connection --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server connection --help` subcommand


::

    Usage: pywbemcli server connection [COMMAND-OPTIONS]

      Display connection info used by this server.

      Displays the connection information for the WBEM connection attached to
      this server.  This includes uri, default namespace, etc.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli server info --help`:

pywbemcli server info --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server info --help` subcommand


::

    Usage: pywbemcli server info [COMMAND-OPTIONS]

      Display general information on the Server.

      Displays general information on the current server includeing brand,
      namespaces, etc.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli server interop --help`:

pywbemcli server interop --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server interop --help` subcommand


::

    Usage: pywbemcli server interop [COMMAND-OPTIONS]

      Display the interop namespace name.

      Displays the name of the interop namespace defined for the WBEM Server.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli server namespaces --help`:

pywbemcli server namespaces --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server namespaces --help` subcommand


::

    Usage: pywbemcli server namespaces [COMMAND-OPTIONS]

      Display the namespaces in the WBEM server

    Options:
      -s, --sort  Sort into alphabetical order by classname.
      -h, --help  Show this message and exit.


.. _`pywbemcli server profiles --help`:

pywbemcli server profiles --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server profiles --help` subcommand


::

    Usage: pywbemcli server profiles [COMMAND-OPTIONS]

      Display profiles in the WBEM Server.

      This display may be filtered by the optional organization and profile name
      options

    Options:
      -o, --organization <org name>   Filter by the defined organization. (ex. -o
                                      DMTF
      -n, --profilename <profile name>
                                      Filter by the profile name. (ex. -n Array
      -h, --help                      Show this message and exit.


.. _`pywbemcli server test_pull --help`:

pywbemcli server test_pull --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server test_pull --help` subcommand


::

    Usage: pywbemcli server test_pull [COMMAND-OPTIONS]

      Test existence of pull opeations.

      Test whether the pull WBEMConnection methods (ex. OpenEnumerateInstances)
      exist on the WBEM server.

      This command tests all of the pull operations and reports any that return
      a NOT_SUPPORTED response.

    Options:
      -h, --help  Show this message and exit.

