
########################################################
Overview of pywbemcli help with the multiple subcommands
########################################################

This is a display of the output of the pywbemcli commands define in this file. Each help output is presented as a section title with the command as sent to pywbemcli followed by the ouput returned by pywbemcli.

*****************
pywbemcli  --help
*****************

::

    Usage: pywbemcli [GENERAL-OPTIONS] COMMAND [ARGS]...
    
      Command line browser for WBEM Servers. This cli tool implements the
      CIM/XML client APIs as defined in pywbem to make requests to a WBEM
      server.
    
      The options shown above that can also be specified on any of the
      (sub-)commands.
    
    Options:
      -s, --server TEXT               Hostname or IP address with scheme of the
                                      WBEMServer (EnvVar: PYWBEMCLI_SERVER).
      -d, --default_namespace TEXT    Default Namespace to use in the target
                                      WBEMServer if no namespace is defined in the
                                      subcommand(EnvVar:
                                      PYWBEMCLI_DEFAULT_NAMESPACE). (Default:
                                      root/cimv2).
      -u, --user TEXT                 User name for the WBEM Server connection.
                                      (EnvVar: PYWBEMCLI_USER).
      -p, --password TEXT             Password for the WBEM Server (EnvVar:
                                      PYWBEMCLI_PASSWORD ).
      -t, --timeout TEXT              Operation timeout for the WBEM Server.
                                      (EnvVar: PYWBEMCLI_TIMEOUT).
      -n, --noverify                  If set, client does not verify server
                                      certificate.
      -x, --certfile TEXT             Server certfile. Ignored if noverify flag
                                      set. (EnvVar: PYWBEMCLI_CERTFILE).
      -k, --keyfile TEXT              Client private key file. (EnvVar:
                                      PYWBEMCLI_KEYFILE).
      -o, --output-format [mof|xml|table|csv|text]
                                      Output format (Default: mof). pywbemcli may
                                      override the format choice depending on the
                                      operation since not all formats apply to all
                                      output data types
      --debug                         Display transmited and received packets
                                      TEMP.
      -v, --verbose                   Display extra information about the
                                      processing.
      --version                       Show the version of this command and exit.
      --help                          Show this message and exit.
    
    Commands:
      class       Command Group to manage CIM Classes.
      connection  Command group to manage WBEM connections...
      help        Show help message for interactive mode.
      instance    Command Group to manage CIM instances.
      qualifier   Command Group to manage CIM...
      repl        Enter interactive (REPL) mode (default) and...
      server      Command Group for WBEM server operations.



**********************
pywbemcli class --help
**********************

::

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
      find          Find all classes that match the CLASSNAME...
      get           get and display a single class from the WBEM...
      hierarchy     Display class inheritance hierarchy as a...
      invokemethod  Invoke the class method named methodname in...
      names         Get and display classnames from the...
      references    Get the reference classes for the CLASSNAME.



**************************
pywbemcli class get --help
**************************

::

    Usage: pywbemcli class get [COMMAND-OPTIONS] CLASSNAME
    
      get and display a single class from the WBEM Server
    
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



***********************************
pywbemcli class invokemethod --help
***********************************

::

    Usage: pywbemcli class invokemethod [COMMAND-OPTIONS] classname name
    
      Invoke the class method named methodname in the class classname
    
    Options:
      -p, --parameter parameter  Optional multiple method parameters of form
                                 name=value
      -n, --namespace <name>     Namespace to use for this operation. If defined
                                 that namespace overrides the general options
                                 namespace
      --help                     Show this message and exit.



****************************
pywbemcli class names --help
****************************

::

    Usage: pywbemcli class names [COMMAND-OPTIONS] CLASSNAME
    
      Get and display classnames from the WBEMServer.
    
      Enumerates the classnames from the WBEMServer starting either at the top
      of the class hierarchy or from  the position in the class hierarch defined
      by the optional`classname` argument if provided.
    
      The output format is normally a list of the classnames
    
      This command corresponds to `class enumerate  -o`
    
      The deepinheritance option defines whether the complete hiearchy is
      retrieved or just the next level in the hiearchy.
    
    Options:
      -d, --deepinheritance           Return complete subclass hiearchy for this
                                      class.
      -d, --deepinheritance           Return complete subclass hiearchy for this
                                      class.
      --includequalifiers / --no_includequalifiers
                                      Include qualifiers in the result. Default is
                                      to include qualifiers
      -c, --includeclassorigin        Include classorigin in the result.
      -s, --sort                      Sort into alphabetical order by classname.
      -n, --namespace <name>          Namespace to use for this operation. If
                                      defined that namespace overrides the general
                                      options namespace
      --help                          Show this message and exit.



********************************
pywbemcli class enumerate --help
********************************

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
      --help                          Show this message and exit.



**********************************
pywbemcli class associators --help
**********************************

::

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



*********************************
pywbemcli class references --help
*********************************

::

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



***************************
pywbemcli class find --help
***************************

::

    Usage: pywbemcli class find [COMMAND-OPTIONS] CLASSNAME regex
    
      Find all classes that match the CLASSNAME regex.
    
      Find all of the classes in the namespace  of the defined WBEMServer that
      match the CLASSNAME  regular expression argument in the namespaces of the
      defined WBEMserver.
    
      The CLASSNAME argument is required.
    
      The CLASSNAME argument may be either a complete classname or a regular
      expression that can be matched to one or more classnames. To limit the
      filter to a single classname, terminate the classname with $.
    
      The regular expression is anchored to the beginning of the classname and
      is case insensitive. Thus pywbem_ returns all classes that begin with
      PyWBEM_, pywbem_, etc.
    
      The namespace option limits the search to the defined namespace
    
    Options:
      -s, --sort              Sort into alphabetical order by classname.
      -n, --namespace <name>  Namespace to use for this operation. If defined that
                              namespace overrides the general options namespace
      --help                  Show this message and exit.



