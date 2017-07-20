
.. _`pywbemcli Help Command Details`:

pywbemcli Help Command Details
==============================


This section defines the help output for each pywbemcli command group and subcommand.



The following defines the help output for the `pywbemcli  --help` subcommand


::

    Usage: pywbemcli [GENERAL-OPTIONS] COMMAND [ARGS]...
    
      Command line browser for WBEM Servers. This cli tool implements the
      CIM/XML client APIs as defined in pywbem to make requests to a WBEM
      server. This browser uses subcommands to      * Explore the
      characteristics of WBEM Servers based on using the       pywbem client
      APIs.  It can manage/inspect CIM_Classes and       CIM_instanceson the
      server.
    
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
      -t, --timeout TEXT              Operation timeout for the WBEM Server in
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
      -v, --verbose                   Display extra information about the
                                      processing.
      --version                       Show the version of this command and exit.
      --help                          Show this message and exit.
    
    Commands:
      class       Command Group to manage CIM Classes.
      connection  Command group to manage WBEM connections.
      help        Show help message for interactive mode.
      instance    Command Group to manage CIM instances.
      qualifier   Command Group to manage CIM...
      repl        Enter interactive (REPL) mode (default) and...
      server      Command Group for WBEM server operations.



.. _`pywbemcli class --help`:

pywbemcli class --help
----------------------



The following defines the help output for the `pywbemcli class --help` subcommand


::

    Error, None
    Usage: pywbemcli class [COMMAND-OPTIONS] COMMAND [ARGS]...
    
      Command Group to manage CIM Classes.
    
      In addition to the command-specific options shown in this help text, the
      general options (see 'pywbemcli --help') can also be specified before the
      command. These are NOT retained after the command is executed.
    
    Options:
      --help  Show this message and exit.
    
    Commands:
      associators   Get the associated classes for the CLASSNAME.
      delete        Delete the class defined by CLASSNAME from...
      enumerate     Enumerate classes from the WBEMServer.
      find          Find all classes that match CLASSNAME.
      get           get and display a single CIM class from the...
      hierarchy     Display class inheritance hierarchy as a...
      invokemethod  Invoke the class method named methodname in...
      references    Get the reference classes for the CLASSNAME.



.. _`pywbemcli class associators --help`:

pywbemcli class associators --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class associators --help` subcommand


::

    Error, None
    Usage: pywbemcli class associators [COMMAND-OPTIONS] CLASSNAME
    
      Get the associated classes for the CLASSNAME.
    
      Get the classes(or classnames) that are associated with the CLASSNAME
      argument filtered by the assocclass, resultclass, role and resultrole
      arguments options.
    
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
      --help                          Show this message and exit.



.. _`pywbemcli class delete --help`:

pywbemcli class delete --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class delete --help` subcommand


::

    Error, None
    Usage: pywbemcli class delete [COMMAND-OPTIONS] CLASSNAME
    
      Delete the class defined by CLASSNAME from the WBEM Server. If the class
      has instances, the command is refused unless the --force option is used.
    
      WARNING: Removing classes from a WBEM Server can cause damage to the
      server. Use this with caution.
    
    Options:
      -f, --force             Force the delete request to be issued even if there
                              are instances in the server or subclasses to this
                              class.  The WBEM Server may still refuse the
                              request.
      -n, --namespace <name>  Namespace to use for this operation. If defined that
                              namespace overrides the general options namespace
      --help                  Show this message and exit.



.. _`pywbemcli class enumerate --help`:

pywbemcli class enumerate --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class enumerate --help` subcommand


::

    Error, None
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
      --help                          Show this message and exit.



.. _`pywbemcli class find --help`:

pywbemcli class find --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class find --help` subcommand


::

    Error, None
    Usage: pywbemcli class find [COMMAND-OPTIONS] CLASSNAME regex
    
      Find all classes that match CLASSNAME.
    
      Find all  class names in the namespace(s) of the defined WBEMServer that
      match the CLASSNAME regular expression argument. The CLASSNAME argument
      may be either a complete classname or a regular expression that can be
      matched to one or more classnames. To limit the filter to a single
      classname, terminate the classname with $.
    
      The regular expression is anchored to the beginning of CLASSNAME and is
      case insensitive. Thus pywbem_ returns all classes that begin with
      PyWBEM_, pywbem_, etc.
    
      The namespace option limits the search to the defined namespace.
    
    Options:
      -s, --sort              Sort into alphabetical order by classname.
      -n, --namespace <name>  Namespace to use for this operation. If defined that
                              namespace overrides the general options namespace
      --help                  Show this message and exit.



