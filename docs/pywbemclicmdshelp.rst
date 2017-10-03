
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
      -o, --output-format [table|plain|simple|grid|mof|xml|txt|tree]
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
      --version                       Show the version of this command and exit.
      -h, --help                      Show this message and exit.

    Commands:
      class         Command group to manage CIM Classes.
      connection    Command group to manage WBEM connections.
      help          Show help message for interactive mode.
      instance      Command group to manage CIM instances.
      qualifier     Commands to view QualifierDeclarations.
      repl          Enter interactive (REPL) mode (default) and...
      server        Command Group for WBEM server operations.
      subscription  Command Group to manage WBEM subscriptions.


.. _`pywbemcli class --help`:

pywbemcli class --help
----------------------



The following defines the help output for the `pywbemcli class --help` subcommand


::

    Usage: pywbemcli class [COMMAND-OPTIONS] COMMAND [ARGS]...

      Command group to manage CIM Classes.

      In addition to the command-specific options shown in this help text, the
      general options (see 'pywbemcli --help') can also be specified before the
      command. These are NOT retained after the command is executed.

    Options:
      -h, --help  Show this message and exit.

    Commands:
      associators   Get the associated classes for the CLASSNAME.
      delete        Delete the class defined by CLASSNAME.
      enumerate     Enumerate classes from the WBEMServer.
      find          Find all classes that match CLASSNAME-regex...
      get           Get and display a single CIM class.
      invokemethod  Invoke the class method named methodname.
      references    Get the reference classes for the CLASSNAME.
      tree          Display CIM class inheritance hierarchy tree.


.. _`pywbemcli class associators --help`:

pywbemcli class associators --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class associators --help` subcommand


::

    Usage: pywbemcli class associators [COMMAND-OPTIONS] CLASSNAME

      Get the associated classes for the CLASSNAME.

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
      --includequalifiers / --no_includequalifiers
                                      Include qualifiers in the result. Default is
                                      to include qualifiers
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
      -h, --help                      Show this message and exit.


.. _`pywbemcli class delete --help`:

pywbemcli class delete --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class delete --help` subcommand


::

    Usage: pywbemcli class delete [COMMAND-OPTIONS] CLASSNAME

      Delete the class defined by CLASSNAME.

      Deletes the class from the  WBEM Server completely.

      If the class has instances, the command is refused unless the --force
      option is used. If --force is used, instances are also deleted.

      WARNING: Removing classes from a WBEM Server can cause damage to the
      server. Use this with caution.  It can impact instance providers and other
      components in the server.

      Some server may refuse the operation.

    Options:
      -f, --force             Force the delete request to be issued even if there
                              are instances in the server or subclasses to this
                              class.  The WBEM Server may still refuse the
                              request.
      -n, --namespace <name>  Namespace to use for this operation. If defined that
                              namespace overrides the general options namespace
      -h, --help              Show this message and exit.


.. _`pywbemcli class enumerate --help`:

pywbemcli class enumerate --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class enumerate --help` subcommand


::

    Usage: pywbemcli class enumerate [COMMAND-OPTIONS] CLASSNAME

      Enumerate classes from the WBEMServer.

      Enumerates the classes (or classnames) from the WBEMServer starting either
      at the top of the class hierarchy or from  the position in the class
      hierarch defined by `classname` argument if provided.

      The output format is defined by the output_format global option.

      The includeclassqualifiers, includeclassorigin options define optional
      information to be included in the output.

      The deepinheritance option defines whether the complete hiearchy is
      retrieved or just the next level in the hiearchy.

    Options:
      -d, --deepinheritance           Return complete subclass hierarchy for this
                                      class if set. Otherwise retrieve only the
                                      next hierarchy level.
      -l, --localonly                 Show only local properties of the class.
      --includequalifiers / --no_includequalifiers
                                      Include qualifiers in the result. Default is
                                      to include qualifiers
      -c, --includeclassorigin        Include classorigin in the result.
      -o, --names_only                Show only local properties of the class.
      -s, --sort                      Sort into alphabetical order by classname.
      -n, --namespace <name>          Namespace to use for this operation. If
                                      defined that namespace overrides the general
                                      options namespace
      -h, --help                      Show this message and exit.


.. _`pywbemcli class find --help`:

pywbemcli class find --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class find --help` subcommand