********************************
pywbemcli class hierarchy --help
********************************

::

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



*****************************
pywbemcli instance get --help
*****************************

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
      --help                          Show this message and exit.



********************************
pywbemcli instance delete --help
********************************

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
      --help                  Show this message and exit.



********************************
pywbemcli instance create --help
********************************

::

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



**************************************
pywbemcli instance invokemethod --help
**************************************

::

    Usage: pywbemcli instance invokemethod [COMMAND-OPTIONS] name name
    
      Invoke the method defined by instancename and methodname with parameters.
    
      This issues an instance level invokemethod request and displays the
      results.
    
    Options:
      -p, --parameter parameter  Optional multiple method parameters of form
                                 name=value
      -n, --namespace <name>     Namespace to use for this operation. If defined
                                 that namespace overrides the general options
                                 namespace
      --help                     Show this message and exit.



*******************************
pywbemcli instance query --help
*******************************

::

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



*******************************
pywbemcli instance names --help
*******************************

::

    Usage: pywbemcli instance names [COMMAND-OPTIONS] [CLASSNAME]
    
      Get and display a list of instance names of the classname argument.
    
      This is equivalent to pywbemcli instance enumerate -o
    
    Options:
      -n, --namespace <name>  Namespace to use for this operation. If defined that
                              namespace overrides the general options namespace
      -s, --sort              Sort into alphabetical order by classname.
      --help                  Show this message and exit.



***********************************
pywbemcli instance enumerate --help
***********************************

::

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



*******************************
pywbemcli instance count --help
*******************************

::

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



************************************
pywbemcli instance references --help
************************************

::

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



*************************************
pywbemcli instance associators --help
*************************************

::

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



**************************
pywbemcli qualifier --help
**************************

::

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



************************************
pywbemcli qualifier enumerate --help
************************************

::

    Usage: pywbemcli qualifier enumerate [COMMAND-OPTIONS]
    
      Enumerate CIMQualifierDeclaractions.
    
      Displays all of the CIMQualifierDeclaration objects in the defined
      namespace in the current WBEM Server
    
    Options:
      -n, --namespace <name>  Namespace to use for this operation. If defined that
                              namespace overrides the general options namespace
      -s, --sort              Sort into alphabetical order by classname.
      --help                  Show this message and exit.



******************************
pywbemcli qualifier get --help
******************************

::

    Usage: pywbemcli qualifier get [COMMAND-OPTIONS] NAME
    
      Display CIMQualifierDeclaration.
    
      Displays a single CIMQualifierDeclaration for the defined namespace in the
      current WBEMServer
    
    Options:
      -n, --namespace <name>  Namespace to use for this operation. If defined that
                              namespace overrides the general options namespace
      --help                  Show this message and exit.



***********************
pywbemcli server --help
***********************

::

    Usage: pywbemcli server [COMMAND-OPTIONS] COMMAND [ARGS]...
    
      Command Group for WBEM server operations.
    
      In addition to the command-specific options shown in this help text, the
      general options (see 'pywbemcli --help') can also be specified before the
      command. These are NOT retained after the command is executed.
    
    Options:
      --help  Show this message and exit.
    
    Commands:
      brand       Display the interop namespace name in the...
      connection  Display information on the connection used by...
      info        Display the brand information on the current...
      interop     Display the interop namespace name in the...
      namespaces  Display the set of namespaces in the current...
      profiles    Display profiles on the current WBEM Server.



*****************************
pywbemcli server brand --help
*****************************

::

    Usage: pywbemcli server brand [COMMAND-OPTIONS]
    
      Display the interop namespace name in the WBEM Server.
    
    Options:
      --help  Show this message and exit.



**********************************
pywbemcli server connection --help
**********************************

::

    Usage: pywbemcli server connection [COMMAND-OPTIONS]
    
      Display information on the connection used by this server.
    
    Options:
      --help  Show this message and exit.



****************************
pywbemcli server info --help
****************************

::

    Usage: pywbemcli server info [COMMAND-OPTIONS]
    
      Display the brand information on the current WBEM Server.
    
    Options:
      --help  Show this message and exit.



**********************************
pywbemcli server namespaces --help
**********************************

::

    Usage: pywbemcli server namespaces [COMMAND-OPTIONS]
    
      Display the set of namespaces in the current WBEM server
    
    Options:
      -s, --sort  Sort into alphabetical order by classname.
      --help      Show this message and exit.



*******************************
pywbemcli server interop --help
*******************************

::

    Usage: pywbemcli server interop [COMMAND-OPTIONS]
    
      Display the interop namespace name in the WBEM Server.
    
    Options:
      --help  Show this message and exit.



********************************
pywbemcli server profiles --help
********************************

::

    Usage: pywbemcli server profiles [COMMAND-OPTIONS]
    
      Display profiles on the current WBEM Server.
    
      This display may be filtered by the optional organization and profile name
      options
    
    Options:
      -o, --organization <org name>   Filter by the defined organization. (ex. -o
                                      DMTF
      -n, --profilename <profile name>
                                      Filter by the profile name. (ex. -n Array
      --help                          Show this message and exit.



********************************
pywbemcli connection show --help
********************************

::

    Usage: pywbemcli connection show [COMMAND-OPTIONS]
    
      Show the current connection information, i.e. all the variables that make
      up the current connection
    
    Options:
      --help  Show this message and exit.