.. _`pywbemcli class get --help`:

pywbemcli class get --help
^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class get --help` subcommand


::

    Error, None
    Usage: pywbemcli class get [COMMAND-OPTIONS] CLASSNAME
    
      get and display a single CIM class from the WBEM Server
    
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
      --help                          Show this message and exit.



.. _`pywbemcli class hierarchy --help`:

pywbemcli class hierarchy --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class hierarchy --help` subcommand


::

    Error, None
    Usage: pywbemcli class hierarchy [COMMAND-OPTIONS] CLASSNAME
    
      Display class inheritance hierarchy as a tree.
    
      The classname option, if it exists defines the topmost class of the
      hierarchy to include in the display. This is a separate subcommand because
      it is tied specifically to displaying in a tree format.
    
    Options:
      -s, --superclasses      Display the superclasses to CLASSNAME.  In this case
                              CLASSNAME is required
      -n, --namespace <name>  Namespace to use for this operation. If defined that
                              namespace overrides the general options namespace
      --help                  Show this message and exit.



.. _`pywbemcli class invokemethod --help`:

pywbemcli class invokemethod --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class invokemethod --help` subcommand


::

    Error, None
    Usage: pywbemcli class invokemethod [COMMAND-OPTIONS] classname name
    
      Invoke the class method named methodname in the class classname
    
    Options:
      -p, --parameter parameter  Optional multiple method parameters of form
                                 name=value
      -n, --namespace <name>     Namespace to use for this operation. If defined
                                 that namespace overrides the general options
                                 namespace
      --help                     Show this message and exit.



.. _`pywbemcli class references --help`:

pywbemcli class references --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli class references --help` subcommand


::

    Error, None
    Usage: pywbemcli class references [COMMAND-OPTIONS] CLASSNAME
    
      Get the reference classes for the CLASSNAME.
    
      Get the reference classes (or their classnames) for the CLASSNAME argument
      filtered by the role and result class options and modified  by the other
      options.
    
    Options:
      -r, --resultclass <class name>  Filter by the classname provided.
      -x, --role <role name>          Filter by the role name provided.
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
      --help                          Show this message and exit.



.. _`pywbemcli connection --help`:

pywbemcli connection --help
---------------------------



The following defines the help output for the `pywbemcli connection --help` subcommand


::

    Error, None
    Usage: pywbemcli connection [COMMAND-OPTIONS] COMMAND [ARGS]...
    
      Command group to manage WBEM connections.
    
      These command allow viewing and setting connection information.
    
      In addition to the command-specific options shown in this help text, the
      general options (see 'pywbemcli --help') can also be specified before the
      command. These are NOT retained after the command is executed.
    
    Options:
      --help  Show this message and exit.
    
    Commands:
      create  Create a new named connection from the input...
      delete  Show the current connection information, i.e.
      export  Export the current connection information.
      list    Execute a simple wbem request to test that...
      select  Select a connection from the current defined...
      set     Set current connection into repository.
      show    Show the current connection information, i.e.
      test    Execute a simple wbem request to test that...



.. _`pywbemcli connection create --help`:

pywbemcli connection create --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection create --help` subcommand


::

    Error, None
    Usage: pywbemcli connection create [COMMAND-OPTIONS] name SERVER
    
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
      -t, --timeout TEXT            Operation timeout for the WBEM Server in
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
      --help                        Show this message and exit.



.. _`pywbemcli connection delete --help`:

pywbemcli connection delete --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection delete --help` subcommand


::

    Error, None
    Usage: pywbemcli connection delete [COMMAND-OPTIONS] name
    
      Show the current connection information, i.e. all the variables that make
      up the current connection
    
    Options:
      --help  Show this message and exit.



.. _`pywbemcli connection export --help`:

pywbemcli connection export --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection export --help` subcommand


::

    Error, None
    Usage: pywbemcli connection export [COMMAND-OPTIONS]
    
      Export  the current connection information.
    
      Creates an export statement for each connection variable and outputs the
      statement to the conole.
    
    Options:
      --help  Show this message and exit.



.. _`pywbemcli connection list --help`:

pywbemcli connection list --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection list --help` subcommand


::

    Error, None
    Usage: pywbemcli connection list [COMMAND-OPTIONS]
    
      Execute a simple wbem request to test that the connection exists and is
      working.
    
    Options:
      --help  Show this message and exit.



.. _`pywbemcli connection select --help`:

pywbemcli connection select --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection select --help` subcommand


::

    Error, None
    Usage: pywbemcli connection select [COMMAND-OPTIONS] name
    
      Select a connection from the current defined connections
    
    Options:
      --help  Show this message and exit.



.. _`pywbemcli connection set --help`:

pywbemcli connection set --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection set --help` subcommand


::

    Error, None
    Usage: pywbemcli connection set [COMMAND-OPTIONS] name
    
      Set current connection into repository.
    
      Sets the current wbem connection information into the repository of
      connections. If the name does not already exist in the connection
      information, the provided name is used.
    
    Options:
      --help  Show this message and exit.



.. _`pywbemcli connection show --help`:

pywbemcli connection show --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection show --help` subcommand


::

    Error, None
    Usage: pywbemcli connection show [COMMAND-OPTIONS] name
    
      Show the current connection information, i.e. all the variables that make
      up the current connection
    
    Options:
      --help  Show this message and exit.



.. _`pywbemcli connection test --help`:

pywbemcli connection test --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli connection test --help` subcommand


::

    Error, None
    Usage: pywbemcli connection test [COMMAND-OPTIONS]
    
      Execute a simple wbem request to test that the connection exists and is
      working.
    
    Options:
      --help  Show this message and exit.



.. _`pywbemcli help --help`:

pywbemcli help --help
---------------------



The following defines the help output for the `pywbemcli help --help` subcommand


::

    Error, None
    Usage: pywbemcli help [OPTIONS]
    
      Show help message for interactive mode.
    
    Options:
      --help  Show this message and exit.



.. _`pywbemcli instance --help`:

pywbemcli instance --help
-------------------------



The following defines the help output for the `pywbemcli instance --help` subcommand


::

    Error, None
    Usage: pywbemcli instance [COMMAND-OPTIONS] COMMAND [ARGS]...
    
      Command Group to manage CIM instances.
    
      This incudes functions to get, enumerate, create, modify, and delete
      instances in a namspace and additional functions to get more general
      information on instances (ex. counts) within the namespace
    
      In addition to the command-specific options shown in this help text, the
      general options (see 'pywbemcli --help') can also be specified before the
      command. These are NOT retained after the command is executed.
    
    Options:
      --help  Show this message and exit.
    
    Commands:
      associators   Get the associated instances or instance...
      count         Get number of instances for each class in...
      create        Create an instance of classname.
      delete        Delete a single instance defined by...
      enumerate     Enumerate instances or instance names from...
      get           Get a single CIMInstance.
      invokemethod  Invoke the method defined by instancename and...
      query         Execute the query defined by the query...
      references    Get the reference instances or instance...



.. _`pywbemcli instance associators --help`:

pywbemcli instance associators --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance associators --help` subcommand


::

    Error, None
    Usage: pywbemcli instance associators [COMMAND-OPTIONS] INSTANCENAME
    
      Get the associated instances or instance names.
    
      Returns the associated instances or names (names-only option) for the
      INSTANCENAME argument filtered by the assocclass, resultclass, role and
      resultrole arguments. This may be executed interactively by providing only
      a classname and the interactive option.
    
    Options:
      -a, --assocclass <class name>   Filter by the associated instancename
                                      provided.
      -r, --resultclass <class name>  Filter by the result class name provided.
      -x, --role <role name>          Filter by the role name provided.
      -o, --resultrole <class name>   Filter by the result role name provided.
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
      --help                          Show this message and exit.



.. _`pywbemcli instance count --help`:

pywbemcli instance count --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance count --help` subcommand