::

    Usage: pywbemcli class find [COMMAND-OPTIONS] CLASSNAME-regex

      Find all classes that match CLASSNAME-regex

      Find all classes in the namespace(s) of the target WBEMServer that match
      the CLASSNAME-regex regular expression argument. The CLASSNAME-regex
      argument is required.

      The CLASSNAME argument may be either a complete classname or a regular
      expression that can be matched to one or more classnames. To limit the
      filter to a single classname, terminate the classname with $.

      The regular expression is anchored to the beginning of the classname and
      is case insensitive. Thus, `pywbem_` returns all classes that begin with
      `PyWBEM_`, `pywbem_`, etc.

      The namespace option limits the search to the defined namespace. Otherwise
      all namespaces in the target server are searched.

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

    Options:
      -l, --localonly                 Show only local properties of the class.
      --includequalifiers / --no_includequalifiers
                                      Include qualifiers in the result. Default is
                                      to include qualifiers
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

    Usage: pywbemcli class invokemethod [COMMAND-OPTIONS] classname name

      Invoke the class method named methodname.

      This invokes the method named `methodname` on the class named `classname`.

      This is the class level invokemethod and uses only the class name on the
      invoke. The subcommand `instance invokemethod` invokes methods based on
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

      Get the reference classes for the CLASSNAME.

      Get the reference classes (or their classnames) for the CLASSNAME argument
      filtered by the role and result class options and modified  by the other
      options.

    Options:
      -R, --resultclass <class name>  Filter by the classname provided.
      -r, --role <role name>          Filter by the role name provided.
      --includequalifiers / --no_includequalifiers
                                      Include qualifiers in the result. Default is
                                      to include qualifiers
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
      -h, --help                      Show this message and exit.


.. _`pywbemcli class tree --help`:

pywbemcli class tree --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class tree --help` subcommand


::

    Usage: pywbemcli class tree [COMMAND-OPTIONS] CLASSNAME

      Display CIM class inheritance hierarchy tree.

      The classname option, if it exists defines the topmost class of the
      hierarchy to include in the display. This is a separate subcommand because
      it is tied specifically to displaying in a tree format.

    Options:
      -s, --superclasses      Display the superclasses to CLASSNAME as a tree.  In
                              this case CLASSNAME is required
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
      delete  Show the current connection information, i.e.
      export  Export the current connection information.
      list    Execute a simple wbem request to test that...
      new     Create a new named connection from the input...
      save    Save current connection into repository.
      select  Select a connection from the current defined...
      show    Show the current connection information, i.e.
      test    Execute a simple wbem request to test that...


.. _`pywbemcli connection delete --help`:

pywbemcli connection delete --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection delete --help` subcommand


::

    Usage: pywbemcli connection delete [COMMAND-OPTIONS] name

      Show the current connection information, i.e. all the variables that make
      up the current connection

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

      Execute a simple wbem request to test that the connection exists and is
      working.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli connection new --help`:

pywbemcli connection new --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection new --help` subcommand


::

    Usage: pywbemcli connection new [COMMAND-OPTIONS] name SERVER

      Create a new named connection from the input parameters.

      This subcommand creates and saves a new named connection from the input
      parameters.

      The name and server arguments MUST exist. They define the server uri and
      the unique name under which this server connection information will be
      stored. All other properties are optional.

      It does NOT automatically set the pywbemcli to use that connection. Use
      `connection select` to set a particular stored connection definition as
      the current connection.

      This is the alternative means of defining a new WBEM server to be accessed
      to supplying the parameters on the command line. and using the connection
      set command to put it into the connection repository.

      Defines a new connection that can be referenced by the name argument in
      the future.  This connection object is capable of managing all of the
      properties defined for WBEMConnections.

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

    Usage: pywbemcli connection save [COMMAND-OPTIONS] name

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

    Usage: pywbemcli connection select [COMMAND-OPTIONS] name

      Select a connection from the current defined connections

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli connection show --help`:

pywbemcli connection show --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection show --help` subcommand


::

    Usage: pywbemcli connection show [COMMAND-OPTIONS] name

      Show the current connection information, i.e. all the variables that make
      up the current connection

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli connection test --help`:

pywbemcli connection test --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection test --help` subcommand


::

    Usage: pywbemcli connection test [COMMAND-OPTIONS]

      Execute a simple wbem request to test that the connection exists and is
      working.

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
      delete        Delete a single instance defined by...
      enumerate     Enumerate instances or names of classname.
      get           Get a single CIMInstance.
      invokemethod  Invoke the method defined by instancename and...
      query         Execute the query defined by the query...
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
      -q, --includequalifiers         Include qualifiers in the result.
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
      -i, --interactive               If set, instancename argument must be a
                                      class and  user is provided with a list of
                                      instances of the  class from which the
                                      instance to delete is selected.
      -h, --help                      Show this message and exit.


.. _`pywbemcli instance count --help`:

pywbemcli instance count --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance count --help` subcommand


::

    Usage: pywbemcli instance count [COMMAND-OPTIONS] CLASSNAME-regex

      Get instance count for classes.

      Displays the count of instances for the classes defined by the `classname-
      regex` argument in one or more namespaces.

      The size of the response may be limited by CLASSNAME-regex argument which
      defines a classname regular expression so that only those classes are
      counted. The CLASSNAME-regex argument is optional.

      The CLASSNAME-regex argument may be either a complete classname or a
      regular expression that can be matched to one or more classnames. To limit
      the filter to a single classname, terminate the classname with $.

      The regular expression is anchored to the beginning of the classname and
      is case insensitive. Thus `pywbem_` returns all classes that begin with
      `PyWBEM_`, `pywbem_`, etc.

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

    Usage: pywbemcli instance create [COMMAND-OPTIONS] classname

      Create an instance of classname.

      Creates an instance of the class `classname` with the properties defined
      in the property option.

      The propertylist option limits the created instance to the properties in
      the list. This parameter is NOT passed to the server

    Options:
      -P, --property property         Optional property definitions of form
                                      name=value.Multiple definitions allowed, one
                                      for each property
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

      Delete a single instance defined by instancename from the WBEM server.
      This may be executed interactively by providing only a classname and the
      interactive option.

    Options:
      -i, --interactive       If set, instancename argument must be a class and
                              user is provided with a list of instances of the
                              class from which the instance to delete is selected.
      -n, --namespace <name>  Namespace to use for this operation. If defined that
                              namespace overrides the general options namespace
      -h, --help              Show this message and exit.


.. _`pywbemcli instance enumerate --help`:

pywbemcli instance enumerate --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance enumerate --help` subcommand


::

    Usage: pywbemcli instance enumerate [COMMAND-OPTIONS] CLASSNAME

      Enumerate instances or names of classname.

      Enumerate instances or instance names from the WBEMServer starting either
      at the top  of the hierarchy (if no classname provided) or from the
      classname argument if provided.

      Displays the returned instances or names

    Options:
      -l, --localonly                 Show only local properties of the class.
      -d, --deepinheritance           Return properties in subclasses of defined
                                      target.  If not specified only properties in
                                      target class are returned
      -q, --includequalifiers         Include qualifiers in the result.
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
      -h, --help                      Show this message and exit.


.. _`pywbemcli instance get --help`:

pywbemcli instance get --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance get --help` subcommand


::

    Usage: pywbemcli instance get [COMMAND-OPTIONS] INSTANCENAME

      Get a single CIMInstance.

      Gets the instance defined by instancename.

      This may be executed interactively by providing only a classname and the
      interactive option.

    Options:
      -l, --localonly                 Show only local properties of the returned
                                      instance.
      -q, --includequalifiers         Include qualifiers in the result.
      -c, --includeclassorigin        Include Class Origin in the returned
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
      -i, --interactive               If set, instancename argument must be a
                                      class and  user is provided with a list of
                                      instances of the  class from which the
                                      instance to delete is selected.
      -h, --help                      Show this message and exit.


.. _`pywbemcli instance invokemethod --help`:

pywbemcli instance invokemethod --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance invokemethod --help` subcommand


::

    Usage: pywbemcli instance invokemethod [COMMAND-OPTIONS] name name

      Invoke the method defined by instancename and methodname with parameters.

      This issues an instance level invokemethod request and displays the
      results.

    Options:
      -p, --parameter parameter  Optional multiple method parameters of form
                                 name=value
      -i, --interactive          If set, instancename argument must be a class and
                                 user is provided with a list of instances of the
                                 class from which the instance to delete is
                                 selected.
      -n, --namespace <name>     Namespace to use for this operation. If defined
                                 that namespace overrides the general options
                                 namespace
      -h, --help                 Show this message and exit.


.. _`pywbemcli instance query --help`:

pywbemcli instance query --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance query --help` subcommand


::

    Usage: pywbemcli instance query [COMMAND-OPTIONS] <query string>

      Execute the query defined by the query argument.

      Executes a query request on the target WBEM Server with the query language
      and query string defined on input.

    Options:
      -l, --querylanguage <query language>
                                      Use the query language defined. (Default:
                                      DMTF:CQL.
      -n, --namespace <name>          Namespace to use for this operation. If
                                      defined that namespace overrides the general
                                      options namespace
      -s, --sort                      Sort into alphabetical order by classname.
      -h, --help                      Show this message and exit.


.. _`pywbemcli instance references --help`:

pywbemcli instance references --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance references --help` subcommand


::

    Usage: pywbemcli instance references [COMMAND-OPTIONS] INSTANCENAME

      Get the reference instances or names.

      Gets the reference instances or instance names (--names-only option) for a
      target instance name in the target WBEM server.

      For the INSTANCENAME argument provided return instances or instance names
      filtered by the --role and --resultclass options.

      This may be executed interactively by providing only a classname and the
      interactive option. Pywbemcli presents a list of instances in the class
      from which one can be chosen as the target.

    Options:
      -R, --resultclass <class name>  Filter by the result class name provided.
      -r, --role <role name>          Filter by the role name provided.
      -q, --includequalifiers         Include qualifiers in the result.
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
      -i, --interactive               If set, instancename argument must be a
                                      class and  user is provided with a list of
                                      instances of the  class from which the
                                      instance to delete is selected.
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
      -s, --sort              Sort into alphabetical order by classname.
      -h, --help              Show this message and exit.


.. _`pywbemcli qualifier get --help`:

pywbemcli qualifier get --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli qualifier get --help` subcommand


::

    Usage: pywbemcli qualifier get [COMMAND-OPTIONS] NAME

      Display CIMQualifierDeclaration.

      Displays a single CIMQualifierDeclaration for the defined namespace in the
      current WBEMServer

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

      Enter interactive (REPL) mode (default) and load history file.

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
      brand       Display interop namespace name in the WBEM...
      connection  Display information on the connection used by...
      info        Display the brand information on theWBEM...
      interop     Display the interop namespace name in the...
      namespaces  Display the namespaces in the WBEM server
      profiles    Display profiles in the WBEM Server.
      test_pull   Test whether pull opeations exist on the WBEM...


.. _`pywbemcli server brand --help`:

pywbemcli server brand --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server brand --help` subcommand


::

    Usage: pywbemcli server brand [COMMAND-OPTIONS]

      Display interop namespace name in the WBEM Server.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli server connection --help`:

pywbemcli server connection --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server connection --help` subcommand


::

    Usage: pywbemcli server connection [COMMAND-OPTIONS]

      Display information on the connection used by this server.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli server info --help`:

pywbemcli server info --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server info --help` subcommand


::

    Usage: pywbemcli server info [COMMAND-OPTIONS]

      Display the brand information on theWBEM Server.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli server interop --help`:

pywbemcli server interop --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server interop --help` subcommand


::

    Usage: pywbemcli server interop [COMMAND-OPTIONS]

      Display the interop namespace name in the WBEM Server.

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

      Test whether pull opeations exist on the WBEM server.

    Options:
      -h, --help  Show this message and exit.


.. _`pywbemcli subscription --help`:

pywbemcli subscription --help
-----------------------------



The following defines the help output for the `pywbemcli subscription --help` subcommand


::

    Usage: pywbemcli subscription [COMMAND-OPTIONS] COMMAND [ARGS]...

      Command Group to manage WBEM subscriptions.

      This group uses the pywbem subscription manager to view and manage CIM
      Indication subscripitons for a WBEM Server

    Options:
      -h, --help  Show this message and exit.

    Commands:
      create  Create a new subscription based on...
      delete  List subscriptions, destinations or filters
      list    List subscriptions, destinations or filters


.. _`pywbemcli subscription create --help`:

pywbemcli subscription create --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli subscription create --help` subcommand


::

    Usage: pywbemcli subscription create [COMMAND-OPTIONS]

      Create a new subscription based on destination and filter provided as
      input

    Options:
      -d, --destination destination  Listener destination for indications
      -f, --filter filter            Filter for this subscription
      -o, --owned                    If True, will create an owned subscription
                                     that will be removed from servers when
                                     pywbemcli terminates
      -c, --class                    Optional query class
      --summary TEXT                 If True shows a summary table of key info
                                     from the destinations and filters for the
                                     subscriptions. Otherwise it shows the
                                     subscription objects in detail.
      -h, --help                     Show this message and exit.


.. _`pywbemcli subscription delete --help`:

pywbemcli subscription delete --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli subscription delete --help` subcommand


::

    Usage: pywbemcli subscription delete [COMMAND-OPTIONS]

      List subscriptions, destinations or filters

    Options:
      -d, --destination destination   Listener destination for indications
      -q, --query query               query for this subscription
      -l, --querylanguage querylanguage
                                      querylanguage for this subscription
      -h, --help                      Show this message and exit.


.. _`pywbemcli subscription list --help`:

pywbemcli subscription list --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli subscription list --help` subcommand


::

    Usage: pywbemcli subscription list [COMMAND-OPTIONS]

      List subscriptions, destinations or filters

    Options:
      -o, --owned  If True, list only owned subscriptions
      -h, --help   Show this message and exit.