::

    Error, None
    Usage: pywbemcli instance count [COMMAND-OPTIONS] CLASSNAME regex
    
      Get number of instances for each class in namespace.
    
      The size of the response may be limited by CLASSNAME argument which
      defines a classname regular expression so that only those classes are
      counted
    
      The CLASSNAME argument is optional.
    
      The CLASSNAME argument may be either a complete classname or a regular
      expression that can be matched to one or more classnames. To limit the
      filter to a single classname, terminate the classname with $.
    
      The regular expression is anchored to the beginning of the classname and
      is case insensitive. Thus pywbem_ returns all classes that begin with
      PyWBEM_, pywbem_, etc.
    
    Options:
      -s, --sort              Sort by instance count. Otherwise sorted by
                              classname
      -n, --namespace <name>  Namespace to use for this operation. If defined that
                              namespace overrides the general options namespace
      --help                  Show this message and exit.



.. _`pywbemcli instance create --help`:

pywbemcli instance create --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance create --help` subcommand


::

    Error, None
    Usage: pywbemcli instance create [COMMAND-OPTIONS] classname
    
      Create an instance of classname.
    
    Options:
      -x, --property property         Optional multiple property definitions of
                                      form name=value
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
      --help                          Show this message and exit.



.. _`pywbemcli instance delete --help`:

pywbemcli instance delete --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance delete --help` subcommand


::

    Error, None
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
      --help                  Show this message and exit.



.. _`pywbemcli instance enumerate --help`:

pywbemcli instance enumerate --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance enumerate --help` subcommand


::

    Error, None
    Usage: pywbemcli instance enumerate [COMMAND-OPTIONS] CLASSNAME
    
      Enumerate instances or instance names from the WBEMServer starting either
      at the top  of the hiearchy (if no classname provided) or from the
      classname argument provided.
    
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
      --help                          Show this message and exit.



.. _`pywbemcli instance get --help`:

pywbemcli instance get --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance get --help` subcommand


::

    Error, None
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
      --help                          Show this message and exit.



.. _`pywbemcli instance invokemethod --help`:

pywbemcli instance invokemethod --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance invokemethod --help` subcommand


::

    Error, None
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
      --help                     Show this message and exit.



.. _`pywbemcli instance query --help`:

pywbemcli instance query --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance query --help` subcommand


::

    Error, None
    Usage: pywbemcli instance query [COMMAND-OPTIONS] <query string>
    
      Execute the query defined by the query argument.
    
    Options:
      -l, --querylanguage <query language>
                                      Use the query language defined. (Default:
                                      DMTF:CQL.
      -n, --namespace <name>          Namespace to use for this operation. If
                                      defined that namespace overrides the general
                                      options namespace
      -s, --sort                      Sort into alphabetical order by classname.
      --help                          Show this message and exit.



.. _`pywbemcli instance references --help`:

pywbemcli instance references --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli instance references --help` subcommand


::

    Error, None
    Usage: pywbemcli instance references [COMMAND-OPTIONS] INSTANCENAME
    
      Get the reference instances or instance names.
    
      For the INSTANCENAME argument provided return instances or instance names
      (names-only option) filtered by the role and result class options. This
      may be executed interactively by providing only a classname and the
      interactive option.
    
    Options:
      -r, --resultclass <class name>  Filter by the result class name provided.
      -o, --role <role name>          Filter by the role name provided.
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
      --help                          Show this message and exit.



.. _`pywbemcli qualifier --help`:

pywbemcli qualifier --help
--------------------------



The following defines the help output for the `pywbemcli qualifier --help` subcommand


::

    Error, None
    Usage: pywbemcli qualifier [COMMAND-OPTIONS] COMMAND [ARGS]...
    
      Command Group to manage CIM QualifierDeclarations.
    
      Includes the capability to get and enumerate qualifier declarations.
    
      This does not provide the capability to create or delete CIM
      QualifierDeclarations
    
      In addition to the command-specific options shown in this help text, the
      general options (see 'pywbemcli --help') can also be specified before the
      command. These are NOT retained after the command is executed.
    
    Options:
      --help  Show this message and exit.
    
    Commands:
      enumerate  Enumerate CIMQualifierDeclaractions.
      get        Display CIMQualifierDeclaration.



.. _`pywbemcli qualifier enumerate --help`:

pywbemcli qualifier enumerate --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli qualifier enumerate --help` subcommand


::

    Error, None
    Usage: pywbemcli qualifier enumerate [COMMAND-OPTIONS]
    
      Enumerate CIMQualifierDeclaractions.
    
      Displays all of the CIMQualifierDeclaration objects in the defined
      namespace in the current WBEM Server
    
    Options:
      -n, --namespace <name>  Namespace to use for this operation. If defined that
                              namespace overrides the general options namespace
      -s, --sort              Sort into alphabetical order by classname.
      --help                  Show this message and exit.



.. _`pywbemcli qualifier get --help`:

pywbemcli qualifier get --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli qualifier get --help` subcommand


::

    Error, None
    Usage: pywbemcli qualifier get [COMMAND-OPTIONS] NAME
    
      Display CIMQualifierDeclaration.
    
      Displays a single CIMQualifierDeclaration for the defined namespace in the
      current WBEMServer
    
    Options:
      -n, --namespace <name>  Namespace to use for this operation. If defined that
                              namespace overrides the general options namespace
      --help                  Show this message and exit.



.. _`pywbemcli repl --help`:

pywbemcli repl --help
---------------------



The following defines the help output for the `pywbemcli repl --help` subcommand


::

    Error, None
    Usage: pywbemcli repl [OPTIONS]
    
      Enter interactive (REPL) mode (default) and load any existing history
      file.
    
    Options:
      --help  Show this message and exit.



.. _`pywbemcli server --help`:

pywbemcli server --help
-----------------------



The following defines the help output for the `pywbemcli server --help` subcommand


::

    Error, None
    Usage: pywbemcli server [COMMAND-OPTIONS] COMMAND [ARGS]...
    
      Command Group for WBEM server operations.
    
      In addition to the command-specific options shown in this help text, the
      general options (see 'pywbemcli --help') can also be specified before the
      command. These are NOT retained after the command is executed.
    
    Options:
      --help  Show this message and exit.
    
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

    Error, None
    Usage: pywbemcli server brand [COMMAND-OPTIONS]
    
      Display interop namespace name in the WBEM Server.
    
    Options:
      --help  Show this message and exit.



.. _`pywbemcli server connection --help`:

pywbemcli server connection --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server connection --help` subcommand


::

    Error, None
    Usage: pywbemcli server connection [COMMAND-OPTIONS]
    
      Display information on the connection used by this server.
    
    Options:
      --help  Show this message and exit.



.. _`pywbemcli server info --help`:

pywbemcli server info --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server info --help` subcommand


::

    Error, None
    Usage: pywbemcli server info [COMMAND-OPTIONS]
    
      Display the brand information on theWBEM Server.
    
    Options:
      --help  Show this message and exit.



.. _`pywbemcli server interop --help`:

pywbemcli server interop --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server interop --help` subcommand


::

    Error, None
    Usage: pywbemcli server interop [COMMAND-OPTIONS]
    
      Display the interop namespace name in the WBEM Server.
    
    Options:
      --help  Show this message and exit.



.. _`pywbemcli server namespaces --help`:

pywbemcli server namespaces --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server namespaces --help` subcommand


::

    Error, None
    Usage: pywbemcli server namespaces [COMMAND-OPTIONS]
    
      Display the namespaces in the WBEM server
    
    Options:
      --help  Show this message and exit.



.. _`pywbemcli server profiles --help`:

pywbemcli server profiles --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server profiles --help` subcommand


::

    Error, None
    Usage: pywbemcli server profiles [COMMAND-OPTIONS]
    
      Display profiles in the WBEM Server.
    
      This display may be filtered by the optional organization and profile name
      options
    
    Options:
      -o, --organization <org name>   Filter by the defined organization. (ex. -o
                                      DMTF
      -n, --profilename <profile name>
                                      Filter by the profile name. (ex. -n Array
      --help                          Show this message and exit.



.. _`pywbemcli server test_pull --help`:

pywbemcli server test_pull --help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



The following defines the help output for the `pywbemcli server test_pull --help` subcommand


::

    Error, None
    Usage: pywbemcli server test_pull [COMMAND-OPTIONS]
    
      Test whether pull opeations exist on the WBEM server.
    
    Options:
      --help  Show this message and exit.


